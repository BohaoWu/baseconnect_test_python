from django.urls import path

from . import views

app_name = "articles"

urlpatterns = [
    # ex:/articles/
    path("", views.index, name="index"),
    # ex:/articles/
    path("create/", views.create, name="create"),
    # ex:/articles/5/
    path("<int:article_id>/", views.detail, name="detail"),
]