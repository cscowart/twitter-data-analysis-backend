# Generated by Django 3.0.4 on 2020-03-26 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_graphic_crud', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='graphic',
            old_name='date_create',
            new_name='date_created',
        ),
    ]