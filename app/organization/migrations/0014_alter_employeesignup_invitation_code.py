# Generated by Django 4.1.5 on 2023-01-02 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0013_remove_employeesignup_organization_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeesignup',
            name='invitation_code',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
