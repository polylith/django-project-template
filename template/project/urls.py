from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.urls import path, include


def health(request: HttpRequest) -> HttpResponse:
    from django.contrib.auth.models import User
    from django.db.utils import OperationalError

    try:
        users = User.objects.all().first()
    except OperationalError:
        return HttpResponse(status=500)
    else:
        return HttpResponse(status=200)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("django_prometheus.urls")),
]
