from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.validators import validate_sku


class Package(models.Model):
    title = models.CharField(_('title'), max_length=50),
    sku = models.CharField(_('stock keeping unit'), max_length=20, validators=[validate_sku], db_index=True)
    description = models.TextField(_('description'), blank=True)
    avatar = models.ImageField(_('avatar'), blank=True, upload_to='packages/')
    is_enable = models.BooleanField(_('is enable'), default=True)
    price = models.PositiveIntegerField(_('price'))
    duration = models.DurationField(_('duration'), blank=True, null=True)
    # gateway = models.ManyToManyField('payments.Gateway')
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    update_time = models.DateTimeField(_('update time'), auto_now=True)

    class Meta:
        db_table = _('packages')
        verbose_name = _('package')
        verbose_name_plural = _('packages')

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey('users.User', related_name='%(class)s', on_delete=models.CASCADE)
    package = models.ForeignKey('Package', related_name='%(class)s', on_delete=models.CASCADE)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    expire_time = models.DateTimeField(_('expire time'), null=True, blank=True)

    class Meta:
        db_table = 'subscriptions'
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')
