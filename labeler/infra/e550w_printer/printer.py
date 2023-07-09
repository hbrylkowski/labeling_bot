from math import inf

from pysnmp.entity.engine import SnmpEngine
from pysnmp.hlapi import getCmd, CommunityData, UdpTransportTarget, ContextData
from pysnmp.smi.rfc1902 import ObjectType, ObjectIdentity

from labeler.domain.objects import MediaDefinition, Dimension
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


class E550W(Printer):
    def __init__(self, ip_address: str):
        self.ip_address = ip_address
        self.snmp_port = 161

    def get_installed_media(self) -> MediaDefinition:
        pass

    def __get_printer_status(self):
        raw_snmp_data = self.__get_snmp_status().asNumbers()
        width = media_width(raw_snmp_data[WIDTH_BYTE])
        media_tape_color = tape_color(raw_snmp_data[COLOR_BYTE])
        media_text_color = text_color(raw_snmp_data[TEXT_COLOR_BYTE])
        tape_type = media_type(raw_snmp_data[TYPE_BYTE])

        return MediaDefinition(
            width=Dimension(mm=width),
            length=Dimension(mm=inf),
            minimal_margin_vertical=Dimension(mm=1),
            minimal_margin_horizontal=Dimension(mm=2),
            dpi=600,
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
