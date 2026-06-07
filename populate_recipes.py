import os
import django
import requests
from django.core.files.base import ContentFile

# Налаштування оточення Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from recipes.models import Recipe, Ingredient
from django.contrib.auth.models import User


def populate():
    print("🚀 Запускаємо наповнення бази з інгредієнтами, КБЖВ та фотками...")
    author = User.objects.first()

    if not author:
        print("❌ Помилка: Створи хоча б одного юзера (адміна) в базі!")
        return

    # Повний список рецептів з чіткими макросами
    recipes_data = [
        # --- НА СУШКУ ---
        {
            "title": "Гарбузово-морквяні фітнес-котлети",
            "category": "Diet Recipes",
            "prep_time": 40,
            "instructions": "Натерти гарбуз та моркву, віджати вологу. Додати яйце, борошно та спеції. Зліпити котлетки і запікати 30 хв при 180°C.",
            "img_url": "https://images.unsplash.com/photo-1548943487-a2e4e43b4851?w=800",
            "ingredients": [
                {
                    "name": "Гарбуз (м'якоть)",
                    "weight": 300,
                    "calories": 78,
                    "protein": 3,
                    "fat": 0,
                    "carbs": 20,
                },
                {
                    "name": "Морква",
                    "weight": 200,
                    "calories": 82,
                    "protein": 2,
                    "fat": 0,
                    "carbs": 14,
                },
                {
                    "name": "Яйце куряче",
                    "weight": 50,
                    "calories": 78,
                    "protein": 6,
                    "fat": 5,
                    "carbs": 0,
                },
                {
                    "name": "Вівсяне борошно",
                    "weight": 30,
                    "calories": 110,
                    "protein": 4,
                    "fat": 2,
                    "carbs": 20,
                },
            ],
        },
        {
            "title": "Куряче філе з диким рисом",
            "category": "Diet Recipes",
            "prep_time": 30,
            "instructions": "Рис відварити. Філе обсмажити на грилі без олії. Броколі бланшувати в окропі 3 хвилини.",
            "img_url": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=800",
            "ingredients": [
                {
                    "name": "Куряче філе",
                    "weight": 200,
                    "calories": 220,
                    "protein": 46,
                    "fat": 3,
                    "carbs": 0,
                },
                {
                    "name": "Дикий рис",
                    "weight": 80,
                    "calories": 285,
                    "protein": 12,
                    "fat": 1,
                    "carbs": 60,
                },
                {
                    "name": "Броколі",
                    "weight": 100,
                    "calories": 34,
                    "protein": 3,
                    "fat": 0,
                    "carbs": 7,
                },
            ],
        },
        # --- НА МАСУ ---
        {
            "title": "Свинячий стейк у винному соусі",
            "category": "Gaining Mass",
            "prep_time": 25,
            "instructions": "Стейк обсмажити по 3 хв з кожного боку, зняти. У сковорідку влити вино, додати масло, випарувати до густоти. Полити соусом м'ясо.",
            "img_url": "https://images.unsplash.com/photo-1600891964092-4316c288032e?w=800",
            "ingredients": [
                {
                    "name": "Свинячий стейк (ошийок)",
                    "weight": 300,
                    "calories": 720,
                    "protein": 48,
                    "fat": 55,
                    "carbs": 0,
                },
                {
                    "name": "Червоне сухе вино",
                    "weight": 100,
                    "calories": 85,
                    "protein": 0,
                    "fat": 0,
                    "carbs": 3,
                },
                {
                    "name": "Вершкове масло",
                    "weight": 30,
                    "calories": 215,
                    "protein": 0,
                    "fat": 24,
                    "carbs": 0,
                },
                {
                    "name": "Часник",
                    "weight": 10,
                    "calories": 15,
                    "protein": 1,
                    "fat": 0,
                    "carbs": 3,
                },
            ],
        },
        {
            "title": "Тяжка паста з яловичиною",
            "category": "Gaining Mass",
            "prep_time": 35,
            "instructions": "Відварити пасту. Фарш обсмажити, залити томатним пюре, тушкувати 5 хв. Змішати з пастою і посипати сиром.",
            "img_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800",
            "ingredients": [
                {
                    "name": "Паста з твердих сортів",
                    "weight": 120,
                    "calories": 420,
                    "protein": 14,
                    "fat": 2,
                    "carbs": 85,
                },
                {
                    "name": "Яловичий фарш",
                    "weight": 200,
                    "calories": 500,
                    "protein": 34,
                    "fat": 40,
                    "carbs": 0,
                },
                {
                    "name": "Томатне пюре",
                    "weight": 150,
                    "calories": 60,
                    "protein": 3,
                    "fat": 0,
                    "carbs": 10,
                },
                {
                    "name": "Сир Пармезан",
                    "weight": 20,
                    "calories": 80,
                    "protein": 7,
                    "fat": 6,
                    "carbs": 1,
                },
            ],
        },
        # --- ВІДНОВЛЕННЯ ---
        {
            "title": "Тайський смузі для бійців",
            "category": "Recovery",
            "prep_time": 5,
            "instructions": "Закинути всі інгредієнти в блендер, збити до однорідної густої маси. Пити одразу після спарингів.",
            "img_url": "https://images.unsplash.com/photo-1553530666-ba11a7da3888?w=800",
            "ingredients": [
                {
                    "name": "Мигдальне молоко",
                    "weight": 200,
                    "calories": 30,
                    "protein": 1,
                    "fat": 2,
                    "carbs": 3,
                },
                {
                    "name": "Стиглий банан",
                    "weight": 150,
                    "calories": 134,
                    "protein": 2,
                    "fat": 0,
                    "carbs": 35,
                },
                {
                    "name": "Сироватковий протеїн",
                    "weight": 30,
                    "calories": 120,
                    "protein": 24,
                    "fat": 2,
                    "carbs": 3,
                },
                {
                    "name": "Арахісова паста",
                    "weight": 20,
                    "calories": 118,
                    "protein": 5,
                    "fat": 10,
                    "carbs": 4,
                },
            ],
        },
    ]

    for data in recipes_data:
        # Видаляємо дублікати перед створенням
        Recipe.objects.filter(title=data["title"]).delete()

        # Створюємо рецепт
        recipe = Recipe.objects.create(
            title=data["title"],
            category=data["category"],
            prep_time=data["prep_time"],
            instructions=data["instructions"],
            author=author,
        )

        # Качаємо картинку з інтернету
        try:
            response = requests.get(data["img_url"], timeout=10)
            if response.status_code == 200:
                filename = f"seeded_{data['title'].lower().replace(' ', '_')[:15]}.jpg"
                recipe.image.save(filename, ContentFile(response.content), save=False)
        except Exception as e:
            print(f"⚠️ Не вдалося стягнути фото для {data['title']}: {e}")

        recipe.save()

        # Заповнюємо інгредієнти
        for ing in data["ingredients"]:
            Ingredient.objects.create(
                recipe=recipe,
                name=ing["name"],
                weight=ing["weight"],
                calories=ing["calories"],
                protein=ing["protein"],
                fat=ing["fat"],
                carbs=ing["carbs"],
            )

        print(f"✅ Додано: {data['title']}")

    print("🔥 Фініш! Всі рецепти та інгредієнти успішно збережено в базу.")


if __name__ == "__main__":
    populate()
