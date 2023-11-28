from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import VisitedLink, HorairePreference
from django.contrib.auth import get_user_model


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Email'})


class CustomLoginForm(AuthenticationForm):
    class Meta:
        model = get_user_model()


class VisitedLinkForm(forms.ModelForm):
    class Meta:
        model = VisitedLink
        fields = ['name', 'url']


class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'btn btn-primary action-button date-input'}), required=True)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'btn btn-primary action-button date-input'}), required=True)



class ChangePasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    ancien_mot_de_passe = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Old Password'}))
    nouveau_mot_de_passe_1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}))
    nouveau_mot_de_passe_2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'}))



class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='Upload CSV File')



class CampagneForm(forms.Form):
    CLIENT_JOIGNABLE_CHOICES = [
        ("Injoignable 1ère tentative", "Injoignable 1ère tentative"),
        ("Injoignable 2éme tentative", "Injoignable 2éme tentative"),
        ("Injoignable", "Injoignable"),
        ("Joignable", "Joignable"),
    ]

    RAISON_DE_NON_COMMANDE_CHOICES = [
        ("N'était pas intéressé", "N'était pas intéressé"),
        ("Problème avec l'application", "Problème avec l'application"),
        ("Problème OTP", "Problème OTP"),
        ("Mauvaise expérience restaurant", "Mauvaise expérience restaurant"),
        ("Mauvaise expérience livraison", "Mauvaise expérience livraison"),
        ("Mauvaise expérience Jumia", "Mauvaise expérience Jumia"),
        ("Concurrence", "Concurrence"),
        ("Zone non couverte", "Zone non couverte"),
    ]

    FEEDBACK_POST_VOUCHER_CHOICES = [
        ("Positif", "Positif"),
        ("Négatif", "Négatif"),
    ]

    Client_Joignable = forms.ChoiceField(
        choices=[('', '---------')] + CLIENT_JOIGNABLE_CHOICES,  # Add a blank choice
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    Raison_de_non_commande = forms.ChoiceField(
        choices=RAISON_DE_NON_COMMANDE_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    Feedback_post_Voucher = forms.ChoiceField(
        choices=FEEDBACK_POST_VOUCHER_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    Mail_client_Valide = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )

    commentaire = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control"}),
        required=False,
    )

class HorairePreferenceForm(forms.ModelForm):
    class Meta:
        model = HorairePreference
        exclude = ['user']
        fields = '__all__'


from .models import Winback2Results

class Winback2ResultsForm(forms.ModelForm):
    class Meta:
        model = Winback2Results
        fields = ['joignabilite', 'feedback_interet_voucher', 'raison_non_interesse', 'commentaire']


from .models import Ningen_Staff

class NingenStaffForm(forms.ModelForm):
    class Meta:
        model = Ningen_Staff
        fields = '__all__'
        widgets = {
            'CL': forms.CheckboxSelectMultiple,
        }


from .models import Activite

class ActiviteForm(forms.ModelForm):
    class Meta:
        model = Activite
        fields = '__all__' 
        exclude = ['id','agent','numero_activite'] 
    def __init__(self, *args, **kwargs):
        super(ActiviteForm, self).__init__(*args, **kwargs)

    enregistrer_et_ajouter = forms.BooleanField(required=False, widget=forms.HiddenInput(), initial=True)


from .models import Ningen_Management
class NingenManagementForm(forms.ModelForm):
    class Meta:
        model = Ningen_Management
        fields = '__all__'
        exclude = ['age']
        widgets = {
            'Act': forms.CheckboxSelectMultiple,
        }

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(label='Sélectionnez votre fichier Excel')

from .models import WorkHours

class WorkHourForm(forms.ModelForm):
    class Meta:
        model = WorkHours
        fields = '__all__'

# forms.py

class WorkHourFilterForm(forms.Form):
    full_name = forms.CharField(required=False, label='Nom complet')
    traitement = forms.CharField(required=False, label='Traitement')
    hour = forms.CharField(required=False, label='Heure')
    date = forms.DateField(required=False, label='Date')
    place = forms.CharField(required=False, label='Place')


