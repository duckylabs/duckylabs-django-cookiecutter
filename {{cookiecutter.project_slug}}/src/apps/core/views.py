from django.http import (
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
    HttpResponseServerError,
)
from django.template import loader


def error_400(request, exception=None):  # pragma: no cover
    content = loader.render_to_string("core/error_400.html", {}, request)
    return HttpResponseBadRequest(content)


def error_403(request, exception=None):  # pragma: no cover
    content = loader.render_to_string("core/error_403.html", {}, request)
    return HttpResponseForbidden(content)


def error_404(request, exception=None):  # pragma: no cover
    content = loader.render_to_string("core/error_404.html", {}, request)
    return HttpResponseNotFound(content)


def error_500(request, exception=None):  # pragma: no cover
    content = loader.render_to_string("core/error_500.html", {}, request)
    return HttpResponseServerError(content)
