# Generated by Django 4.2.6 on 2023-11-24 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0040_ningen_management_date_de_naissance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ningen_management',
            name='Activite',
        ),
        migrations.AddField(
            model_name='ningen_management',
            name='Activite',
            field=models.CharField(blank=True, choices=[('Jumia TN', 'Jumia TN'), ('Jumia DZ', 'Jumia DZ'), ('KooL', 'KooL'), ('Arkan', 'Arkan')], max_length=50, null=True),
        ),
    ]