# Generated by Django 4.2.7 on 2023-11-29 05:08

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0005_alter_review_unique_together"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="project",
            options={"ordering": ["-vote_ratio", "-vote_total", "title"]},
        ),
    ]
