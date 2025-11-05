from django.test import TestCase
from django.urls import reverse
from core.models import User, Recipe, IngredientType
from datetime import timedelta
from unittest.mock import patch


class FavoriteViewTest(TestCase):
    def setUp(self):
        self.patcher = patch("core.models.calculate_nutritional_value", return_value=0)
        self.mock_calc = self.patcher.start()

        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")
        self.recipe = Recipe.objects.create(
            user=self.user,
            title="Receta favorita",
            description="Descripción",
            category="postre",
            preparation_time=timedelta(minutes=30),
            portions=4
        )
        self.user.favorite_recipes.add(self.recipe)

    def tearDown(self):
        self.patcher.stop()

    def test_favorite_list_view(self):
        response = self.client.get(reverse("favorites"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Receta favorita")



class IngredientTypeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_create_ingredient_type(self):
        tipo = IngredientType.objects.create(
            nombre="Zanahoria",
            category="vegetal",
            user=self.user
        )
        self.assertEqual(tipo.nombre, "zanahoria")  # se guarda en minúsculas
        self.assertEqual(tipo.category, "vegetal")
        self.assertEqual(tipo.user, self.user)
