# Generated by Django 4.2.7 on 2023-11-28 15:03

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_profile_location_skill"),
        ("projects", "0004_alter_project_options_review_owner_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="review",
            unique_together={("owner", "project")},
        ),
    ]
