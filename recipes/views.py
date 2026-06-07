from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Post, Profile, Ingredient
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileUpdateForm
from django.contrib.auth import logout


def home(request):
    # Беремо 3 останні додані рецепти для головної сторінки
    latest_recipes = Recipe.objects.all().order_by("-id")[:3]
    return render(request, "recipes/index.html", {"recipes": latest_recipes})


def recipes_list(request):
    # Ловимо категорію з URL (наприклад, ?category=DIET)
    category_filter = request.GET.get("category")

    # Якщо користувач вибрав конкретну категорію
    if category_filter:
        # Шукаємо в базі тільки рецепти з цією категорією
        all_recipes = Recipe.objects.filter(category=category_filter).order_by("-id")
    else:
        # Якщо категорії немає (натиснули "Усі рецепти"), показуємо все
        all_recipes = Recipe.objects.all().order_by("-id")

    return render(request, "recipes/recipes.html", {"recipes": all_recipes})


def blog(request):
    # Беремо всі статті блогу, найновіші зверху
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "recipes/blog.html", {"posts": posts})


def about(request):
    # Для сторінки "Про нас" база даних не потрібна, просто віддаємо шаблон
    return render(request, "recipes/about.html")


def recipe_detail(request, recipe_id):
    # Шукаємо рецепт за його ID. Якщо немає — видаємо 404 помилку
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, "recipes/recipe_detail.html", {"recipe": recipe})


# Реєстрація
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])  # Шифруємо пароль
            user.save()
            login(
                request, user, backend="django.contrib.auth.backends.ModelBackend"
            )  # Одразу логінимо після реєстрації
            return redirect("profile")
    else:
        form = UserRegisterForm()
    return render(request, "recipes/register.html", {"form": form})


# Вхід на сайт
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("profile")
    else:
        form = AuthenticationForm()
    return render(request, "recipes/login.html", {"form": form})


# Вихід із сайту
def user_logout(request):
    logout(request)
    return redirect("home")


@login_required
def profile_view(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    # Адмін має свою стару логіку з формою на одній сторінці
    if request.user.is_staff:
        if request.method == "POST":
            form = ProfileUpdateForm(
                request.POST, request.FILES or None, instance=profile
            )
            if form.is_valid():
                form.save()
                return redirect("profile")
        else:
            form = ProfileUpdateForm(instance=profile)
        return render(request, "recipes/admin_profile.html", {"form": form})

    # Звичайний юзер просто дивиться свої дані (без форми)
    return render(request, "recipes/profile.html", {"profile": profile})


@login_required
def profile_edit(request):
    # Окрема сторінка тільки для юзерів, де вони вносять дані
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES or None, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")  # Після збереження кидаємо назад на перегляд
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, "recipes/profile_edit.html", {"form": form})


@login_required
def favorite_items_view(request):
    # Дістаємо з бази всі рецепти та пости, які лайкнув саме цей користувач
    favorite_recipes = request.user.favorite_recipes.all()
    favorite_posts = request.user.favorite_posts.all()
    # Передаємо ці списки у наш HTML-шаблон
    return render(
        request, "recipes/favorite_items.html", {
            "favorite_recipes": favorite_recipes,
            "favorite_posts": favorite_posts,
        }
    )


@login_required
def create_recipe_view(request):
    if request.method == "POST":
        # Витягуємо всі дані з нашої форми
        title = request.POST.get("title")
        category = request.POST.get("category")
        prep_time = request.POST.get("prep_time")
        instructions = request.POST.get("instructions")
        image = request.FILES.get("image")

        # Створюємо рецепт у базі даних
        new_recipe = Recipe.objects.create(
            title=title,
            category=category,
            prep_time=prep_time if prep_time else None,
            instructions=instructions,
            image=image,
            author=request.user,
        )

        # Зберігаємо інгредієнти з форми
        ingredient_count = int(request.POST.get("ingredient_count", 0))
        for i in range(ingredient_count):
            ing_name = request.POST.get(f"ingredient_{i}_name", "").strip()
            if ing_name:  # Зберігаємо тільки якщо назва не порожня
                Ingredient.objects.create(
                    recipe=new_recipe,
                    name=ing_name,
                    weight=float(request.POST.get(f"ingredient_{i}_weight", 0) or 0),
                    calories=float(request.POST.get(f"ingredient_{i}_calories", 0) or 0),
                    protein=float(request.POST.get(f"ingredient_{i}_protein", 0) or 0),
                    fat=float(request.POST.get(f"ingredient_{i}_fat", 0) or 0),
                    carbs=float(request.POST.get(f"ingredient_{i}_carbs", 0) or 0),
                )

        # Після успішної публікації перекидаємо юзера в його улюблене
        return redirect("profile_favorites")

    return render(request, "recipes/create_recipe.html")


@login_required
def toggle_favorite(request, recipe_id):
    if request.method == "POST":
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if request.user in recipe.favorites.all():
            recipe.favorites.remove(request.user)  # Якщо вже є - видаляємо
            is_favorited = False
        else:
            recipe.favorites.add(request.user)  # Якщо нема - додаємо
            is_favorited = True

        return JsonResponse({"is_favorited": is_favorited})
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def toggle_favorite_post(request, post_id):
    """Додати/прибрати статтю блогу з улюблених."""
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        if request.user in post.favorites.all():
            post.favorites.remove(request.user)
            is_favorited = False
        else:
            post.favorites.add(request.user)
            is_favorited = True

        return JsonResponse({"is_favorited": is_favorited})
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def my_recipes_view(request):
    # Витягуємо з бази тільки ті рецепти, які створив цей юзер
    my_recipes = Recipe.objects.filter(author=request.user)
    return render(request, "recipes/my_recipes.html", {"my_recipes": my_recipes})


@login_required
def delete_recipe_view(request, recipe_id):
    # Шукаємо рецепт, перевіряючи, що автор - це саме наш юзер
    recipe = get_object_or_404(Recipe, id=recipe_id, author=request.user)
    if request.method == "POST":
        recipe.delete()
    return redirect("profile_my_recipes")


@login_required
def delete_profile(request):
    if request.method == "POST":
        user = request.user
        logout(request)  # Розлогінюємо користувача
        user.delete()  # Повністю видаляємо акаунт з бази
        return redirect("home")  # Викидаємо на головну сторінку сайту
    return redirect("profile")
