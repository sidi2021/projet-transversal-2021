from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from django.conf.urls import url, handler404, handler500
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("administration.urls", namespace="administration")),
    path("", include("comptes.urls", namespace="comptes")),
    path("reset_password/", auth_views.PasswordResetView.as_view(template_name="comptes/reset_password.html"), name="reset_password"),
    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(template_name="comptes/password_reset_sent.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(template_name="comptes/password_reset_form.html"), name="password_reset_confirm"),
    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(template_name="comptes/password_reset_done.html"), name="password_reset_complete",),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()

if not settings.DEBUG:
    urlpatterns += [
        url(r"^static/(?P<path>.*)/$", serve, {"document_root": settings.STATIC_ROOT,}),
    ]


handler404 = "comptes.views.view_404"

handler500 = "comptes.views.view_500"
