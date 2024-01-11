from importlib import reload
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import re_path

from wagtail import urls as wagtail_core_urls

import wagtailsharing.urls


class TestUrlPatterns(TestCase):
    def setUp(self):
        def test_view():
            pass  # pragma: no cover

        root_patterns = [
            re_path(r"^foo/$", re_path, name="foo"),
            re_path(r"^((?:[\w\-]+/)*)$", re_path, name="wagtail_serve"),
            re_path(r"^bar/$", re_path, name="bar"),
        ]

        self.patcher = patch.object(
            wagtail_core_urls, "urlpatterns", root_patterns
        )
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

        reload(wagtailsharing.urls)
        self.urlpatterns = wagtailsharing.urls.urlpatterns

    def test_leaves_previous_urls_alone(self):
        self.assertEqual(self.urlpatterns[0].name, "foo")

    def test_replaces_wagtail_serve(self):
        from django import VERSION as DJANGO_VERSION

        self.assertEqual(self.urlpatterns[1].name, "wagtail_serve")

        if DJANGO_VERSION >= (4, 1):
            self.assertEqual(self.urlpatterns[1].callback.__name__, "view")
        else:
            self.assertEqual(
                self.urlpatterns[1].callback.__name__, "ServeView"
            )

    def test_leaves_later_urls_alone(self):
        self.assertEqual(self.urlpatterns[2].name, "bar")


@override_settings(WAGTAILSHARING_TOKENIZE_URL=True)
class TestUrlPatternsTokenized(TestCase):
    def setUp(self):
        def test_view():
            pass  # pragma: no cover

        root_patterns = [
            re_path(r"^foo/$", re_path, name="foo"),
            re_path(r"^bar/$", re_path, name="bar"),
            re_path(r"^baz/$", re_path, name="baz"),
        ]

        self.patcher = patch.object(
            wagtail_core_urls, "urlpatterns", root_patterns
        )
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

        reload(wagtailsharing.urls)
        self.urlpatterns = wagtailsharing.urls.urlpatterns

    def test_leaves_previous_urls_alone(self):
        self.assertEqual(self.urlpatterns[0].name, "foo")
        self.assertEqual(self.urlpatterns[1].name, "bar")

    def test_adds_wagtail_serve(self):
        # The TokenServeView is added to the end of the urlpatterns
        from django import VERSION as DJANGO_VERSION

        self.assertEqual(self.urlpatterns[-1].name, "wagtail_serve")

        if DJANGO_VERSION >= (4, 1):
            self.assertEqual(self.urlpatterns[-1].callback.__name__, "view")
        else:
            self.assertEqual(
                self.urlpatterns[-1].callback.__name__, "TokenServeView"
            )
