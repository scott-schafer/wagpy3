from django.db import models

from wagtail.models import Page
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel


class HomePage(Page):
    template = "home/home_page.html"
    max_count = 1

    sub_title = models.CharField(max_length=255, blank=True, null=True)


    content_panels = Page.content_panels + [
        FieldPanel("sub_title"),

    ]

    def get_context(self, request, *args, **kwargs):
        """Adding products information to page"""
        context = super().get_context(request, *args, **kwargs)
        # context['custom_data'] = 'This is a custom data'

        return context

