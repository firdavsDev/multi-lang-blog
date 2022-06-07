import contextlib
import os

from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.timezone import now
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from PIL import Image
from unidecode import unidecode

from . import managers

# Create your models here.


def upload_image(instance, image_name):
    """ Make a path to the post image and change the name of the image to a post id

    Returns:
        [str]: [image path]
    """
    _ , extension = os.path.splitext(image_name)

    return f"post_images/{instance.title}.{extension}"


active_field_choices = [
    (True, _('Active')),
    (False, _('Inactive'))
]

class Language(models.Model):
    """ Language model

    Args:
        models (_type_): Django Model

    Returns:
        _type_: Save the language code and name
    """
    name = models.CharField(_('name'), max_length=25, null=True, blank=True)
    code = models.CharField(_('code'), max_length=5, null=True, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now_add=True)
    active = models.BooleanField(_('active'), default=True, choices=active_field_choices)

    class Meta:
        db_table = 'language'
        verbose_name = _('Language')
        verbose_name_plural = _('Language')
        ordering = ['-created_at']

    def __str__(self):
        return self.code


class Category(models.Model):
    name = models.CharField(_('name'), max_length=50)

    class Meta:
        db_table = 'category'
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('author'), related_name='blog_author')
    title = models.CharField(_('title'), max_length=100)
    content = RichTextField(_('content'))
    categories = models.ManyToManyField(Category, blank=True, verbose_name=_('categories'), related_name='categories')
    image = models.ImageField(_('image'), upload_to=upload_image, blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now_add=True)
    published_at = models.DateTimeField(_('published at'), default=now)
    views_count = models.IntegerField(_('views count'), null=True, blank=True, default=0, editable=False)
    language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name='posts_lang', verbose_name=_('language'), null=True, blank=True)
    active = models.BooleanField(_('active'), default=True, choices=active_field_choices)
    slug = models.SlugField(null=True, blank=True, unique=True, max_length=100, allow_unicode=True)
    #managers
    cus_objects = managers.BlogManager()
    objects = models.Manager()
    class Meta:
        db_table = 'blog'
        ordering = ('-published_at', )
        verbose_name = _('blog')
        verbose_name_plural = _('blogs')

    @property
    def get_self_or_post_lang(self):
        # check are language existin Language model
        try:
            lang = Language.objects.get(code=get_language())
        except Language.DoesNotExist: # if not retrun default title
            return self
        if self.language == lang:
            return self
        if post_lang := self.post_lang.filter(language=lang):
            return post_lang.get()

        return self

    def get_title(self):
        return self.get_self_or_post_lang.title

    def get_content(self):
        return self.get_self_or_post_lang.content

    def get_categories(self):
        return self.get_self_or_post_lang.categories

    def get_language_code(self):
        return self.get_self_or_post_lang.language.code



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

class PostLanguage(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='post_lang', verbose_name=_('post'),related_query_name='lang_post')
    title = models.CharField(_('title'), max_length=100)
    content = RichTextField(_('content'))
    categories = models.ManyToManyField(Category, blank=True, verbose_name=_('categories'))
    language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name='posts_lan', verbose_name=_('language'))
    active = models.BooleanField(_('active'), default=True, choices=active_field_choices)

    class Meta:
        db_table = 'post_language'
        managed = True
        verbose_name = 'PostLanguage'
        verbose_name_plural = 'PostLanguages'

    def __str__(self):
        return self.title
