# Generated by Django 5.0.7 on 2024-07-18 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_subscription_amount_due_subscription_amount_paid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestlog',
            name='user',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
