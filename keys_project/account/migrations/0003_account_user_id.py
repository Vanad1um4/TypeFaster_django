# Generated by Django 4.1.4 on 2022-12-22 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_rename_profile_account_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='user_id',
            field=models.PositiveSmallIntegerField(blank=True, default=0),
            preserve_default=False,
        ),
    ]
