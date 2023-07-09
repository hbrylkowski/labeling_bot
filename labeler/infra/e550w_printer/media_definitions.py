"""
Values from technical reference manual, can be found in /labeler_docs/brother/technical_reference_manual.pdf
"""

WIDTH_BYTE = 10
TYPE_BYTE = 11
COLOR_BYTE = 24
TEXT_COLOR_BYTE = 25


def media_width(code):
    if code == 0:
        raise ValueError("NO TAPE")
    elif code == 4:
        return 3.5
    else:
        return code


def media_type(code):
    media = {
        0: "NO TAPE",
        1: "Laminated tape",
        0x11: "Heat-Shrink Tube",
        0x03: "Non-laminated tape",
        0xFF: "Incompatible tape",
    }
    return media.get(code)


def tape_color(code):
    colors = {
        0x01: "White",
        0x02: "Other",
        0x03: "Clear",
        0x04: "Red",
        0x05: "Blue",
        0x06: "Yellow",
        0x07: "Green",
        0x08: "Black",
        0x09: "Clear(White text)",
        0x20: "Matte White",
        0x21: "Matte Clear",
        0x22: "Matte Silver",
        0x23: "Satin Gold",
        0x24: "Satin Silver",
        0x30: "Blue(D)",
        0x31: "Red(D)",
        0x40: "Fluorescent Orange",
        0x41: "Fluorescent Yellow",
        0x50: "Berry Pink(S)",
        0x51: "Light Gray(S)",
        0x52: "Lime Green(S)",
        0x60: "Yellow(F)",
        0x61: "Pink(F)",
        0x62: "Blue(F)",
        0x70: "White(Heat-shrink Tube)",
        0x90: "White(Flex. ID)",
        0x91: "Yellow(Flex. ID)",
        0xF0: "Cleaning",
        0xF1: "Stencil",
        0xFF: "Incompatible",
    }

    return colors.get(code)


def text_color(code):
    colors = {
        0x01: "White",
        0x04: "Red",
        0x05: "Blue",
        0x08: "Black",
        0x0A: "Gold",
        0x62: "Blue(F)",
        0xF0: "Cleaning",
        0xF1: "Stencil",
        0x02: "Other",
        0xFF: "Incompatible",
    }
    return colors.get(code)
