# Generated by Django 4.2.6 on 2023-11-13 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0025_alter_ningen_staff_lob_actuelle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ningen_staff',
            name='CIN',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ningen_staff',
            name='N1',
            field=models.CharField(choices=[('Mehrzia Hannafi', 'Mehrzia Hannafi'), ('Ines Dridi', 'Ines Dridi')], max_length=25),
        ),
    ]
