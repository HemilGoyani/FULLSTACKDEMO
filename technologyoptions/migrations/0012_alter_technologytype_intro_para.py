# Generated by Django 4.0.8 on 2022-12-07 08:55

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('technologyoptions', '0011_alter_technologyoption_part_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='technologytype',
            name='intro_para',
            field=ckeditor.fields.RichTextField(null=True),
        ),
    ]
