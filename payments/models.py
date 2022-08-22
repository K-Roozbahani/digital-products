from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.validators import validate_phone_number


class Gateway(models.Model):
    title = models.CharField(_("title"), max_length=50)
    description = models.TextField(_("description"), blank=True)
    avatar = models.ImageField(_("avatar"), blank=True, upload_to="gateway/")
    is_enable = models.BooleanField(_("is_enable"), default=True)
    created_time = models.DateTimeField(_("created time"), auto_now_add=True)
    update_time = models.DateTimeField(_("update time"), auto_now=True)

    class Meta:
        db_table = 'gateways'
        verbose_name = _('Gateway')
        verbose_name_plural = _("Gateways")


class Payment(models.Model):
    STATUS_VOID = 0
    STATUS_PAID = 10
    STATUS_ERROR = 20
    STATUS_CANCEL = 30
    STATUS_REFUNDED = 31
    STATUS_CHOICES = (
        (STATUS_VOID, _('Void')),
        (STATUS_PAID, _('Paid')),
        (STATUS_ERROR, _('Error')),
        (STATUS_CANCEL, _('user Canceled')),
        (STATUS_REFUNDED, _('Refunded')),
    )

    user = models.ForeignKey('users.User', related_name='%(class)s', on_delete=models.CASCADE)
    package = models.ForeignKey('subscriptions.Package', related_name='%(class)s', on_delete=models.CASCADE)
    gateway = models.ManyToManyField('Gateway', related_name='package')
    price = models.PositiveIntegerField(_('price'), default=0)
    status = models.PositiveSmallIntegerField(_('status'), choices=STATUS_CHOICES, default=STATUS_VOID, db_index=True)
    device_uuid = models.CharField(_('device uuid'), max_length=50, blank=True)
    phone_number = models.BigIntegerField(_('phone number'), validators=[validate_phone_number], db_index=True)
    consumed_code = models.PositiveSmallIntegerField(_('consumed reference code'), null=True, db_index=True)
    created_time = models.DateTimeField(_("created time"), auto_now_add=True, db_index=True)
    update_time = models.DateTimeField(_("update time"), auto_now=True)

    class Meta:
        db_table = 'payments'
        verbose_name = _('Payment')
        verbose_name_plural = _("Payments")