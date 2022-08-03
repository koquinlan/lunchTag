from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "core"


urlpatterns = [
    path("", views.homepage, name="homepage"),

    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),

    path("account", views.account_request, name="account"),
    path("account/edit", views.edit_account_request, name="edit_account"),
    path("account/edit_profile", views.edit_profile_request, name="edit_profile"),

    path("account/strike/<int:userID>", views.strike_request, name="request strike"),
    path("account/remove_strike/<int:userID>", views.remove_strike_request, name="remove strike"),
    path("account/crush/<int:userID>", views.crush_request, name="request crush"),
    path("account/remove_crush", views.remove_crush_request, name="remove crush"),
    path("account/toggle_active", views.toggle_active_request, name="toggle_active"),

    path("edit_pairings", views.edit_pairs_request, name="edit_pairings"),
    path("edit_pairings/create_new", views.create_pairings_request, name="create_pairings"),
    path("edit_pairings/push", views.push_pairings_request, name="push_pairings"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)