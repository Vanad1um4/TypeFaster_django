# Generated by Django 4.1.4 on 2022-12-22 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_account_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='user_id',
        ),
    ]
