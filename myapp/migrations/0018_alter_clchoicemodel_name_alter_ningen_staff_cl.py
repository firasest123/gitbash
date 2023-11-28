# Generated by Django 4.2.6 on 2023-11-07 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_alter_ningen_staff_niveau_d_etude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clchoicemodel',
            name='name',
            field=models.CharField(blank=True, choices=[('', ''), ('Khaoula Werghi', 'Khaoula Werghi'), ('Anis Hedhli', 'Anis Hedhli'), ('Ishrak Ben Rjab', 'Ishrak Ben Rjab'), ('Molka CHOUIKA', 'Molka CHOUIKA'), ('Mohamed Amine ZOUAOUI', 'Mohamed Amine ZOUAOUI')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='ningen_staff',
            name='CL',
            field=models.ManyToManyField(to='myapp.clchoicemodel'),
        ),
    ]