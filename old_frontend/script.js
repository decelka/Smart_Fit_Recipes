// Наша база даних рецептів
const recipes = [
    {
        id: 1,
        title: "Морквяно-гарбузові котлети в аерогрилі",
        category: "Схуднення",
        prepTimeMinutes: 20,
        ingredients: [
            { name: "Гарбуз (м'якоть)", weightGrams: 200, calories: 26, protein: 1.0, fat: 0.1, carbs: 6.5 },
            { name: "Морква", "weightGrams": 150, calories: 41, protein: 0.9, fat: 0.2, carbs: 9.6 },
            { name: "Яйце куряче", "weightGrams": 50, calories: 78, protein: 6.0, fat: 5.0, carbs: 0.5 }
        ]
    },
    {
        id: 2,
        title: "Відновлювальний смузі (після Муай-тай)",
        category: "Набір маси",
        prepTimeMinutes: 5,
        ingredients: [
            { name: "Протеїн сироватковий", weightGrams: 30, calories: 113, protein: 24.0, fat: 1.5, carbs: 2.0 },
            { name: "Банан", weightGrams: 120, calories: 89, protein: 1.1, fat: 0.3, carbs: 22.8 }
        ]
    },
    {
        id: 3,
        title: "Куряче філе з броколі",
        category: "Підтримання форми",
        prepTimeMinutes: 25,
        ingredients: [
            { name: "Куряче філе", weightGrams: 200, calories: 220, protein: 46.0, fat: 2.4, carbs: 0.0 },
            { name: "Броколі", weightGrams: 150, calories: 51, protein: 4.2, fat: 0.6, carbs: 9.9 }
        ]
    }
];

// Знаходимо HTML-елементи за їхніми ID
const recipeContainer = document.getElementById('recipe-container');
const categoryFilter = document.getElementById('category-filter');
const exportBtn = document.getElementById('export-btn');

// Функція для відображення рецептів на сторінці
function renderRecipes(recipesToRender) {
    // Очищаємо контейнер перед кожним новим малюванням (корисно для фільтрів)
    recipeContainer.innerHTML = '';

    // Проходимося по кожному рецепту в масиві
    recipesToRender.forEach(recipe => {
        // Створюємо HTML-елемент для однієї картки
        const card = document.createElement('div');
        card.className = 'recipe-card';

        // Змінні для підрахунку загального КБЖВ
        let totalCalories = 0;
        let totalProtein = 0;
        let totalFat = 0;
        let totalCarbs = 0;

        // Збираємо інгредієнти у список
        let ingredientsListHTML = '';

        recipe.ingredients.forEach(ing => {
            totalCalories += ing.calories;
            totalProtein += ing.protein;
            totalFat += ing.fat;
            totalCarbs += ing.carbs;

            ingredientsListHTML += `<li>${ing.name}: ${ing.weightGrams}г</li>`;
        });

        // Наповнюємо картку інформацією
        card.innerHTML = `
            <h2 style="color: #2c3e50; font-size: 20px; margin-bottom: 10px;">${recipe.title}</h2>
            <p><strong>Категорія:</strong> ${recipe.category}</p>
            <p><strong>Час приготування:</strong> ${recipe.prepTimeMinutes} хв</p>
            <hr style="margin: 15px 0; border: 0; border-top: 1px solid #eee;">
            <h3 style="font-size: 16px; margin-bottom: 10px;">Інгредієнти:</h3>
            <ul style="list-style-type: circle; margin-left: 20px; margin-bottom: 15px; color: #555;">
                ${ingredientsListHTML}
            </ul>
            <div style="background: #e8f6f3; padding: 10px; border-radius: 5px; font-size: 14px;">
                <strong style="color: #16a085;">Загальне КБЖВ порції:</strong><br>
                Калорії: ${totalCalories.toFixed(1)} ккал<br>
                Б: ${totalProtein.toFixed(1)} г | Ж: ${totalFat.toFixed(1)} г | В: ${totalCarbs.toFixed(1)} г
            </div>
        `;

        // Додаємо готову картку на сторінку
        recipeContainer.appendChild(card);
    });
}

// Запускаємо функцію при першому завантаженні сторінки
renderRecipes(recipes);

// Підпункт 2.3: Робота фільтра за категоріями
categoryFilter.addEventListener('change', function () {
    // Отримуємо те, що вибрав користувач (наприклад, "Схуднення")
    const selectedCategory = categoryFilter.value;

    if (selectedCategory === 'all') {
        // Якщо вибрано "Усі категорії", показуємо весь масив
        renderRecipes(recipes);
    } else {
        // Фільтруємо масив: залишаємо тільки ті рецепти, де категорія збігається
        const filteredRecipes = recipes.filter(recipe => recipe.category === selectedCategory);
        renderRecipes(filteredRecipes);
    }
});

// Підпункт 2.4: Генерація та скачування файлу .txt
exportBtn.addEventListener('click', function () {
    // Дивимося, які рецепти зараз на екрані (залежно від фільтра)
    const selectedCategory = categoryFilter.value;
    let recipesToExport = recipes;

    if (selectedCategory !== 'all') {
        recipesToExport = recipes.filter(recipe => recipe.category === selectedCategory);
    }

    // Формуємо текстовий рядок, який стане нашим файлом
    let fileContent = "ВІД ЗАВТРА НА ДІЄТІ: СПИСОК ПОКУПОК\n";
    fileContent += "========================================\n\n";

    recipesToExport.forEach(recipe => {
        fileContent += `--- Страва: ${recipe.title} ---\n`;
        recipe.ingredients.forEach(ing => {
            fileContent += `• ${ing.name} - ${ing.weightGrams}г\n`;
        });
        fileContent += "\n";
    });

    // Створюємо Blob (віртуальний файл у пам'яті браузера)
    const blob = new Blob([fileContent], { type: "text/plain;charset=utf-8" });

    // Створюємо невидиме посилання (тег <a>), "клікаємо" по ньому і видаляємо
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = "shopping_list.txt"; // Назва файлу при завантаженні

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
});