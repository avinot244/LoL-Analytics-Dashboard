# Generated by Django 4.2.11 on 2024-04-12 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Draft', '0006_championdraftstats'),
    ]

    operations = [
        migrations.AddField(
            model_name='championdraftstats',
            name='role',
            field=models.CharField(default='Top', max_length=240, verbose_name='Role'),
            preserve_default=False,
        ),
    ]
