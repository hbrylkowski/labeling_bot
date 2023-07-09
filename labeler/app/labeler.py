from labeler.domain.objects import Label, LabelRequest, LabelDefinition, MediaDefinition
from labeler.interfaces import Renderer, Printer


class Application:
    def __init__(self, renderer: Renderer, printer: Printer):
        self.renderer = renderer
        self.printer = printer

    def render_preview(self, label_request: LabelRequest):
        media = self.printer.get_installed_media()

        if label_request.length is not None:
            label_length = label_request.length - 2 * media.minimal_margin_horizontal
        else:
            label_length = media.printable_length

        label_definition = LabelDefinition(
            text=label_request.text,
            length=label_length,
            width=media.printable_width,
            dpi=media.dpi,
        )

        self.renderer.render_label(label_definition)

    def get_installed_media(self) -> MediaDefinition:
        return self.printer.get_installed_media()
