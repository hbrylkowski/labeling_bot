import textwrap
from string import ascii_letters

from PIL import ImageFont, ImageDraw, Image as PILImage

from labeler.domain.objects import Image, LabelDefinition
from labeler.interfaces import Renderer


class PILRenderer(Renderer):
    def __init__(self):
        self.font_path = "/Library/Fonts/Arial.ttf"

    def render_label(self, label_definition: LabelDefinition) -> Image:
        if label_definition.length is None:
            pil_image = self.__render_no_fixed_lenth(label_definition)
        else:
            pil_image = self.__render_fixed_length(label_definition)

        return Image.from_pil(pil_image)

    def __render_fixed_length(self, label_definition: LabelDefinition):
        width = label_definition.pixel_width
        length = label_definition.pixel_length
        font, text = self.__get_font(
            label_definition.text,
            width,
            length,
        )
        im = PILImage.new("1", (length, width), 1)
        draw = ImageDraw.Draw(im)
        draw.text(
            (length / 2, width / 2),
            text,
            font=font,
            fill=0,
            anchor="mm",
            align="center",
        )
        return im

    def __render_no_fixed_lenth(self, label_definition: LabelDefinition):
        lines_to_print = label_definition.text.count("\n") + 1
        text = "\n".join([line.strip() for line in label_definition.text.split("\n")])

        text_height = label_definition.pixel_width // lines_to_print

        while text_height > 0:
            font = ImageFont.truetype(
                "/Library/Fonts/Arial.ttf",
                text_height,
            )
            if lines_to_print > 1:
                occupied_height = font.getsize_multiline(text)[1]
            else:
                occupied_height = font.getsize(text)[1]
            if occupied_height <= label_definition.pixel_width:
                break
            text_height -= 1

        sizes = [font.getsize(line) for line in text.split("\n")]

        length = max(length for length, height in sizes)

        im = PILImage.new("1", (length, label_definition.pixel_width), 1)
        draw = ImageDraw.Draw(im)
        draw.text(
            (length / 2, label_definition.pixel_width / 2),
            text,
            font=font,
            fill=0,
            anchor="mm",
            align="center",
        )
        return im

    def __get_font(self, text: str, max_width: int, max_length: int):
        font_size = max_width
        step = max_width // 2
        last_good = None
        last_corrected = None
        while step > 1:
            fits, corrected = self.__will_font_fit(
                text, self.font_path, font_size, max_width, max_length
            )
            if fits:
                last_good = font_size
                last_corrected = corrected
                font_size += step
            else:
                font_size -= step
            step //= 2

        return ImageFont.truetype(self.font_path, last_good), last_corrected

    def __will_font_fit(
        self, text: str, font_path: str, font_size: int, max_width: int, max_length: int
    ):
        font = ImageFont.truetype(font_path, font_size)
        if "\n" in text:
            text_width, text_height = font.getsize_multiline(text)
        else:
            text_width, text_height = font.getsize(text)

        if text_height > max_width:
            return False, None

        if text_width <= max_length:
            # Now we know that the text fits. We can stop trying
            return True, text

        avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(
            ascii_letters
        )
        charachters_per_line = max_length // avg_char_width
        if charachters_per_line < max(len(line) for line in text.split(" ")):
            return False, None

        wrapped = textwrap.fill(text, charachters_per_line)
        wrapped_width, wrapped_height = font.getsize_multiline(wrapped)
        if wrapped_height <= max_width and wrapped_width <= max_length:
            # Now we know that the text fits. We can stop trying
            return True, wrapped

        return False, None
