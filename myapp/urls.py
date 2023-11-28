from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import custom_login,save_copy_macro,custom_logout


urlpatterns = [
    path('', views.index, name='index'),
    path('jumia_ods_tn', views.jumia_ods_tn, name='jumia_ods_tn'),
    path('get_case_suggestions/', views.get_case_suggestions, name='get_case_suggestions'),
    path('case_detail/<str:case_numero>/<str:case_nom>/', views.case_detail, name='case_detail'),
    path('image/<str:image_name>/', views.serve_image, name='image'),
    path('case_list/<str:case_name>/', views.case_list_view, name='case_list'),
    path('commande_annulee/', views.commande_annulee_view, name='commande_annulee'),
    path('login/', views.custom_login, name='user_login'),
    path('logout/', views.custom_logout, name='user_logout'),
    path('download_interactions/', views.download_interactions, name='download_interactions'),
    path('save_copy_macro/', save_copy_macro, name='save_copy_macro'),
    path('download_copied_macros/', views.download_copied_macros, name='download_copied_macros'),
    path('download_user_login_logout/', views.download_user_login_logout, name='download_user_login_logout'),
    path('change-password/', views.change_password, name='change_password'),
    path('change_status/<str:status>/', views.change_status, name='change_status'),
    path('download_status_excel/', views.download_status_excel, name='download_status_excel'),
    path('upload_excel/', views.upload_excel, name='upload_excel'),
    path('winbacklist/', views.agent_gsm_list, name='agent_gsm_list'),
    path('gsm/<int:gsm_id>/', views.gsm_detail, name='gsm_detail'),
    path('winback-form/<int:gsm>/<str:Email>/', views.winback_form, name='winback_form'),
    path('release-lock/<str:gsm_id>/', views.release_lock, name='release_lock'),
    path('agent_processed_forbidden/', views.agent_processed_forbidden_view, name='agent_processed_forbidden'),
    path('horaire_preference/', views.preference_regime_horaire_view, name='horaire_preference'),
    path('uploadwinback2/', views.uploadwinback2, name='uploadwinback2'),
    path('winback_rappel_list/', views.winback_rappel_list, name='winback_rappel_list'),
    path('winback2/<int:gsm>/', views.winback2_detail, name='winback2_detail'),
    path('winback2/<int:gsm>/release_lock2/', views.release_lock2, name='release_lock2'),
    path('winback-form2/<int:gsm>/', views.winback_form_view, name='winback_form2'),
    path('addStaff/', views.create_staff, name='addStaff'),
    path('ajouter_activite/<str:id_beside>/', views.ajouter_activite, name='ajouter_activite'),
    path('staff/', views.staff_list, name='staff_list'),
    path('agent/<str:id_beside>/', views.agent_detail, name='agent_detail'),
    path('download_selected_staff/', views.download_selected_staff, name='download_selected_staff'),
    path('modify_staff/<str:id_beside>/', views.modify_staff, name='modify_staff'),
    path('modify_activity/', views.modify_activity, name='modify_activity'),
    path('add_activity/', views.add_activity, name='add_activity'),
    path('addManagement/', views.create_management, name='addManagement'),
    path('test/', views.testview, name='test'),
    path('upload_planning/', views.manage_hours, name='upload_planning'),
    path('WorkHour/', views.WorkHour, name='WorkHour'),
    path('delete_work_hour/<int:work_hour_id>/', views.delete_work_hour, name='delete_work_hour'),
    path('delete_upload/<int:upload_id>/', views.delete_upload, name='delete_upload'),
    path('show_session/<int:upload_id>/', views.show_session, name='show_session'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)