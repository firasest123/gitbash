from datetime import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone
from datetime import date, datetime
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.signals import pre_save

class case(models.Model):
    id = models.AutoField(primary_key=True, default=None)
    numero = models.IntegerField()
    nom = models.TextField()
    action = models.TextField()
    macro = models.TextField()

    def formatted_macro(self):
        import re
        return re.sub(r'\[(.*?)\]', r'<strong style="color:red">\1</strong>', self.macro)

    def formatted_action(self):
        import re
        return re.sub(r'\[(.*?)\]', r'<strong style="color:red">\1</strong>', self.action)


class Image(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name


# Create a custom manager for the CustomUser model
class CustomUserManager(BaseUserManager):
    def create_user(self, name, password=None, **extra_fields):
        if not name:
            raise ValueError('The Name field must be set')

        user = self.model(name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(name, password, **extra_fields)

# Define choices for the access level
ACCESS_LEVEL_CHOICES = [
    ('',''),
    ('manager', 'Manager'),
    ('cl', 'CL'),
    ('agent', 'Agent'),
]

# Define the CustomUser model with the access_level field
class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True, default=r"user_images\16612.png")
    access_choice = models.CharField(max_length=10, choices=ACCESS_LEVEL_CHOICES, default='',null=True, blank=True)  # Add access_choice field
    objects = CustomUserManager()

    USERNAME_FIELD = 'name'

    def __str__(self):
        return self.name

    def upload_image(self, image_file):
        self.image = image_file
        self.save()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


class VisitedLink(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=200)
    url = models.URLField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.name}"

class CopyMacro(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    text = models.TextField()
    link = models.URLField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.text[:50]}'


