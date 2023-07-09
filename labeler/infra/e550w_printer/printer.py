import io
import logging
from math import inf

from brother_ql import BrotherQLRaster, create_label
from brother_ql.backends import guess_backend, backend_factory
from pysnmp.entity.engine import SnmpEngine
from pysnmp.hlapi import getCmd, CommunityData, UdpTransportTarget, ContextData
from pysnmp.smi.rfc1902 import ObjectType, ObjectIdentity

from labeler.domain.objects import MediaDefinition, Dimension, Image
from labeler.infra.e550w_printer.media_definitions import (
    media_width,
    tape_color,
    text_color,
    media_type,
    WIDTH_BYTE,
    COLOR_BYTE,
    TEXT_COLOR_BYTE,
    TYPE_BYTE,
)
from labeler.interfaces import Printer
from PIL import Image as PILImage

PRINTABLE_WIDTH = {
    12: Dimension.from_points(150, 360),
    24: Dimension.from_points(320, 360),
}


class E550W(Printer):
    def __init__(self, ip_address: str):
        self.ip_address = ip_address
        self.snmp_port = 161

    def get_installed_media(self) -> MediaDefinition:
        return self.__get_printer_status()

    def print_label(self, label: Image):
        im = PILImage.open(io.BytesIO(label.bytes))

        qlr = BrotherQLRaster("PT-E550W")
        create_label(
            qlr,
            im,
            self.__media_width_to_type(label.height),
            red=False,
            threshold=70,
            cut=True,
            rotate=270,
            compress=True,
            dpi_600=True,
            hq=True,
        )

        try:
            try:
                selected_backend = guess_backend(f"tcp://{self.ip_address}:9100")
            except ValueError:
                logging.error(
                    "Couln't guess the backend to use from the printer string descriptor"
                )
            BACKEND_CLASS = backend_factory(selected_backend)["backend_class"]
            be = BACKEND_CLASS(f"tcp://{self.ip_address}:9100")
            be.write(qlr.data)
            be.dispose()
            del be
        except Exception as e:
            logging.exception("Exception happened: %s", e)

    def __media_width_to_type(self, height: int):
        metric_width = Dimension.from_points(height, 360)
        if metric_width == Dimension.from_points(150, 360):
            return "pt512"
        else:
            raise ValueError(f"Unsupported media width: {metric_width}")

    def __get_printer_status(self):
        raw_snmp_data = self.__get_snmp_status().asNumbers()
        width = media_width(raw_snmp_data[WIDTH_BYTE])
        media_tape_color = tape_color(raw_snmp_data[COLOR_BYTE])
        media_text_color = text_color(raw_snmp_data[TEXT_COLOR_BYTE])
        tape_type = media_type(raw_snmp_data[TYPE_BYTE])

        return MediaDefinition(
            width=Dimension(mm=width),
            length=Dimension(mm=inf),
            minimal_margin_vertical=(Dimension(mm=width) - PRINTABLE_WIDTH[width]) / 2,
            minimal_margin_horizontal=Dimension(mm=1),
            dpi=360,
            description=f"{tape_type} - {width}mm, {media_text_color} on {media_tape_color} background",
        )

    def __get_snmp_status(self):
        """
        This oid was found by using wireshark, however it's also documented here:
        https://support.brother.com/g/s/es/dev/en/command/faq/index.html?c=eu_ot&lang=en&navi=offall&comple=on&redirect=on
        just not for the E550W model.
        """
        oid = "1.3.6.1.4.1.2435.3.3.9.1.6.1.0"

        error_indication, error_status, error_index, var_binds = next(
            getCmd(
                SnmpEngine(),
                CommunityData("public", mpModel=0),
                UdpTransportTarget((self.ip_address, self.snmp_port)),
                ContextData(),
                ObjectType(ObjectIdentity(oid)),
            )
        )

        if error_indication:
            raise Exception(error_indication)
        elif error_status:
            raise Exception(
                "%s at %s"
                % (
                    error_status.prettyPrint(),
                    error_index and var_binds[int(error_index) - 1][0] or "?",
                )
            )
        else:
            return var_binds[0][1]
