import unittest

from django import template

from ....context.templatetags import fb_script

class FBScript(unittest.TestCase):

    def test__validate_length(self):
        self.assertEqual(None, fb_script._validate_length(['tag_name'], 0, 1))
        self.assertEqual(None, fb_script._validate_length(['tag_name'], 1, 1))
        self.assertEqual(None, fb_script._validate_length(['tag_name'], 1, 2))
        self.assertEqual(None, fb_script._validate_length(['tag_name', 'app_settings'], 0, 2))
        self.assertEqual(None, fb_script._validate_length(['tag_name', 'app_settings'], 1, 2))
        self.assertEqual(None, fb_script._validate_length(['tag_name', 'app_settings'], 1, 3))
        self.assertEqual(None, fb_script._validate_length(['tag_name', 'app_settings'], 2, 3))

        self.assertRaises(template.TemplateSyntaxError, lambda: fb_script._validate_length(['tag_name'], 2, 10))
        self.assertRaises(template.TemplateSyntaxError, lambda: fb_script._validate_length(['tag_name', 'app_settings', 'foo', 'bar'], 0, 2))

    def test__validate_app_settings(self):

        from django.conf import settings

        class _settings:
            class valid:
                app_id = None
                scope = None
            class no_app_id:
                scope = None
            class no_scope:
                app_id = None
            class no_nothin:
                pass

        settings.FACEBOOK_SETTINGS = _settings

        self.assertEqual(_settings.valid, fb_script._validate_app_settings('"valid"'))
        self.assertRaises(template.TemplateSyntaxError, lambda: fb_script._validate_app_settings('"no_app_id"'))
        self.assertRaises(template.TemplateSyntaxError, lambda: fb_script._validate_app_settings('"no_scope"'))
        self.assertRaises(template.TemplateSyntaxError, lambda: fb_script._validate_app_settings('"no_nothin"'))

    def test__parse_params(self):

        valid_tokens = ['abc=123', 'def=456']
        invalid_tokens = ['abc=123', 'def']

        params = fb_script._parse_params('foo_tag', valid_tokens, ['abc', 'def'])
        self.assertEqual(params.get('abc', None), '123')
        self.assertEqual(params.get('def', None), '456')

        self.assertRaises(template.TemplateSyntaxError, lambda: fb_script._parse_params('foo_tag', invalid_tokens, ['abc, def']))

