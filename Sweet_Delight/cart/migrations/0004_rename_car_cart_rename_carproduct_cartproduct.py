# Generated by Django 4.0.3 on 2022-04-10 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_foodmenu_digital'),
        ('cart', '0003_rename_cart_car_rename_cartproduct_carproduct'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Car',
            new_name='Cart',
        ),
        migrations.RenameModel(
            old_name='CarProduct',
            new_name='CartProduct',
        ),
    ]