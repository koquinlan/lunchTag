from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "core"


urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("help", views.help_request, name="help"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    # Password reset URLs
    path("password_reset/", auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset.html",
        email_template_name="accounts/password_reset_email.html",
        subject_template_name="accounts/password_reset_subject.txt",
        success_url="done/"
    ), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_done.html"
    ), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_confirm.html",
        success_url="done/"
    ), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_complete.html"
    ), name="password_reset_complete"),
    path("account", views.account_request, name="account"),
    path("account/edit", views.edit_account_request, name="edit_account"),
    path("account/edit_profile", views.edit_profile_request, name="edit_profile"),
    path(
        "account/edit_profile/remove_avatar",
        views.remove_avatar_request,
        name="remove_avatar",
    ),
    path("account/strike/<int:userID>", views.strike_request, name="request strike"),
    path(
        "account/remove_strike/<int:userID>",
        views.remove_strike_request,
        name="remove strike",
    ),
    path("account/crush/<int:userID>", views.crush_request, name="request crush"),
    path("account/remove_crush", views.remove_crush_request, name="remove crush"),
    path("account/toggle_active", views.toggle_active_request, name="toggle_active"),
    path("edit_pairings", views.edit_pairs_request, name="edit_pairings"),
    path(
        "edit_pairings/create_new",
        views.create_pairings_request,
        name="create_pairings",
    ),
    path("edit_pairings/push", views.push_pairings_request, name="push_pairings"),
]
