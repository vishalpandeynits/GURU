from django.urls import path,include
from .views import *

urlpatterns = [
    path('',home,name="home"),
    path('features/',features,name="features"),
    path('privacy-policy/',privacy,name="privacy"),
    path('homepage/',homepage,name="homepage"),
    path('classroom/<unique_id>/',classroom_page,name="classroom_page"),
    path('class/<unique_id>/',subjects,name="subjects"),
    path('<unique_id>/<int:subject_id>/delete/',delete_subject,name="delete_subject"), 

    path('<unique_id>/<username>/Classadmin/',admin_status,name="class_admin"),
    path('<str:unique_id>/<str:username>/remove/',remove_member, name="remove_member"),
    path('<str:unique_id>/<str:username>/accept/',accept_request, name="accept_request"),
    path('<str:unique_id>/<str:username>/delete/',delete_request, name="delete_request"),

    path('<unique_id>/<subject_id>/resource/',notes_list,name="resources"), # 
    path('<unique_id>/<subject_id>/<id>/read/',note_details,name="read_note"), #
    path('<unique_id>/<subject_id>/<id>/delete/',note_delete,name="delete_resource"),
    
    path('<unique_id>/<subject_id>/announcement/',announcements_list,name="announcement"),#
    path('<unique_id>/<subject_id>/<id>/announcement/',announcement_details,name="announcement_page"),
    path('<unique_id>/<subject_id>/<id>/announcement/delete/',announcement_delete,name="delete_announcement"),

    path('<unique_id>/<subject_id>/assignments/',assignments_list,name="assignments"),#
    path('<unique_id>/<subject_id>/<id>/assignment/',assignment_details,name="assignment_page"),
    path('<unique_id>/<subject_id>/<id>/assignment-handle/',assignment_handle,name="assignment-handle"),
    path('<unique_id>/<subject_id>/<id>/assignment/delete/',assignment_delete,name="delete_assignment"),

    path('<unique_id>/<subject_id>/subject_details/',subject_details,name="subject_details"),#
    path('<unique_id>/<subject_id>/upload_permissions/<username>/',manage_upload_permission,name="upload_permissions"),

    path('<unique_id>/unsend-request',unsend_request,name="unsend_request"),
    path('<unique_id>/<subject_id>/<id>/see-marks',export_marks,name="export_marks"),
]