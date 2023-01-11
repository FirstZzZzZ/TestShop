# Generated by Django 4.1 on 2022-09-30 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store01', '0003_order_orderitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('id',), 'verbose_name': 'ข้อมูลใบสั่งซื้อ', 'verbose_name_plural': 'ข้อมูลใบสั่งซื้อ'},
        ),
        migrations.AlterModelOptions(
            name='orderitem',
            options={'ordering': ('order',), 'verbose_name': 'รายการสินค้าในใบสั่งซื้อ', 'verbose_name_plural': 'ข้อมูลสินค้าในใบสั่งซื้อ'},
        ),
        migrations.AddField(
            model_name='product01',
            name='หน่วย',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]