from django.contrib import admin
from .models import Recipe, Ingredient, Post, Profile


# Цей клас дозволяє додавати інгредієнти прямо на сторінці створення самого рецепту
class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1  # Кількість порожніх рядків для нових інгредієнтів


# Налаштовуємо вигляд таблиці рецептів в адмінці
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "prep_time", "author")
    inlines = [IngredientInline]  # Прив'язуємо інгредієнти


# Реєструємо моделі
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Post)
admin.site.register(Profile)
