from django.urls import path,include
from .views import *

urlpatterns = [
    path('',home,name="home"),
    path('homepage/',homepage,name="homepage"),
    path('guru/join/<unique_id>/',join,name="join"),
    path('classroom/<unique_id>/',classroom_page,name="classroom_page"),
    path('guru/<unique_id>/',subjects,name="subjects"),
    path('<unique_id>/<int:subject_id>/delete/',delete_subject,name="delete_subject"), 
    path('<unique_id>/<username>/Classadmin/',admin_status,name="class_admin"),

    path('subjects/<str:unique_id>/<str:username>/removeMember/',remove_member, name="remove_member"),
    path('subjects/<str:unique_id>/<str:username>/acceptRequest/',accept_request, name="accept_request"),
    path('subjects/<str:unique_id>/<str:username>/deleteRequest/',delete_request, name="delete_request"),

    path('<unique_id>/<subject_id>/resource/',notes_list,name="resources"), # 
    path('<unique_id>/<subject_id>/<id>/read/',note_details,name="read_note"), #
    path('<unique_id>/<subject_id>/<id>/resource/delete/',resource_delete,name="delete_resource"),
    
    path('<unique_id>/<subject_id>/announcement/',announcements_list,name="announcement"),#
    path('<unique_id>/<subject_id>/<id>/announcement/',announcement_details,name="announcement_page"),
    path('<unique_id>/<subject_id>/<id>/announcement/delete/',announcement_delete,name="delete_announcement"),

    path('<unique_id>/<subject_id>/assignments/',assignments_list,name="assignments"),#
    path('<unique_id>/<subject_id>/<id>/assignment/',assignment_details,name="assignment_page"),
    path('<unique_id>/<subject_id>/<id>/assignment-handle/',assignment_handle,name="assignment-handle"),
    path('<unique_id>/<subject_id>/<id>/assignment/delete/',assignment_delete,name="delete_assignment"),

    path('<unique_id>/<subject_id>/subject_details/',subject_details,name="subject_details"),#
    path('<unique_id>/<subject_id>/upload_permissions/<username>/',manage_upload_permission,name="upload_permissions"),

    path('<unique_id>/unsend-request',unsend_request,name="unsend_request")
]