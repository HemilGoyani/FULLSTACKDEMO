# Generated by Django 4.0.8 on 2022-11-20 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotations', '0006_alter_quotationtechnologyoption_part_number'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='quotationtechnologyoption',
            unique_together={('quotation', 'part_number')},
        ),
    ]
