# Generated by Django 5.0.6 on 2024-07-22 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Draft', '0013_championbanstats'),
    ]

    operations = [
        migrations.AddField(
            model_name='championdraftstats',
            name='draftPresence',
            field=models.FloatField(default=0, verbose_name='DraftPresence'),
            preserve_default=False,
        ),
    ]
