# Generated by Django 4.1.5 on 2023-01-02 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0012_employeesignup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeesignup',
            name='organization',
        ),
        migrations.AddField(
            model_name='employeesignup',
            name='invitation_code',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
