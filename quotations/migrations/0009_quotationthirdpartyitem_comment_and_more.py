# Generated by Django 4.0.8 on 2022-11-23 11:13

from decimal import Decimal
from django.db import migrations, models
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('quotations', '0008_alter_quotation_quotation_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotationthirdpartyitem',
            name='comment',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='quotationthirdpartyitem',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quotationthirdpartyitem',
            name='ps_cost',
            field=djmoney.models.fields.MoneyField(currency_choices=(('USD', 'USD'),), decimal_places=2, default=Decimal('0'), default_currency='USD', max_digits=10),
        ),
        migrations.AddField(
            model_name='quotationthirdpartyitem',
            name='ps_cost_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('USD', 'USD')], default='USD', editable=False, max_length=3),
        ),
        migrations.AddField(
            model_name='thirdpartyitem',
            name='comment',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='thirdpartyitem',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='thirdpartyitem',
            name='ps_cost',
            field=djmoney.models.fields.MoneyField(currency_choices=(('USD', 'USD'),), decimal_places=2, default=Decimal('0'), default_currency='USD', max_digits=10),
        ),
        migrations.AddField(
            model_name='thirdpartyitem',
            name='ps_cost_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('USD', 'USD')], default='USD', editable=False, max_length=3),
        ),
        migrations.AddField(
            model_name='thirdpartyitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='quotationthirdpartyitem',
            name='unit',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='thirdpartyitem',
            name='unit',
            field=models.CharField(max_length=40),
        ),
    ]
