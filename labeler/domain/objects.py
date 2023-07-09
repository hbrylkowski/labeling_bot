import io
from math import inf

from pydantic import BaseModel, Field


class Image(BaseModel):
    bytes: bytes
    width: int
    height: int

    @classmethod
    def from_pil(cls, pil_image):
        buffer = io.BytesIO()
        pil_image.save(buffer, format="PNG")
        buffer.seek(0)

        return cls(
            bytes=buffer.read(),
            width=pil_image.width,
            height=pil_image.height,
        )


class Dimension(BaseModel):
    mm: float
    __EPSILON = 0.0001

    @classmethod
    def from_inch(cls, inch: float) -> "Dimension":
        return cls(mm=inch * 25.4)

    @classmethod
    def from_points(cls, points: float, dpi: int) -> "Dimension":
        return cls.from_inch(points / dpi)

    @property
    def inch(self) -> float:
        return self.mm / 25.4

    def in_pixels(self, dpi: int) -> int:
        return int(self.inch * dpi)

    def __ensure_same_type(self, other):
        if type(other) != Dimension:
            raise TypeError(f"Cannot use {other} to {self}")

    def __add__(self, other):
        self.__ensure_same_type(other)
        return Dimension(mm=self.mm + other.mm)

    def __sub__(self, other):
        self.__ensure_same_type(other)
        return Dimension(mm=self.mm - other.mm)

    def __mul__(self, other):
        if type(other) not in (int, float):
            raise TypeError(f"Cannot multiply {self} by {other}")
        return Dimension(mm=self.mm * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if type(other) not in (int, float):
            raise TypeError(f"Cannot divide {self} by {other}")

        return Dimension(mm=self.mm / other)

    def __eq__(self, other):
        self.__ensure_same_type(other)
        if self.mm == inf and other.mm == inf:
            return True
        return abs(self.mm - other.mm) < self.__EPSILON

    def __lt__(self, other):
        self.__ensure_same_type(other)
        return self.mm < other.mm

    def __gt__(self, other):
        self.__ensure_same_type(other)
        return self.mm > other.mm


class LabelRequest(BaseModel):
    text: str
    length: Dimension | None


class LabelDefinition(BaseModel):
    text: str
    length: Dimension | None = None
    width: Dimension
    dpi: int

    @property
    def pixel_width(self):
        return self.width.in_pixels(self.dpi)

    @property
    def pixel_length(self):
        return self.length.in_pixels(self.dpi)


class MediaDefinition(BaseModel):
    width: Dimension
    length: Dimension
    minimal_margin_vertical: Dimension
    minimal_margin_horizontal: Dimension
    minimum_length: Dimension = Field(default_factory=lambda: Dimension(mm=5))
    dpi: int
    description: str

    @property
    def printable_width(self) -> Dimension:
        return self.width - 2 * self.minimal_margin_vertical

    @property
    def printable_length(self) -> Dimension:
        return self.length - 2 * self.minimal_margin_horizontal


class Label(BaseModel):
    dpi: str
    image: Image
