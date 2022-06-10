import contextlib
import os

from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from PIL import Image
from unidecode import unidecode

from . import managers
from .basemodels import BaseModel
# Create your models here.


def upload_image(instance, image_name):
    """ Make a path to the post image and change the name of the image to a post id

    Returns:
        [str]: [image path]
    """
    _ , extension = os.path.splitext(image_name)

    return f"post_images/{instance.title}.{extension}"

#choices for the post status
active_field_choices = [
    (True, _('Active')),
    (False, _('Inactive'))
]


class Category(models.Model):
    name = models.CharField(_('name'), max_length=50)

    class Meta:
        db_table = 'category'
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name

class Blog(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('author'), related_name='blog_author')
    title = models.CharField(_('title'), max_length=100)
    content = RichTextField(_('content'))
    categories = models.ManyToManyField(Category, blank=True, verbose_name=_('categories'), related_name='categories')
    image = models.ImageField(_('image'), upload_to=upload_image, blank=True, null=True)
    published_at = models.DateTimeField(_('published at'), default=now)
    views_count = models.IntegerField(_('views count'), null=True, blank=True, default=0, editable=False)
    active = models.BooleanField(_('active'), default=True, choices=active_field_choices)
    slug = models.SlugField(null=True, blank=True, unique=True, max_length=100, allow_unicode=True)
    #managers
    custom_objects = managers.BlogManager()
    objects = models.Manager()
    class Meta:
        db_table = 'blog'
        ordering = ('-published_at', )
        verbose_name = _('blog')
        verbose_name_plural = _('blogs')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
            Overwrite save mehtod to make a slug to post, rename a image and resize a big image
        """

        # Make a post Slug
        if not self.pk:
            slug = slugify(unidecode(f"{self.title}"))

            slug_count = len(Blog.objects.filter(slug=slug))
            if slug_count > 0:
                slug = f"{slug}-{slug_count}"

            self.slug = slug

        # Handle problem in upload_image function  (pk not generator yet)
        # if self.pk is None:
        #     post_image = self.image
        #     self.image = None
        #     super().save(*args, **kwargs)
        #     self.image = post_image

        super().save(*args, **kwargs)

        # image resize
        if self.image:
            with contextlib.suppress(Exception):
                img = Image.open(self.image.path)
                if img.width > 800 or img.height > 800:
                    img.thumbnail( (800, 800) )
                    img.save(self.image.path)

class PostLanguage(BaseModel):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='post_lang', verbose_name=_('post'), related_query_name='lang_post')
    LANGUAGE_TYPES = (
        ('en', 'English'),
        ('uz', 'Uzbek'),
        ('ru', 'Russian'),
    )
    language = models.CharField(max_length=2, choices=LANGUAGE_TYPES, default='en')
    title = models.CharField(_('title'), max_length=100)
    content = RichTextField(_('content'))
    active = models.BooleanField(_('active'), default=True, choices=active_field_choices)

    class Meta:
        db_table = 'post_language'
        managed = True
        verbose_name = 'PostLanguage'
        verbose_name_plural = 'PostLanguages'

    def __str__(self):
        return self.title
