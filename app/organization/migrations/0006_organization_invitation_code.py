# Generated by Django 4.1.4 on 2022-12-30 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_organization_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='invitation_code',
            field=models.CharField(default=1, max_length=8, unique=False),
            preserve_default=False,
        ),
    ]
