# Generated by Django 4.2.6 on 2023-10-27 15:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_rename_mail_client_valide_winbacktable_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Winback2',
            fields=[
                ('Date_de_traitement', models.DateField(blank=True, null=True)),
                ('GSM', models.IntegerField(primary_key=True, serialize=False)),
                ('VOUCHER_ELIGIBILITY', models.IntegerField(blank=True, null=True)),
                ('CUSTOMER_ID', models.CharField(max_length=20)),
                ('CLIENT_JOIGNABLE', models.TextField(blank=True, null=True)),
                ('RAISON_DE_NON_COMMANDE', models.TextField(blank=True, null=True)),
                ('FEEDBACK_POST_VOUCHER', models.TextField(blank=True, null=True)),
                ('COMMENTAIRE', models.TextField(blank=True, null=True)),
                ('Voucher_code', models.CharField(max_length=20)),
                ('Email', models.CharField(blank=True, max_length=100, null=True)),
                ('CLIENT_JOIGNABLE2', models.TextField(blank=True, null=True)),
                ('done', models.BooleanField(default=False)),
                ('locked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Winback2Results',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('GSM', models.IntegerField(blank=True, null=True)),
                ('joignabilite', models.CharField(choices=[('Injoignable 1ère tentative', 'Injoignable 1ère tentative'), ('Injoignable 2éme tentative', 'Injoignable 2éme tentative'), ('Injoignable', 'Injoignable'), ('Joignable', 'Joignable')], max_length=50)),
                ('feedback_interet_voucher', models.CharField(choices=[('Positif', 'Positif'), ('Négatif', 'Négatif')], max_length=10)),
                ('raison_non_interesse', models.TextField()),
                ('commentaire', models.TextField()),
                ('treated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]