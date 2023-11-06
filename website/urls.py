from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

handler404 = "website.views.custom_404"
urlpatterns = [
    path("", views.main, name="main"),
    path("property", views.show_property),
    path("search", views.search_property),
    path("parse", views.parse_all),
    path("searching", views.search),
    path("404", views.custom_404, kwargs={"exception": Exception("Page not Found!")}),
    # path("usi/", views.usi),
    # path("thanks/", views.thanks),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
