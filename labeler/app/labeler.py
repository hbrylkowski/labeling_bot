from labeler.domain.objects import (
    Label,
    LabelRequest,
    LabelDefinition,
    MediaDefinition,
    Dimension,
    Image,
)
from labeler.interfaces import Renderer, Printer


class Application:
    def __init__(self, renderer: Renderer, printer: Printer):
        self.renderer = renderer
        self.printer = printer

    def render_preview(self, text: str, length: int = None) -> Label:
        media = self.printer.get_installed_media()

        if length != 0:
            label_length = Dimension(mm=length) - 2 * media.minimal_margin_horizontal
        else:
            label_length = None

        label_definition = LabelDefinition(
            text=text,
            length=label_length,
            width=media.printable_width,
            dpi=media.dpi,
        )

        self.renderer.render_label(label_definition)

    def print_label(self, text: str, length: int = None) -> Image:
        media = self.printer.get_installed_media()

        if length != 0:
            label_length = Dimension(mm=length) - 2 * media.minimal_margin_horizontal
        else:
            label_length = None

        label_definition = LabelDefinition(
            text=text,
            length=label_length,
            width=media.printable_width,
            dpi=media.dpi,
        )

        label = self.renderer.render_label(label_definition)
        self.printer.print_label(label)
        return label

    def get_installed_media(self) -> MediaDefinition:
        return self.printer.get_installed_media()
