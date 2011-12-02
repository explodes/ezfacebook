from django import template

TEMPLATE_TEXT = '''{% load absurl %}
<div id="fb-root"></div>
{% url facebook-channel-html as channel_url %}
<script type="text/javascript">
function appendScriptToFBRoot(src){ var e = document.createElement('script'); e.async = true; e.src = document.location.protocol + src; document.getElementById('fb-root').appendChild(e); }
window.fbAsyncInit = function() {
    FB.init({
        appId : '{{ app_settings.app_id }}',
        status     : true, // check login status
        cookie     : true, // enable cookies to allow the server to access the session
        oauth      : true, // enable OAuth 2.0
        xfbml      : true,  // parse XFBML
        channelUrl : '{{ channel_url|absolute_url:request }}'
    });
    {% if fix_20168 %}FB.UIServer.setLoadedNode = function (a, b){FB.UIServer._loadedNodes[a.id] = b; }{% endif %}
    {% if fix_19042 %}FB.UIServer.setActiveNode = function(a,b){FB.UIServer._active[a.id]=b;}{% endif %}
    {% if use_share %}appendScriptToFBRoot('//static.ak.fbcdn.net/connect.php/js/FB.Share');{% endif %}
    {% if canvas_height %}FB.Canvas.setSize({ width : {{ canvas_width|default_if_none:500 }}, height : {{ canvas_height }} });{% endif %}
};
appendScriptToFBRoot('//connect.facebook.net/en_US/all.js');
</script>'''

fb_script_template = template.Template(TEMPLATE_TEXT)
