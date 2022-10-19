from django.db import models


class Expert(models.Model):
    SITE_CHITGHAR = 1
    SITE_ZARAFSHAN = 2
    SITE_SEMNAN = 3
    SITES = ((SITE_SEMNAN, 'site Chitghar'), (SITE_ZARAFSHAN, 'site Zarafshan'), (SITE_SEMNAN, 'site Semnan'))
    user = models.OneToOneField('User', models.CASCADE)
    personal_id = models.IntegerField(unique=True)
    date_employment = models.DateField("date employment", null=True, blank=True)
    site = models.SmallIntegerField('site', default=1, choices=SITES)

