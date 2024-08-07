# Generated by Django 4.2.11 on 2024-04-07 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Draft', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DraftPlayerPick',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=240, verbose_name='Date')),
                ('patch', models.CharField(max_length=240, verbose_name='Patch')),
                ('seriesId', models.IntegerField(verbose_name='SeriesId')),
                ('sumonnerName', models.CharField(max_length=240, verbose_name='SumonnerName')),
                ('championName', models.CharField(max_length=240, verbose_name='ChampionName')),
                ('role', models.CharField(max_length=240, verbose_name='Role')),
            ],
        ),
    ]
