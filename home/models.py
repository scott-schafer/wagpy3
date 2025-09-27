from django.db import models

from wagtail.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel

class SitePage(Page):
    sub_title = models.CharField(max_length=255)

    content_panels = Page.content_panels + [
        FieldPanel('sub_title'),
    ]


class HomePage(Page):
    template = "home/home_page.html"

    sub_title = models.CharField(max_length=255, blank=True, null=True)







    content_panels = Page.content_panels + [
        FieldPanel("sub_title"),
        MultiFieldPanel([
            InlinePanel("hero_carousel", max_num=5, min_num=1,
                        label="Slider Panel"),
        ], heading="Slider Carousel Panels"),
    ]

    def get_context(self, request, *args, **kwargs):
        """Adding products information to page"""
        context = super().get_context(request, *args, **kwargs)
        context['custom_data'] = 'This is a custom data'

        return context





class HeroPageCarousel(Orderable):
    """Hero Slider Text Up To 5 Slides"""

    template = "home/home_page.html"
    page = ParentalKey("home.HomePage", related_name="hero_carousel")
    slider_title = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Slider Title Text Goes Here"
    )

    slider_sub_title = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Slider Sub Title Text Goes Here"
    )

    panels = [
        FieldPanel("slider_title"),
        FieldPanel("slider_sub_title"),

    ]
