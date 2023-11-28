# Generated by Django 4.2.6 on 2023-10-31 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_mymodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChoiceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selected_choice', models.IntegerField(choices=[(1, 'Choice 1'), (2, 'Choice 2'), (3, 'Choice 3')])),
            ],
        ),
        migrations.DeleteModel(
            name='MyModel',
        ),
    ]
