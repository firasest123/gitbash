# Generated by Django 4.2.6 on 2023-11-07 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_rename_name_clchoicemodel_cl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clchoicemodel',
            name='CL',
        ),
        migrations.AddField(
            model_name='clchoicemodel',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='ningen_staff',
            name='CL',
            field=models.ManyToManyField(choices=[('', ''), ('Khaoula Werghi', 'Khaoula Werghi'), ('Anis Hedhli', 'Anis Hedhli'), ('Ishrak Ben Rjab', 'Ishrak Ben Rjab'), ('Molka CHOUIKA', 'Molka CHOUIKA'), ('Mohamed Amine ZOUAOUI', 'Mohamed Amine ZOUAOUI')], to='myapp.clchoicemodel'),
        ),
    ]
