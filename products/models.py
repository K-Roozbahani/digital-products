from django.db import models
from django.utils.translation import ugettext_lazy as _

class Category(models.Model):
    parent = models.ForeignKey("self", verbose_name="parent", blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(_("title"), max_length=50)
    description = models.TextField(_("description"), blank=True)
    avatar = models.ImageField(_("avatar"), blank=True, upload_to="category/")
    is_enable = models.BooleanField(_("is_enable"), default=True)
    created_time = models.DateTimeField(_("created time"), auto_now_add=True)
    update_time = models.DateTimeField(_("update time"), auto_now=True)

    class Meta:
        db_table = 'categories'
        verbose_name = _('Category')
        verbose_name_plural = _("Categories")

class Product(models.Model):
    title = models.CharField(_("title"), max_length=50)
    description = models.TextField(_("description"), blank=True)
    avatar = models.ImageField(_("avatar"), blank=True, upload_to="category/")
    is_enable = models.BooleanField(_("is enable"), default=True)
    categories = models.ManyToManyField('Category', verbose_name=_("categories"), blank=True)
    created_time = models.DateTimeField(_("created time"), auto_now_add=True)
    update_time = models.DateTimeField(_("update time"), auto_now=True)

    class Meta:
        db_table = 'product'
        verbose_name = _('product')
        verbose_name_plural = _("products")


class File(models.Model):
    product = models.ForeignKey("Product", verbose_name=_('product'), on_delete=models.CASCADE)
    title = models.CharField(_("title"), max_length=50)
    is_enable = models.BooleanField(_("is_enable"), default=True)
    created_time = models.DateTimeField(_("created time"), auto_now_add=True)
    update_time = models.DateTimeField(_("update time"), auto_now=True)

    class Meta:
        db_table = 'files'
        verbose_name = _('file')
        verbose_name_plural = _("files")