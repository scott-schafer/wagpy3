from django.db import models
from django.http import JsonResponse
from django.template.defaultfilters import slugify
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.blocks import TextBlock, ListBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail import blocks

from wagtail.models import Page, Orderable
# from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.fields import StreamField
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.blocks import RichTextBlock
from wagtailcodeblock.blocks import CodeBlock
from app_blocks import app_blocks
from wagtail.contrib.routable_page.models import RoutablePageMixin, path, re_path


class BlogPageTags(TaggedItemBase):
    content_object = ParentalKey(
        'blog.BlogDetail',
        related_name='tagged_items',
        on_delete=models.CASCADE,
    )


class BlogIndex(RoutablePageMixin, Page):
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

    ##### All Blog Posts #####
    @path('all/', name='all')
    def all_blog_posts(self, request):
        posts = BlogDetail.objects.live().public().order_by('-first_published_at')

        return self.render(
            request,
            context_overrides={
                'posts': posts,
            },
            template='blog/posts_all.html'
        )

    #### Tag Posts ####
    @path('tag/<str:tag>/', name='tag')
    def blog_post_tags(self, request, tag=None):
        # posts = BlogDetail.objects.live().public().filter(tags__name=tag).order_by('-first_published_at')
        posts = BlogDetail.objects.live().public().filter(tags__name=tag)

        return self.render(
            request,
            context_overrides={
                'posts': posts,
                'tag': tag,
            },
            template='blog/posts_by_tag.html'
        )


    def get_context(self, request):
        context = super().get_context(request)
        context['blog_pages'] = BlogDetail.objects.live().public().order_by('-first_published_at')[:6]
        context["authors"] = BlogDetail.objects.all()
        # context['blog_pages'] = BlogDetail.objects.live().public().descendant_of(self)
        return context


class BlogAuthorOrderable(Orderable):
    page = ParentalKey('blog.BlogDetail', related_name='blog_authors')
    author = models.ForeignKey("blog.Author", on_delete=models.CASCADE)

    panels = [
        FieldPanel("author"),
    ]




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
        ('article_section', app_blocks.ArticleSectionBlock()),
        ('divider', app_blocks.InfoBlock()),
        ('image', app_blocks.ImageBlock()),
        ('code', CodeBlock(label='Code', group='Coding')),
        ('text', app_blocks.TextBlock()),
        ('page', blocks.PageChooserBlock(required=False, group = 'Standalone Blocks')),
        ('doc', DocumentChooserBlock(group = 'Standalone Blocks')),
        # ('author', SnippetChooserBlock('blog.Author')),
        ('faq', app_blocks.FAQListBlock()),
        ('call_to_action', app_blocks.CallToActionBlock()),
        ('carousel', app_blocks.CarouselBlock()),
        ('rich_text', RichTextBlock(
            features=['h2', 'h3', 'h4', 'bold', 'italic', 'link', 'document-link', 'image', 'ol', 'ul', 'blockquote', 'code'],
            group='Coding'
        )),
        ],
        use_json_field=True, blank=True, null=True)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # context["authors"] = blog_authors.all()
        # Create a list of tuples with (heading, anchor_id)
        sections = []
        for block in self.body:
            if block.block_type == 'article_section':
                # Get the value from the header field
                heading_text = block.value.get('header')
                # Slugify the heading to create a clean anchor ID
                anchor_id = slugify(heading_text)
                sections.append({
                    'heading': heading_text,
                    'anchor_id': anchor_id,
                })
        context['toc_sections'] = sections
        return context



    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('description'),
        MultiFieldPanel(
            [
                InlinePanel("blog_authors", label="Authors", min_num=1, max_num=2),
            ],
            heading='Authors',
        ),
        FieldPanel('tags'),
        FieldPanel('image'),
        FieldPanel('body'),
    ]






