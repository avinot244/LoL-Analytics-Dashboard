# Generated by Django 4.2.11 on 2024-04-07 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Draft', '0002_draftplayerpick'),
    ]

    operations = [
        migrations.AddField(
            model_name='draftpickorder',
            name='tournament',
            field=models.CharField(default='test', max_length=240, verbose_name='Tournament'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='draftplayerpick',
            name='tournament',
            field=models.CharField(default='test', max_length=240, verbose_name='Tournament'),
            preserve_default=False,
        ),
    ]