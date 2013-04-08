"""Widgets for the ``calendarium`` app."""
from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe


class ColorPickerWidget(forms.TextInput):
    class Media:
        css = {
            'all': (
                settings.STATIC_URL + 'calendarium/css/colorpicker.css',
            )
        }
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.2.6/jquery.min.js',
            settings.STATIC_URL + 'calendarium/js/colorpicker.js',
            settings.STATIC_URL + 'calendarium/js/colorpicker_list.js',
            settings.STATIC_URL + 'calendarium/js/eye.js',
            settings.STATIC_URL + 'calendarium/js/layout.js',
            settings.STATIC_URL + 'calendarium/js/utils.js',
        )

    def __init__(self, language=None, attrs=None):
        self.language = language or settings.LANGUAGE_CODE[:2]
        super(ColorPickerWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        rendered = super(ColorPickerWidget, self).render(name, value, attrs)
        return rendered + mark_safe(
            u'''<script type="text/javascript">
                $('#id_%s').ColorPicker({
                onSubmit: function(hsb, hex, rgb, el) {
                    $(el).val(hex);
                    $(el).ColorPickerHide();
                },
                onBeforeShow: function () {
                    $(this).ColorPickerSetColor(this.value);
                }
             }).bind('keyup', function(){
                 $(this).ColorPickerSetColor(this.value);
             });
            </script>''' % name)
