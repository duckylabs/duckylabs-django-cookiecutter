from django.contrib.auth.forms import AuthenticationForm
{%- if cookiecutter.use_django_recaptcha == 'y' %}

from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


class RecaptchaAuthenticationForm(AuthenticationForm):
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(
            attrs={
                "data-theme": "light",
                "data-size": "normal",
                "style": (
                    "transform:scale(1.2);-webkit-transform:scale(1.2);"
                    "transform-origin:0 0;-webkit-transform-origin:0 0;"
                ),
                "data-callback": "captchaSuccess",
            }
        )
    )
{%- endif %}
