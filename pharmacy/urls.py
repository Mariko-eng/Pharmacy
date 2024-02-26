from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from user.views import custom_permission_denied

handler403 = custom_permission_denied

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('', include('company.urls')),
    path('', include('inventory.urls')),
    path('', include('purchases.urls')),
    path('', include('sales.urls')),

    path('reset_password/', 
          auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="reset_password"),

    path('reset_password/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name ="accounts/password_reset_send.html"),name="password_reset_done"), # Email Sent Success Message

    path('reset_password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name ="accounts/password_reset_form.html"
    ), name='password_reset_confirm'),

     path('reset_password/complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name ="accounts/password_reset_done.html"),name="password_reset_complete"),
             
    path('404/', TemplateView.as_view(template_name='404.html'), name='404'),

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)