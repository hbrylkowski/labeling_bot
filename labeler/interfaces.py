import abc

from labeler.domain.objects import LabelDefinition, Image, MediaDefinition


class Renderer(abc.ABC):
    @abc.abstractmethod
    def render_label(self, label_definition: LabelDefinition) -> Image:
        pass


class Printer(abc.ABC):
    @abc.abstractmethod
    def get_installed_media(self) -> MediaDefinition:
        pass
