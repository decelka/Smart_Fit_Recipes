from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("recipes/", views.recipes_list, name="recipes"),
    path("recipe/<int:recipe_id>/", views.recipe_detail, name="recipe_detail"),
    path("blog/", views.blog, name="blog"),
    path("about/", views.about, name="about"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="recipes/password_reset.html"
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="recipes/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="recipes/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="recipes/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("profile/favorites/", views.favorite_items_view, name="profile_favorites"),
    path("profile/create-recipe/", views.create_recipe_view, name="create_recipe"),
    path(
        "recipe/<int:recipe_id>/favorite/",
        views.toggle_favorite,
        name="toggle_favorite",
    ),
    path(
        "post/<int:post_id>/favorite/",
        views.toggle_favorite_post,
        name="toggle_favorite_post",
    ),
    path("profile/my-recipes/", views.my_recipes_view, name="profile_my_recipes"),
    path(
        "recipe/<int:recipe_id>/delete/", views.delete_recipe_view, name="delete_recipe"
    ),
    path("profile/delete/", views.delete_profile, name="delete_profile"),
]
