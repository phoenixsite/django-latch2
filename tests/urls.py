"""
Here we define urls for our mock testing app.
Like django.contrib.auth, we chose admin site templates
for our app, so we to being able to run tests,
we need to provide access to admin site without modifing
the app urls.
"""
# pylint: disable=invalid-name
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("latch.urls")),
    path("admin/", admin.site.urls),
]