class UserLoginLogoutRecord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    device = models.CharField(max_length=20, null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    def logout(self):
        self.logout_time = timezone.now()
        self.save()

    def __str__(self):
        return f"User: {self.user}, Login Time: {self.login_time}, Logout Time: {self.logout_time}, Device: ({self.device})"


class StatusChange(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    def __str__(self):
        return f"{self.user} - {self.status}"


class Campagne(models.Model):
    treated_by = models.CharField(max_length=100, null=True, blank=True)
    GSM = models.IntegerField(primary_key=True)
    Voucher_eligibilty = models.IntegerField(null=True, blank=True)
    Email = models.CharField(max_length=100,null=True, blank=True)
    Customer_ID = models.CharField(max_length=100,null=True, blank=True)
    Client_Joignable = models.TextField(null=True, blank=True)
    Voucher_Validity = models.DateField(null=True, blank=True)
    Voucher_code = models.TextField(null=True, blank=True)
    Agent = models.CharField(max_length=100, null=True, blank=True)
    Done = models.BooleanField(default=False)
    locked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    is_locked = models.BooleanField(default=False)
    submission_datetime = models.DateTimeField(default='', null=True, blank=True)

    def __str__(self):
        return f"{self.GSM} - {self.Agent}"



class CampagneResults(models.Model):
    treated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    GSM = models.IntegerField(null=True, blank=True)
    Client_Joignable = models.TextField(null=True, blank=True)
    Raison_de_non_commande = models.TextField(null=True, blank=True)
    Feedback_post_Voucher = models.TextField(null=True, blank=True)
    Mail_client_Valide = models.TextField(null=True, blank=True)
    commentaire = models.TextField(null=True, blank=True)
    done = models.BooleanField(null=True, blank=True)


class HorairePreference(models.Model):

    REGIME_HORAIRE_CHOICES = [
        (
        '48 Hrs',
        '48 Hrs'),
        (
        '40 Hrs',
        '40 Hrs'),
        (
        '30 Hrs',
        '30 Hrs'),
        (
        '24 Hrs',
        '24 Hrs'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    Quel_régime_horaire_préférez_vous = models.CharField(max_length=225, choices=REGIME_HORAIRE_CHOICES, blank=False, null=False)

    def __str__(self):
        return f"HorairePreference: {self.pk}"



class Winback2(models.Model):
    Date_de_traitement = models.DateField(null=True, blank=True)
    GSM = models.IntegerField(primary_key=True)
    VOUCHER_ELIGIBILITY = models.IntegerField(null=True, blank=True)
    CUSTOMER_ID = models.CharField(max_length=20)
    CLIENT_JOIGNABLE = models.TextField(null=True, blank=True)
    RAISON_DE_NON_COMMANDE = models.TextField(null=True, blank=True)
    FEEDBACK_POST_VOUCHER = models.TextField(null=True, blank=True)
    COMMENTAIRE = models.TextField(null=True, blank=True)
    Voucher_code = models.CharField(max_length=20)
    Email = models.CharField(max_length=100,null=True, blank=True)
    CLIENT_JOIGNABLE2 = models.TextField(null=True, blank=True)
    done = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)
    def __str__(self):
        return str(self.GSM)



class Winback2Results(models.Model):
    treated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    GSM = models.IntegerField(null=True, blank=True)
    joignabilite_choices = [
        ('Injoignable 1ère tentative', 'Injoignable 1ère tentative'),
        ('Injoignable 2éme tentative', 'Injoignable 2éme tentative'),
        ('Injoignable', 'Injoignable'),
        ('Joignable', 'Joignable'),
    ]

    joignabilite = models.CharField(max_length=50, choices=joignabilite_choices)
    FEEDBACK_CHOICES = [
        ("Positif", "Positif"),
        ("Négatif", "Négatif"),
    ]
    feedback_interet_voucher = models.CharField(max_length=10, choices=FEEDBACK_CHOICES)
    raison_non_interesse = models.TextField()
    commentaire = models.TextField()
    done = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f'Winback2 Results - {self.date_time}'


CL_CHOICES = [
        ("", ""),
        ("Khaoula Werghi", "Khaoula Werghi"),
        ("Anis Hedhli", "Anis Hedhli"),
        ("Ishrak Ben Rjab", "Ishrak Ben Rjab"),
        ("Molka CHOUIKA", "Molka CHOUIKA"),
        ("Mohamed Amine ZOUAOUI", "Mohamed Amine ZOUAOUI"),
]


class Ningen_Staff(models.Model):
    Ngroupe = models.IntegerField(default=None)
    Matricule = models.IntegerField(null=True, blank=True)
    ID_Beside = models.CharField(max_length=30,default=None)
    Prenom = models.CharField(max_length=20,null=True, blank=True)
    Nom = models.CharField(max_length=20,null=True, blank=True)
    Fonction=models.CharField(null=True, blank=True,max_length=50, choices=[
        ("Chargé Client", "Chargé Client"),
        ("Conseiller Leader", "Conseiller Leader"),
    ])
    Genre=models.CharField(null=True, blank=True,max_length=2, choices=[
        ("M", "M"),
        ("F", "F"),
    ])
    CL_CHOICES = [
        ("", ""),
        ("Khaoula Werghi", "Khaoula Werghi"),
        ("Anis Hedhli", "Anis Hedhli"),
        ("Ishrak Ben Rjab", "Ishrak Ben Rjab"),
        ("Molka CHOUIKA", "Molka CHOUIKA"),
        ("Mohamed Amine ZOUAOUI", "Mohamed Amine ZOUAOUI"),
    ]
    CL = models.ManyToManyField('CLChoiceModel', blank=True)

    N1_CHOICES = [
        ("Mehrzia Hannafi", "Mehrzia Hannafi"),
        ("Ines Dridi", "Ines Dridi"),    
        ("Mounir Bech", "Mounir Bech"),
    ]
    N1 = models.CharField(max_length=25, choices=N1_CHOICES)

    N2_CHOICES = [
        ("Mounir Bech", "Mounir Bech"),
        ("Ali Hamouda", "Ali Hamouda"),   
    ]
    N2 = models.CharField(max_length=25, choices=N2_CHOICES)
    Date_embauche = models.DateField(null=True, blank=True)
    Date_fin_1ere_période_d_essai = models.DateField(null=True, blank=True)

    contrat_CHOICES = [
        ("CDI", "CDI"),
        ("CIVP", "CIVP"),
        ("EL Karama", "EL Karama"), 
        ("Stage", "Stage"), 
    ]
    Type_de_contrat = models.CharField(max_length=10, choices=contrat_CHOICES)

    Regime_CHOICES = [
            ("20", "20"),
            ("24", "24"),
            ("28", "28"),
            ("30", "30"),
            ("40", "40"),
            ("45", "45"),
            ("48", "48"),
        ]
    Régime_horaire = models.CharField(max_length=2, choices=Regime_CHOICES)
    CIN = models.CharField(max_length=8,null=True, blank=True)
    Titulaire_CHOICES = [
            ("oui", "oui"),
            ("non", "non"),
        ]
    Titulaire = models.CharField(max_length=3, choices=Titulaire_CHOICES)
    Date_de_titularisation = models.DateField(null=True, blank=True)
    Tel = models.IntegerField(null=True, blank=True)
    Date_de_naissance = models.DateField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Calculate age when saving the model
        if self.Date_de_naissance:
            today = date.today()
            age = today.year - self.Date_de_naissance.year - (
                        (today.month, today.day) < (self.Date_de_naissance.month, self.Date_de_naissance.day))
            self.age = age
        else:
            self.age = None
        super().save(*args, **kwargs)

    Situation_CHOICES= [
            ("marié", "marié"),
            ("célibataire", "célibataire"),
        ]
    Situation = models.CharField(max_length=20, choices=Situation_CHOICES,null=True)

    Nombre_d_enfants = models.IntegerField(null=True, blank=True)

    etude_CHOICES = [
                ("Lycée/Bac non validé", "Lycée/Bac non validé"),
                ("bac", "bac"),
                ("bac+1", "bac+1"),
                ("bac+2", "bac+2"),
                ("bac+3", "bac+3"),
                ("bac+4", "bac+4"),
                ("bac+5", "bac+5"),
                ("BTP", "BTP"),
            ]
    Niveau_d_etude = models.CharField(max_length=20, choices=etude_CHOICES,null=True, blank=True)
    Diplome = models.CharField(max_length=255,null=True, blank=True)
    Centre_d_intérêt = models.CharField(max_length=255,null=True, blank=True)
    Mail_personel = models.EmailField(null=True, blank=True)
    Adresse_postale = models.CharField(max_length=255,null=True, blank=True)
    Activité_actuelle=models.CharField(null=True, blank=True,max_length=50, choices=[
        ("Jumia TN", "Jumia TN"),
        ("Jumia DZ", "Jumia DZ"),
        ("KooL", "KooL"),
        ("Arkan", "Arkan"),
    ])

    Micro_activité_actuelle=models.CharField(null=True, blank=True,max_length=50, choices=[
        ("CS", "CS"),
        ("Confirmation", "Confirmation"),
        ("ODS", "ODS"),
        ("PG", "PG"),
    ])
    LOB_actuelle=models.CharField(null=True, blank=True,max_length=50, choices=[
        ("CS", "CS"),
        ("BO", "BO"),
        ("Confirmation", "Confirmation"),
        ("ODS", "ODS"),
        ("Sales", "Sales"),
    ])
    Affectation_actuelle_CANAL=models.CharField(null=True, blank=True,max_length=50, choices=[
        ("IB", "IB"),
        ("IB/OB", "IB/OB"),
        ("LiveChat", "LiveChat"),
        ("Voice", "Voice"),
    ])
    TT=models.BooleanField(default=False)
    Statut_à_date = models.CharField(null=True, blank=True,max_length=50, choices=[
        ("Actif", "Actif"),
        ("démission", "démission"),
        ("FPE", "FPE"),
    ])
    Mission_spéciale = models.CharField(max_length=255,null=True, blank=True)
    Date_FPE = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.ID_Beside

class CLChoiceModel(models.Model):
    name = models.CharField(max_length=50,null=True, blank=True, choices=CL_CHOICES)

    def __str__(self):
        return self.name
    


class Activite(models.Model):
    agent = models.ForeignKey('Ningen_Staff', on_delete=models.CASCADE)
    numero_activite = models.PositiveIntegerField()
    nom_activite = models.CharField(max_length=50, choices=[
        ("Jumia TN", "Jumia TN"),
        ("Jumia DZ", "Jumia DZ"),
        ("KooL", "KooL"),
        ("Arkan", "Arkan"),
    ])
    Line_of_business = models.CharField(max_length=50, choices=[
        ("CS", "CS"),
        ("Confirmation", "Confirmation"),
        ("ODS", "ODS"),
        ("PG", "PG"),
    ])

    Skills_CS = models.BooleanField(default=False)
    Skills_Sales = models.BooleanField(default=False)
    Skills_BO = models.BooleanField(default=False)
    Skills_Confirmation = models.BooleanField(default=False)
    CANAL_IB = models.BooleanField(default=False)
    CANAL_OB = models.BooleanField(default=False)
    CANAL_Live_Chat = models.BooleanField(default=False)

    class Meta:
        unique_together = ('agent', 'numero_activite')

    def save(self, *args, **kwargs):
        if not self.numero_activite:
            max_numero_activite = Activite.objects.filter(
                agent=self.agent
            ).aggregate(models.Max('numero_activite'))['numero_activite__max'] or 0

            self.numero_activite = max_numero_activite + 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Activité {self.numero_activite}: {self.nom_activite}"



Act_CHOICES = [
        ("Jumia TN", "Jumia TN"),
        ("Jumia DZ", "Jumia DZ"),
        ("KooL", "KooL"),
        ("Arkan", "Arkan"),
    ]

class Ningen_Management(models.Model):
    Matricule = models.IntegerField(null=True, blank=True)
    ID_Beside = models.CharField(max_length=30,default=None)
    Prenom = models.CharField(max_length=20,null=True, blank=True)
    Nom = models.CharField(max_length=20,null=True, blank=True)
    Genre=models.CharField(null=True, blank=True,max_length=2, choices=[
        ("M", "M"),
        ("F", "F"),
    ])
    Date_de_naissance = models.DateField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    Situation_CHOICES= [
            ("marié", "marié"),
            ("célibataire", "célibataire"),
        ]
    Situation = models.CharField(max_length=20, choices=Situation_CHOICES,null=True)

    def save(self, *args, **kwargs):
        # Calculate age when saving the model
        if self.Date_de_naissance:
            today = date.today()
            age = today.year - self.Date_de_naissance.year - (
                        (today.month, today.day) < (self.Date_de_naissance.month, self.Date_de_naissance.day))
            self.age = age
        else:
            self.age = None
        super().save(*args, **kwargs)

    Nombre_d_enfants = models.IntegerField(null=True, blank=True)

    etude_CHOICES = [
                ("Lycée/Bac non validé", "Lycée/Bac non validé"),
                ("bac", "bac"),
                ("bac+1", "bac+1"),
                ("bac+2", "bac+2"),
                ("bac+3", "bac+3"),
                ("bac+4", "bac+4"),
                ("bac+5", "bac+5"),
                ("bac+6", "bac+6"),
                ("BTP", "BTP"),
            ]
    Niveau_d_etude = models.CharField(max_length=20, choices=etude_CHOICES,null=True, blank=True)

    Diplome = models.CharField(max_length=255,null=True, blank=True)

    Centre_d_intérêt = models.CharField(max_length=255,null=True, blank=True)

    Mail_personel = models.EmailField(null=True, blank=True)
    Tel1 = models.IntegerField(null=True, blank=True)
    Tel2 = models.IntegerField(null=True, blank=True)
    Adresse_postale = models.CharField(max_length=255,null=True, blank=True)

    Fonction=models.CharField(null=True, blank=True,max_length=50, choices=[
        ("Floor manager quality and process", "Floor manager quality and process"),
        ("Responsable WFM", "Responsable WFM"),
        ("Responsable IT", "Responsable IT"),
        ("Dir PROD", "Dir PROD"),
        ("MANGING ASSOCIATE", "MANGING ASSOCIATE"),
        ("DPH", "DPH"),
        ("Responsable Qualité", "Responsable Qualité"),
        ("Floor Manager ", "Floor Manager "),
        ("Team leader", "Team leader"),
        ("Data Analyst junior", "Data Analyst junior"),
        ("Assistante de direction", "Assistante de direction"),
        ("Développeur Junior", "Développeur Junior"),
        ("Floor Manager ", "Floor Manager "),
    ])
    
    

    N1_CHOICES = [  
        ("Mounir Bech", "Mounir Bech"),
        ("Samiha M'RABET", "Samiha M'RABET"),
        ("Stéphane DUCREUX", "Stéphane DUCREUX"),    
        ("Ali HAMOUDA", "Ali HAMOUDA"),
        ("Manel MADOURI", "Manel MADOURI"),
        ("Aymen DRIDI", "Aymen DRIDI"),    
    ]
    N1 = models.CharField(max_length=25, choices=N1_CHOICES)
    Act_CHOICES = [
        ("Jumia TN", "Jumia TN"),
        ("Jumia DZ", "Jumia DZ"),
        ("KooL", "KooL"),
        ("Arkan", "Arkan"),
    ]
    Act = models.ManyToManyField('actChoiceModel', blank=True)

    Date_embauche = models.DateField(null=True, blank=True)
    Durrée_mission= models.DurationField(null=True, blank=True)
    Date_fin_1ere_période_d_essai = models.DateField(null=True, blank=True)

    contrat_CHOICES = [
        ("CDI", "CDI"),
        ("CIVP", "CIVP"),
        ("EL Karama", "EL Karama"),
        ("Stage", "Stage"), 
    ]
    Type_de_contrat = models.CharField(max_length=10, choices=contrat_CHOICES)

    Regime_CHOICES = [
            ("20", "20"),
            ("24", "24"),
            ("28", "28"),
            ("30", "30"),
            ("40", "40"),
            ("45", "45"),
            ("48", "48"),
        ]
    Régime_horaire = models.CharField(max_length=2, choices=Regime_CHOICES)
    CIN = models.CharField(max_length=8,null=True, blank=True)
    Titulaire_CHOICES = [
            ("oui", "oui"),
            ("non", "non"),
        ]
    Titulaire = models.CharField(max_length=3, choices=Titulaire_CHOICES)

    Date_de_titularisation = models.DateField(null=True, blank=True)
    
    Statut_à_date = models.CharField(null=True, blank=True,max_length=50, choices=[
        ("Actif", "Actif"),
        ("démission", "démission"),
        ("FPE", "FPE"),
    ])
    Date_FPE = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.ID_Beside
    


class actChoiceModel(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, choices=Act_CHOICES)

    def __str__(self):
        return self.name

class WorkHours(models.Model):

    id_day = models.IntegerField(default=0)
    id_upload = models.IntegerField(default=0)
    full_name = models.CharField(max_length=255)
    traitement = models.CharField(max_length=255)
    hour = models.CharField(max_length=5)
    date = models.DateField()
    place = models.CharField(max_length=255)

    class Meta:
        unique_together = ['full_name','hour','date']

class upload(models.Model):
    id_upload = models.IntegerField(default=0)
    nom_excel = models.CharField(max_length=255)
    workhour_dispo = models.IntegerField(default=0)
    date = models.DateField()

    class Meta:
        unique_together = ['id_upload']
