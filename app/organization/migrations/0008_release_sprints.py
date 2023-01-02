# Generated by Django 4.1.4 on 2023-01-02 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0007_remove_sprint_team_release_alter_sprint_release'),
    ]

    operations = [
        migrations.AddField(
            model_name='release',
            name='sprints',
            field=models.ManyToManyField(blank=True, related_name='sprints', to='organization.sprint'),
        ),
    ]