# Generated by Django 4.2.6 on 2023-11-24 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0037_rename_lob_bo_activite_skills_bo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ningen_staff',
            name='Type_de_contrat',
            field=models.CharField(choices=[('CDI', 'CDI'), ('CIVP', 'CIVP'), ('EL Karama', 'EL Karama'), ('Stage', 'Stage')], max_length=10),
        ),
    ]
