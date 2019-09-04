# Generated by Django 2.2.1 on 2019-09-02 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0010_auto_20190902_0626'),
    ]

    operations = [
        migrations.RenameField(
            model_name='screens',
            old_name='HostIP',
            new_name='hostIP',
        ),
        migrations.AddField(
            model_name='screens',
            name='height',
            field=models.IntegerField(default=1080, verbose_name='Screen Height'),
        ),
        migrations.AddField(
            model_name='screens',
            name='width',
            field=models.IntegerField(default=1920, verbose_name='Screen Width'),
        ),
    ]
