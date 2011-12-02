from django import template
from django.utils.safestring import mark_safe

import _fb_script_template, _param_parser
from ...lib import settings

register = template.Library()

class FBScriptNode(template.Node):
    """
    Loads facebook sdk using the channel url
    Optionally sets FB.Canvas size
    Optionally loads Facebook Share JS
    Optionally applies IE monkey patches 19042 and 20168
    """

    def __init__(self, app_settings, use_share=False, canvas_height=None, canvas_width=None, fix_19042=False, fix_20168=False):
        self.template_vars = dict(
            app_settings=app_settings,
            use_share=self._bool_str(use_share, False),
            canvas_height=self._int_str(canvas_height),
            canvas_width=self._int_str(canvas_width),
            fix_19042=self._bool_str(fix_19042, False),
            fix_20168=self._bool_str(fix_20168, False),
        )

    def _int_str(self, string):
        if string is None:
            return None
        else:
            return int(string)

    def _bool_str(self, string, default=False):
        if string in [True, False]:
            return string
        elif string == 'True':
            return True
        elif string == 'False':
            return False
        else:
            return default

    def render(self, context):
        _template = _fb_script_template.fb_script_template
        _context = template.context.Context(self.template_vars, autoescape=context.autoescape)
        _context['request'] = context
        result = _template.render(_context)
        safe_result = mark_safe(result)
        return safe_result

def _validate_length(tokens, min_args, max_args):
    tag_name = tokens[0]
    if len(tokens) < min_args:
        raise template.TemplateSyntaxError('%r requires at least %s argument(s).' % (tag_name, min_args))
    if max_args and len(tokens) > max_args + 1:
        raise template.TemplateSyntaxError('%r takes at most %s arguments.' % (tag_name, max_args))

def _validate_app_settings(token):
    if not (token[0] == token[-1] and token[0] in ('"', "'")):
        raise template.TemplateSyntaxError("app_name should be in quotes.")
    token = token[1:-1]
    app_settings = settings.app_settings(token)
    if app_settings is None or not hasattr(app_settings, 'app_id') or not hasattr(app_settings, 'scope'):
        raise template.TemplateSyntaxError('%r is not valid for app_settings.' % app_settings)
    return app_settings

def _parse_params(tag_name, bits, allowed_params):
    results = _param_parser.parse_kw_args(tag_name, bits)
    params = dict(results)
    if params and not allowed_params:
        raise template.TemplateSyntaxError('%r does not accept any parameters.' % tag_name)
    else:
        leftovers = dict(results)
        for allowed_param in allowed_params:
            if allowed_param in leftovers:
                leftovers.pop(allowed_param)
        if leftovers:
            for invalid_param in leftovers.iterkeys():
                raise template.TemplateSyntaxError('%r is not a valid keyword argument for %r.' % (invalid_param, tag_name))
    return params

def _parse_token(token, allowed_params=None):
    max_args = 1 + (len(allowed_params) if allowed_params else 0)
    tokens = token.split_contents()
    _validate_length(tokens, 2, max_args)
    app_settings = _validate_app_settings(tokens[1])

    params = {}
    if len(tokens) > 2:
        params = _parse_params(tokens[0], tokens[2:], allowed_params)

    return app_settings, params

@register.tag()
def fb_script(parser, token):
    """
    Renders the Facebook Javascript SDK script required for facebook connectivity.
    Example:
    {% load fb_script %}
    
    {% fb_script 'my_first_fb_app' %}
    
    {# See http://bugs.developers.facebook.net/show_bug.cgi?id=19042 #}
    {% fb_script 'my_first_fb_app' fix_19042=True %} 
    
    {# See http://bugs.developers.facebook.net/show_bug.cgi?id=20168= #}
    {% fb_script 'my_first_fb_app' fix_20168=True %} 
    """
    app_settings, params = _parse_token(token, allowed_params=['fix_19042', 'fix_20168', 'use_share'])
    return FBScriptNode(app_settings, **params)

@register.tag()
def fb_script_with_canvas(parser, token):
    """
    Renders the Facebook Javascript SDK script required for facebook connectivity and sets the Facebook Canvas size.
    Example:
    {% load fb_script %}
    
    {% fb_script_with_canvas 'my_first_fb_app' canvas_height=2000 canvas_width=500 %} {# 500 is the recommended width for a Page Tab #}
    
    {# See http://bugs.developers.facebook.net/show_bug.cgi?id=19042 #}
    {% fb_script_with_canvas 'my_first_fb_app' canvas_height=2000 canvas_width=500 fix_19042=True %} 
    
    {# See http://bugs.developers.facebook.net/show_bug.cgi?id=20168= #}
    {% fb_script_with_canvas 'my_first_fb_app' canvas_height=2000 canvas_width=500 fix_20168=True %} 
    """
    app_settings, params = _parse_token(token, allowed_params=['canvas_height', 'canvas_width', 'fix_19042', 'fix_20168', 'use_share'])
    return FBScriptNode(app_settings, **params)
