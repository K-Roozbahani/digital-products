# Generated by Django 3.2 on 2022-08-22 07:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subscriptions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Gateway',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('avatar', models.ImageField(blank=True, upload_to='gateway/', verbose_name='avatar')),
                ('is_enable', models.BooleanField(default=True, verbose_name='is_enable')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='update time')),
            ],
            options={
                'verbose_name': 'Gateway',
                'verbose_name_plural': 'Gateways',
                'db_table': 'gateways',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='price')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Void'), (10, 'Paid'), (20, 'Error'), (30, 'user Canceled'), (31, 'Refunded')], db_index=True, default=0, verbose_name='status')),
                ('device_uuid', models.CharField(blank=True, max_length=50, verbose_name='device uuid')),
                ('phone_number', models.BigIntegerField(db_index=True, validators=[utils.validators.PhoneNumberValidator], verbose_name='phone number')),
                ('consumed_code', models.PositiveSmallIntegerField(db_index=True, null=True, verbose_name='consumed reference code')),
                ('created_time', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created time')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='update time')),
                ('gateway', models.ManyToManyField(related_name='package', to='payments.Gateway')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='subscriptions.package')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
                'db_table': 'payments',
            },
        ),
    ]
