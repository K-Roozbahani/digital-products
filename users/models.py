import random

from django.db import models

from django.utils.translation import ungettext_lazy as _
from django.core import validators
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, send_mail


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, phone_number, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()

        if not username:
            raise ValueError('the given username must be set')
        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number,
                          username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        if not extra_fields.get('no_password'):
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_user(self, username=None, phone_number=None, email=None, password=None, **extra_fields):
        if username is None:
            if email:
                username = email.split('@', 1)[0]
            if phone_number:
                username = random.choice('abcdefghijklmnopqrstuvwxyz') + str(phone_number)[-7:0]
            while User.objects.filter(username=username).exsists():
                username += str(random.randint(10, 99))

    def creat_superuser(self, username, phone_number, email, password, **extra_fields):
        return self._create_user(username, phone_number, email, password, True, True, **extra_fields)

    def get_by_phone_number(self, phone_number):
        return self.get(**{'phone_number': phone_number})


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=32, unique=True,
                                help_text=_('Required. 30 characters or fewer starting with a letter. Letters, digit'),
                                validators=[
                                    validators.RegexValidator(r'^[a-zA-Z][a-zA-Z0-9_\.]+$',
                                                              _('Enter a valid username start with a-z.'
                                                                'This value contain only letters, numbers'
                                                                'and underscore charactors.'), 'invalid'),
                                ],
                                error_messages={'unique': _("A user with that username already exists.")}
                                )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), unique=True, blank=True)
    phone_number = models.BigIntegerField(_("phone number"), unique=True, null=True, blank=True,
                                          validators=[
                                              validators.RegexValidator(r'^989[0-3,9]\d{8}$',
                                                                        'Enter a valid mobile number.'),
                                          ],
                                          error_messages={'unique': _('A user with this mobile number already exist.')}
                                          )
    is_staff = models.BooleanField(_('is staff'), default=False,
                                   help_text=_('Designates whether the user can log in to this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treat as active.'
                                                'unselect this instead of deleting accounts'))
    date_join = models.DateTimeField(_('date joined'), default=timezone.now())
    last_seen = models.DateTimeField(_('last seen date'), null=True)

    objects = BaseUserManager()

    USERNAME_FILD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, form_email=None, **kwargs):
        send_mail(subject, message, form_email, [self.email], **kwargs)

    @property
    def is_loggedin_user(self):
        return self.phone_number is not None or self.email is not None

    def save(self, *args, **kwargs):
        if self.email is not None and self.email.strip() == "":
            self.email = None
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick_name = models.CharField(_("nick name"), max_length=150, blank=True)
    avatar = models.ImageField(_('avatar'), blank=True)
    birthday = models.DateField(_("birthday"), null=True, blank=True)
    gender = models.NullBooleanField(_('gender'), help_text="famel is False, male is True, Null is unset.")
    province = models.ForeignKey(verbose_name=_('provice'), to='province', null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'user_profiles'
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    @property
    def get_first_name(self):
        return self.user.first_name

    @property
    def get_last_name(self):
        return self.user.last_name

    def get_nick_name(self):
        return self.nick_name if self.nick_name else self.user.username


class Device(models.Model):
    WEB = 1
    IOS = 2
    ANDROID = 3
    DEVICE_TYPE_CHOICES = (
        (WEB, 'web'),
        (IOS, 'ios'),
        (ANDROID, 'android'),
    )

    user = models.ForeignKey(User, related_name='device', on_delete=models.CASCADE)
    device_uuid = models.UUIDField(_('device uuid'), null=True)
    last_login = models.DateTimeField(_('last login date'), null=True)
    device_type = models.PositiveSmallIntegerField(choices=DEVICE_TYPE_CHOICES, default=ANDROID)
    device_os = models.CharField(_('device os'), max_length=50, blank=True)
    app_version = models.CharField(_('app version'), max_length=20, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_devises'
        verbose_name = 'device'
        verbose_name_plural = 'devices'
        unique_together = ('user', 'device_uuid')


class Province(models.Model):
    name = models.CharField(max_length=50)
    is_enable = models.BooleanField(default=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name