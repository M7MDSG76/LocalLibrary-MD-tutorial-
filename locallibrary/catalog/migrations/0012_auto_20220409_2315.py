# Generated by Django 3.1.7 on 2022-04-09 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_auto_20220406_1540'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'permissions': (('can_view_book_istances', 'can view book instances'),)},
        ),
    ]
