# Generated by Django 5.1.2 on 2024-11-19 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "accounts",
            "0003_remove_userlocation_user_user_location_user_username_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
