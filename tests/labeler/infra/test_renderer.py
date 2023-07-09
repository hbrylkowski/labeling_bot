from labeler.domain.objects import LabelDefinition, Dimension
from labeler.infra.renderer import PILRenderer


def test_simple_label(get_test_image):
    renderer = PILRenderer()
    expected_label = get_test_image("simple_label_test.png")

    definition = LabelDefinition(
        text="dolphin", length=Dimension(mm=40), width=Dimension(mm=10), dpi=600
    )

    label = renderer.render_label(definition)

    assert label.bytes == expected_label


def test_multiline_label(get_test_image):
    label_text = "dolphin\nis\nawesome"
    expected_label = get_test_image("multiline_label_test.png")

    renderer = PILRenderer()
    definition = LabelDefinition(
        text=label_text, length=Dimension(mm=40), width=Dimension(mm=10), dpi=600
    )

    label = renderer.render_label(definition)
    assert label.bytes == expected_label


def test_simple_label_no_fixed_width(get_test_image):
    renderer = PILRenderer()
    expected_label = get_test_image("no_fixed_width.png")

    definition = LabelDefinition(text="dolphin", width=Dimension(mm=10), dpi=600)

    label = renderer.render_label(definition)
    assert label.bytes == expected_label


def test_multiline_label_no_fixed_width(get_test_image):
    renderer = PILRenderer()
    expected_label = get_test_image("multiline_label_no_fixed_width.png")

    definition = LabelDefinition(
        text="dolphin\nis\nawesome", width=Dimension(mm=10), dpi=600
    )

    label = renderer.render_label(definition)
    assert label.bytes == expected_label
