# Generated by Django 2.2.1 on 2019-08-20 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0008_auto_20190820_0700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='order',
            field=models.CharField(default='-1', max_length=255, verbose_name='Special Order'),
        ),
    ]
