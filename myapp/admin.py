from django.contrib import admin
from .models import case, Image, VisitedLink, CopyMacro, Campagne, HorairePreference, Winback2, Winback2Results, Winback2, Winback2Results, CampagneResults,Activite,Ningen_Management
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,UserLoginLogoutRecord,StatusChange,Ningen_Staff
from django.contrib import admin
from django.utils.html import format_html

@admin.register(case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ("numero", "nom","action","macro")


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview')

    def image_preview(self, obj):
        return f'<img src="{obj.image.url}" width="100"/>'

    image_preview.allow_tags = True
    image_preview.short_description = 'Image Preview'


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('name', 'access_choice', 'is_active', 'image_preview')
    list_filter = ('access_choice', 'is_active')
    fieldsets = (
        (None, {'fields': ('name', 'password', 'image')}),
        ('Permissions', {'fields': ('access_choice', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'password1', 'password2', 'access_choice', 'is_active', 'image'),
        }),
    )
    search_fields = ('name',)
    ordering = ('name',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" style="object-fit: cover;"/>', obj.image.url)
        else:
            return "No Image"

    image_preview.short_description = 'Image Preview'


class VisitedLinkAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'url', 'date', 'time')

admin.site.register(VisitedLink, VisitedLinkAdmin)


class CopiedMacroAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'link', 'date', 'time')

admin.site.register(CopyMacro, CopiedMacroAdmin)


class UserLoginLogoutRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_time', 'logout_time','device','duration')
    list_filter = ('user',)
    search_fields = ('user__username',)

admin.site.register(UserLoginLogoutRecord, UserLoginLogoutRecordAdmin)

class StatusChangeAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'start_time', 'end_time')
    list_filter = ('status',)
    search_fields = ('user__username', 'status')
    date_hierarchy = 'start_time'

# Register the StatusChange model with the admin site
admin.site.register(StatusChange, StatusChangeAdmin)

class CampagneAdmin(admin.ModelAdmin):
    list_display = ('submission_datetime','treated_by','GSM', 'Voucher_eligibilty', 'Email', 'Customer_ID','Voucher_Validity', 'Voucher_code','Client_Joignable','Agent','Done','is_locked','locked_by')
    list_filter = ('treated_by','Client_Joignable', 'Done','Agent','is_locked','submission_datetime','locked_by')
    search_fields = ('GSM', 'Email', 'Customer_ID', 'Agent')

# Register your Campagne model with the custom admin class
admin.site.register(Campagne, CampagneAdmin)


class CampagneResultsAdmin(admin.ModelAdmin):
    list_display = ('date_time','treated_by','GSM', 'Client_Joignable', 'Raison_de_non_commande', 'Feedback_post_Voucher','Mail_client_Valide', 'commentaire','done')
    list_filter = ('Client_Joignable', 'done','date_time','treated_by')
    search_fields = ('GSM', 'Agent')

# Register your Campagne model with the custom admin class
admin.site.register(CampagneResults, CampagneResultsAdmin)


class HorairePreferenceAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'Quel_régime_horaire_préférez_vous',
    )
admin.site.register(HorairePreference,HorairePreferenceAdmin)


class Winback2Admin(admin.ModelAdmin):
    list_display = ('Date_de_traitement','GSM','VOUCHER_ELIGIBILITY', 'CUSTOMER_ID', 'CLIENT_JOIGNABLE', 'RAISON_DE_NON_COMMANDE','FEEDBACK_POST_VOUCHER', 'COMMENTAIRE','Voucher_code','Email','CLIENT_JOIGNABLE2','done','locked')
    list_filter = ( 'CLIENT_JOIGNABLE','done','CLIENT_JOIGNABLE2','FEEDBACK_POST_VOUCHER','locked')
    search_fields = ('GSM','VOUCHER_ELIGIBILITY', 'CUSTOMER_ID','Voucher_code','Email')

# Register your Campagne model with the custom admin class
admin.site.register(Winback2, Winback2Admin)


class Winback2ResultsAdmin(admin.ModelAdmin):
    list_display = ('date_time','treated_by','GSM','joignabilite', 'feedback_interet_voucher', 'raison_non_interesse', 'commentaire','done')
    list_filter = ('date_time','joignabilite','done')
    search_fields = ('GSM','joignabilite')

admin.site.register(Winback2Results, Winback2ResultsAdmin)


class Ningen_StaffAdmin(admin.ModelAdmin):
    list_display = ('ID_Beside','Prenom','Nom')
    search_fields = ('Prenom','Nom')

admin.site.register(Ningen_Staff,Ningen_StaffAdmin)


class ActiviteAdmin(admin.ModelAdmin):
    list_display = ['numero_activite', 'nom_activite', 'agent']
    search_fields = ('agent','nom_activite')
admin.site.register(Activite, ActiviteAdmin)


class Ningen_ManagementAdmin(admin.ModelAdmin):
    list_display = ('ID_Beside','Prenom','Nom')
    search_fields = ('Prenom','Nom')

admin.site.register(Ningen_Management,Ningen_ManagementAdmin)