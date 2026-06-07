from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Таблиця для статей Блогу
class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст статті")
    image = models.ImageField(
        upload_to="blog_images/", blank=True, null=True, verbose_name="Фото для статті"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публікації")

    # Улюблені статті — юзер може зберегти статтю в обране
    favorites = models.ManyToManyField(
        User, related_name="favorite_posts", blank=True
    )

    def __str__(self):
        return self.title


# Таблиця для Рецептів
class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ("Diet Recipes", "Diet Recipes (Схуднення)"),
        ("Gaining Mass", "Gaining Mass (Набір маси)"),
        ("Recovery", "Recovery Recipes (Відновлення)"),
    ]
    title = models.CharField(max_length=200, verbose_name="Назва страви")
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, verbose_name="Категорія"
    )
    prep_time = models.IntegerField(verbose_name="Час приготування (хв)")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipes", verbose_name="Автор"
    )
    image = models.ImageField(
        upload_to="recipes_images/", blank=True, null=True, verbose_name="Фото"
    )
    instructions = models.TextField(
        verbose_name="Спосіб приготування", blank=True, null=True
    )

    favorites = models.ManyToManyField(
        User, related_name="favorite_recipes", blank=True
    )

    def __str__(self):
        return self.title


# Таблиця для Інгредієнтів
class Ingredient(models.Model):
    # Зв'язок: багато інгредієнтів належать одному рецепту
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="ingredients"
    )
    name = models.CharField(max_length=100, verbose_name="Назва продукту")
    weight = models.FloatField(verbose_name="Вага (г)")
    calories = models.FloatField(verbose_name="Калорії")
    protein = models.FloatField(verbose_name="Білки")
    fat = models.FloatField(verbose_name="Жири")
    carbs = models.FloatField(verbose_name="Вуглеводи")

    def __str__(self):
        return f"{self.name} - {self.weight}г"


class Profile(models.Model):
    # Зв'язуємо профіль зі стандартним юзером Django (один до одного)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Користувач",
    )
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True, verbose_name="Фото профілю"
    )

    # Спортивні метрики
    height = models.IntegerField(verbose_name="Ріст (см)", blank=True, null=True)
    weight = models.FloatField(verbose_name="Вага (кг)", blank=True, null=True)
    sport_type = models.CharField(
        max_length=100, verbose_name="Вид спорту", blank=True, null=True
    )
    daily_calories = models.IntegerField(
        verbose_name="Денна норма калорій", blank=True, null=True
    )

    # Збережені (улюблені) рецепти. Зв'язок "багато-до-багатьох", бо юзер може зберегти багато рецептів, а рецепт може бути збережений багатьма юзерами
    saved_recipes = models.ManyToManyField(
        Recipe, blank=True, related_name="saved_by", verbose_name="Збережені рецепти"
    )

    def __str__(self):
        return f"Профіль: {self.user.username}"

    # Ця функція спрацьовує автоматично, коли створюється новий User
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
