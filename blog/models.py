from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class BlogIndex(Page):
    template = "blog/blog_index.html"
    parent_page_types = ['home.HomePage']
    subpage_types = ['blog.BlogDetail']
    max_count = 1

    subtitle = models.CharField(max_length=100, blank=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('body'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['blogpages'] = BlogDetail.objects.live().public().order_by('-first_published_at')
        return context


class BlogDetail(Page):
    parent_page_types = ['blog.BlogIndex']
    subpage_types = []

    subtitle = models.CharField(max_length=100, blank=True)
    body = RichTextField(
     blank=True,
     features=['h2', 'h3', 'h4', 'bold', 'italic', 'link', 'document-link', 'image', 'ol', 'ul',
               'blockquote', 'code', 'strikethrough']
    )


    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('body'),
    ]






