from asyncio.log import logger
from django.db.models import Count, Q, manager,F, Value,ExpressionWrapper
from django.db.models.functions import Coalesce
from django.utils.timezone import now
from django.db.models import CharField
from django.shortcuts import get_object_or_404


# QuerySet TODO: must optimiziton
class BlogQuerySet(manager.QuerySet):

    # get blog detail with translate fields
    def get_translate_blog_detail_queryset(self, blog_pk:int, queries:dict):
        try:
            from .models import PostLanguage
            #update views_count every time user visit blog
            self.filter(pk=blog_pk).update(
                views_count=F("views_count") + 1
            )
            lang = queries.get("lang")
            queryset_blog = queryset = self.filter(pk=blog_pk, lang_post__language=lang)
            if queryset_blog.exists():
                post_lang =get_object_or_404(PostLanguage, post_id=blog_pk, language=lang)
                queryset = queryset_blog.annotate(
                    title_translate=ExpressionWrapper(Value(post_lang.title), output_field=CharField()),
                    content_translate=ExpressionWrapper(Value(post_lang.content), output_field=CharField()),
                )
            return queryset
        except Exception as e:
            logger.error(e)

    # get translate blog list TODO : must optimiziton. Bug - return one queryset. not many querysets I try to find solution for this little bug :)
    def get_translate_blog_list_queryset(self, queries:dict):
        from .models import PostLanguage
        try:
            lang = queries.get("lang")
            for i in self:
                queryset = self.filter(pk=i.pk)
                post_lang = PostLanguage.objects.filter(post_id=i.id, language=lang).last() # dont get 2!
                if post_lang is not None:
                    queryset = queryset.annotate(
                    title_translate = ExpressionWrapper(Value(post_lang.title), output_field=CharField()),
                    content_translate = ExpressionWrapper(Value(post_lang.content), output_field=CharField()),
                )
                else:
                    queryset = queryset.annotate(
                    title_translate = ExpressionWrapper(Value(i.title), output_field=CharField()),
                    content_translate = ExpressionWrapper(Value(i.content), output_field=CharField()),
                )
            return queryset
        except Exception as e:
            logger.error(e)

#Manager custom
class BlogManager(manager.Manager):

    def get_queryset(self, *args, **kwargs):
        return BlogQuerySet(self.model, using=self._db, hints=self._hints)

    #get list blogs with translate field
    def get_translate_blog_list(self, queries:dict):
        return self.get_queryset().get_translate_blog_list_queryset(queries)

    #get blog detail with translate field
    def get_translate_blog_detail(self, blog_pk, queries:dict):
        return self.get_queryset().get_translate_blog_detail_queryset(blog_pk, queries)

    #all()
    def get_published_blogs(self):
        return self.get_queryset().filter(Q(active=True) & Q(published_at__lte=now()))
