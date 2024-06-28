__version__ = "{{ cookiecutter.version }}"
__version_info__ = tuple(
    int(num) if num.isdigit() else num
    for num in __version__.replace("-", ".", 1).split(".")
)
{% if cookiecutter.use_celery == 'y' -%}
from {{cookiecutter.project_slug}}.celery import app as celery_app

__all__ = ("celery_app", "__version__", "__version_info__")
{% else %}
__all__ = ("__version__", "__version_info__")
{%- endif %}
