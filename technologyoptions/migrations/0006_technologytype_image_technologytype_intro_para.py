# Generated by Django 4.1.2 on 2022-11-17 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("technologyoptions", "0005_technologyoption_technologysubcomponent_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="technologytype",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="TechnologyTypeImages/"
            ),
        ),
        migrations.AddField(
            model_name="technologytype",
            name="intro_para",
            field=models.TextField(null=True),
        ),
    ]
