# Generated by Django 4.0.8 on 2022-11-28 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('technologyoptions', '0008_alter_technologyoption_technology_component_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='technologyoption',
            name='technology_sub_component',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='technology_options', to='technologyoptions.technologysubcomponent'),
        ),
    ]
