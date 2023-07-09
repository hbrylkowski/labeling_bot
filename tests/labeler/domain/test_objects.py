import math

from labeler.domain.objects import Dimension, MediaDefinition


def test_dimension():
    dimension = Dimension(mm=25.4)

    assert dimension.mm == 25.4
    assert dimension.inch == 1.0

    assert dimension.in_pixels(dpi=300) == 300

    assert dimension + Dimension(mm=10) == Dimension(mm=35.4)
    assert dimension * 2 == Dimension(mm=50.8)

    assert dimension / 2 == Dimension(mm=12.7)


def test_infinite_media():
    media = MediaDefinition(
        width=Dimension(mm=12),
        length=Dimension(mm=math.inf),
        minimal_margin_vertical=Dimension(mm=1),
        minimal_margin_horizontal=Dimension(mm=2),
        dpi=300,
    )

    assert media.printable_length == Dimension(mm=math.inf)
