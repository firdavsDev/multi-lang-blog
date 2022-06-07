from django.db.models import Count, Q, manager
from django.db.models.functions import Coalesce
from django.utils.timezone import now


class BlogManager(manager.Manager):
    def with_counts(self):
        return self.annotate(
            num_views=Coalesce(Count('views_count'), 0)
        )
    def get_queryset(self):
        return super().get_queryset().filter(Q(active=True) & Q(published_at__lte=now()))
