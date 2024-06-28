"""
URL configuration for {{cookiecutter.project_slug}} project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.contrib.auth import urls as auth_urls
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
{% if cookiecutter.use_django_recaptcha == 'y' %}
from apps.core.forms import RecaptchaAuthenticationForm
{%- endif %}


admin.autodiscover()
{%- if cookiecutter.use_django_recaptcha == 'y' %}
admin.site.login_form = RecaptchaAuthenticationForm
{%- endif %}
admin.site.login_template = "core/admin_login.html"
admin.site.site_title = _("{{cookiecutter.project_name}} Admin Site")
admin.site.site_header = _("{{cookiecutter.project_name}} Administration")
admin.site.index_title = "{{cookiecutter.project_name}}"


urlpatterns = [
    path("", TemplateView.as_view(template_name="core/index.html"), name="index"),
    path("accounts/", include(auth_urls)),
    path(settings.ADMIN_URL, admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]


handler404 = "apps.core.views.error_404"
handler500 = "apps.core.views.error_500"
handler403 = "apps.core.views.error_403"
handler400 = "apps.core.views.error_400"
