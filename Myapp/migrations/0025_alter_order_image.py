# Generated by Django 4.0 on 2023-05-22 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0024_delete_orders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='image',
            field=models.ImageField(blank=True, upload_to='proof/'),
        ),
    ]