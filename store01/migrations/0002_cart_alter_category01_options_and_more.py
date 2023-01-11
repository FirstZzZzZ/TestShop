# Generated by Django 4.1 on 2022-08-26 04:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_id', models.CharField(blank=True, max_length=255)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'ตะกร้าสินค้า',
                'verbose_name_plural': 'ข้อมูลตะกร้าสินค้า',
                'db_table': 'cart',
                'ordering': ('date_added',),
            },
        ),
        migrations.AlterModelOptions(
            name='category01',
            options={'ordering': ('name',), 'verbose_name': 'ประเภทสินค้า', 'verbose_name_plural': 'ข้อมูลประเภทสินค้า'},
        ),
        migrations.AlterModelOptions(
            name='product01',
            options={'ordering': ('name',), 'verbose_name': 'สินค้า', 'verbose_name_plural': 'ข้อมูลสินค้า'},
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store01.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store01.product01')),
            ],
            options={
                'verbose_name': 'รายการสินค้าในตะกร้า',
                'verbose_name_plural': 'ข้อมูลรายการสินค้าในตะกร้า',
                'db_table': 'cartItem',
            },
        ),
    ]
