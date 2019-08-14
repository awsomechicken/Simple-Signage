# Generated by Django 2.2.1 on 2019-07-17 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='Image Id')),
                ('imageName', models.CharField(max_length=250, verbose_name='Image Name')),
                ('uploadDate', models.DateTimeField(verbose_name='Upload Date')),
                ('startDate', models.DateTimeField(verbose_name='Start Date')),
                ('expireDate', models.DateTimeField(verbose_name='Expire Date')),
                ('displayTime', models.IntegerField(default=15, verbose_name='Display Time (Seconds)')),
                ('order', models.IntegerField(default=0, verbose_name='Special Order')),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.Show')),
            ],
        ),
        migrations.RemoveField(
            model_name='file',
            name='show',
        ),
        migrations.DeleteModel(
            name='Page',
        ),
        migrations.DeleteModel(
            name='File',
        ),
    ]