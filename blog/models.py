from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.blocks import TextBlock, ListBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail import blocks

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import RichTextBlock
from wagtailcodeblock.blocks import CodeBlock
from app_blocks import app_blocks



class BlogPageTags(TaggedItemBase):
    content_object = ParentalKey(
        'blog.BlogDetail',
        related_name='tagged_items',
        on_delete=models.CASCADE,
    )


class BlogIndex(Page):
    template = "blog/blog_index.html"
    max_count = 1
    parent_page_types = ['home.HomePage']
    subpage_types = ['blog.BlogDetail']
    subtitle = models.CharField(max_length=100, blank=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('body'),
    ]


    def get_context(self, request):
        context = super().get_context(request)
        context['blog_pages'] = BlogDetail.objects.live().public().order_by('-first_published_at')
        # context['blog_pages'] = BlogDetail.objects.live().public().descendant_of(self)
        return context


class Author(models.Model):
    full_name = models.CharField(max_length=60)
    bio = models.TextField(max_length=500, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('full_name'),
        FieldPanel('bio'),
    ]

    def __str__(self):
        return self.full_name


class BlogDetail(Page):
    parent_page_types = ['blog.BlogIndex']
    subpage_types = []

    subtitle = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=210, blank=True, help_text='210 Characters, about 35 words.')
    tags = ClusterTaggableManager(through=BlogPageTags, blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    body = StreamField([
        ('divider', app_blocks.InfoBlock()),
        ('image', app_blocks.ImageBlock()),
        ('code', CodeBlock(label='Code', group='Coding')),
        ('text', app_blocks.TextBlock()),
        ('page', blocks.PageChooserBlock(required=False, group = 'Standalone Blocks')),
        ('doc', DocumentChooserBlock(group = 'Standalone Blocks')),
        ('author', SnippetChooserBlock('blog.Author')),
        ('faq', app_blocks.FAQListBlock()),
        ('call_to_action', app_blocks.CallToActionBlock()),
        ('carousel', app_blocks.CarouselBlock()),
        ('rich_text', RichTextBlock(
            features=['h2', 'h3', 'h4', 'bold', 'italic', 'link', 'document-link', 'image', 'ol', 'ul', 'blockquote',
                      'code'],
            group='Coding'
        )),
        ],
        use_json_field=True, blank=True, null=True)


    # body = RichTextField(
    #  blank=True,
    #  features=['h2', 'h3', 'h4', 'bold', 'italic', 'link', 'document-link', 'image', 'ol', 'ul', 'blockquote', 'code', 'strikethrough'])


    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('description'),
        FieldPanel('tags'),
        FieldPanel('image'),
        FieldPanel('body'),
    ]






