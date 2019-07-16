# Generated by Django 2.2.1 on 2019-05-30 03:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pageName', models.CharField(max_length=200, verbose_name='Page Name')),
                ('pageURL', models.CharField(default='https://google.com', max_length=2000, verbose_name='URL:')),
                ('startDate', models.DateTimeField(verbose_name='Start Date')),
                ('endDate', models.DateTimeField(verbose_name='End Date')),
            ],
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('name', models.CharField(default='Slide Show Name', max_length=150, verbose_name='Show Name')),
                ('id', models.IntegerField(default=0, primary_key=True, serialize=False, verbose_name='Show ID')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imageName', models.CharField(max_length=250, verbose_name='Image Name')),
                ('uploadDate', models.DateTimeField(default=1559187006.077497, verbose_name='Upload Date')),
                ('expireDate', models.DateTimeField(default=1559187007.0775223, verbose_name='Expire Date')),
                ('displayTime', models.IntegerField(default=15, verbose_name='Display Time')),
                ('order', models.IntegerField(default=0, verbose_name='Special Order')),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.Show')),
            ],
        ),
    ]