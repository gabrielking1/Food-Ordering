# Generated by Django 4.0 on 2023-05-22 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0022_alter_payment_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='image',
            field=models.ImageField(default='/proof/succ.jpg', upload_to='proof/'),
        ),
    ]
