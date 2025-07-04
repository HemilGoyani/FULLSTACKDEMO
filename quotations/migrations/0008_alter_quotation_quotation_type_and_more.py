# Generated by Django 4.0.8 on 2022-11-23 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotations', '0007_alter_quotationtechnologyoption_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='quotation_type',
            field=models.CharField(choices=[('lump_sum', 'Lump Sum'), ('itemized', 'Itemized'), ('subscription_based', 'Subscription Based')], default='lump_sum', max_length=20),
        ),
        migrations.AlterField(
            model_name='quotationthirdpartyitem',
            name='item_name',
            field=models.CharField(max_length=80),
        ),
    ]
