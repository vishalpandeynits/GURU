from django.contrib import admin
from django.conf import settings
from django.urls import path,include
from django.conf.urls.static import static
from django.contrib.auth import views
from users.forms import UserLoginForm
import notifications.urls

urlpatterns = [
    path('AKIAUMKLYNQMHJ3N2H7Q/', admin.site.urls),
    path('', include('basic.urls')),
    path('accounts/password_reset/', views.PasswordResetView.as_view(
    html_email_template_name='registration/password_reset_html_email.html'
    )),
    path('accounts/login/',views.LoginView.as_view(template_name="registration/login.html",
        authentication_form=UserLoginForm),name='login'
    ),
    path('accounts/',include('django.contrib.auth.urls')),
    path('polls/',include('poll.urls')),
    path('profile/',include('users.urls')),
    path('comments/', include('django_comments.urls')),
    path('accounts/', include('allauth.urls')),
    path('rest/',include('rest_framework.urls')),
    #path('basicrest/',include('basic.rest_urls')),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)