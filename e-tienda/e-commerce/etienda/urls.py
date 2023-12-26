from django.urls import path

from . import views

app_name = "etienda"

urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("search/", views.search, name="search"),
    path("category/<str:category>/", views.category_view, name="category_view"),
    path("new_product_form/", views.new_product_form_view, name="new_product_form_view"),
    path("login/", views.login_view, name="login_view"),
    path("consulta1", views.consulta_1, name="consulta1"),
    path("consulta2", views.consulta_2, name="consulta2"),
    path("consulta3", views.consulta_3, name="consulta3"),
    path("consulta4", views.consulta_4, name="consulta4"),
    path("consulta5", views.consulta_5, name="consulta5"),
    path("consulta6", views.consulta_6, name="consulta6"),
    path("consulta7", views.consulta_7, name="consulta7"),
    path("consulta8", views.consulta_8, name="consulta8"),
]