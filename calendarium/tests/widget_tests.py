"""Tests for the widgets of the ``calendarium`` app."""
from django.test import TestCase

from ..widgets import ColorPickerWidget


class ColorPickerWidgetTestCase(TestCase):
    """Tests for the ``ColorPickerWidget`` widget."""
    longMessage = True

    def setUp(self):
        self.widget = ColorPickerWidget()

    def test_render_tag(self):
        self.assertIn('value="ffffff"', self.widget.render('field', 'ffffff'),
                      msg=('Should render the input form.'))
