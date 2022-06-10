from django.db import models
from django.utils.translation import gettext_lazy as _

class BaseModel(models.Model):
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, null=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, null=True)

    class Meta:
        abstract = True
