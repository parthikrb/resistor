# Generated by Django 4.1.4 on 2023-01-02 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_organization_invitation_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sprint',
            name='team',
        ),
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='releases', to='organization.team')),
            ],
        ),
        migrations.AlterField(
            model_name='sprint',
            name='release',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='release', to='organization.release'),
        ),
    ]
