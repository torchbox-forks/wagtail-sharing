from django.urls import re_path
from django.conf import settings

from wagtail.urls import serve_pattern
from wagtail.urls import urlpatterns as wagtailcore_urlpatterns

from wagtailsharing.views import ServeView, TokenServeView


if getattr(settings, "WAGTAILSHARING_TOKENIZE_URL", False):
    share_path = getattr(settings, "WAGTAILSHARING_TOKEN_SHARE_PATH", "share")
    wagtailsharing_serve_path = re_path(
        rf"^{share_path}/([\w\.\-\_]+)/$",
        TokenServeView.as_view(),
        name="wagtail_serve",
    )
else:
    wagtailsharing_serve_path = re_path(
        serve_pattern, ServeView.as_view(), name="wagtail_serve"
    )

urlpatterns = [
    wagtailsharing_serve_path
    if urlpattern.name == "wagtail_serve"
    else urlpattern
    for urlpattern in wagtailcore_urlpatterns
]
