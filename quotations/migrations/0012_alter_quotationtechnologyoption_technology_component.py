# Generated by Django 4.0.8 on 2022-11-25 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotations', '0011_merge_20221124_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotationtechnologyoption',
            name='technology_component',
            field=models.CharField(choices=[('1-Hardware', 'Hardware'), ('2-Setup', 'Setup'), ('3-Training', 'Training'), ('4-Software', 'Software'), ('5-Ongoing', 'OnGoing')], max_length=255),
        ),
    ]
