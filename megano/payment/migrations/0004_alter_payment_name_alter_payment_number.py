# Generated by Django 4.2 on 2025-03-24 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0003_alter_payment_name_alter_payment_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="name",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="payment",
            name="number",
            field=models.CharField(db_index=True, max_length=16),
        ),
    ]
