from django import forms
from django.forms import inlineformset_factory
from core.models import IngredientType, Ingredient, Instruction, Recipe, Review

class CommaSeparatedListField(forms.CharField):
    def to_python(self, value):
        if not value:
            return []
        return [item.strip() for item in value.split(",")]

    def prepare_value(self, value):
        if isinstance(value, list):
            return ", ".join(value)
        return value


class IngredientTypeForm(forms.ModelForm):
    vitamins = CommaSeparatedListField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ej: Vitamina A, Vitamina C"
        })
    )
    excesses = CommaSeparatedListField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ej: Sodio, Azúcar"
        })
    )

    class Meta:
        model = IngredientType
        fields = ["nombre", "category", "vitamins", "excesses"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
        }
    
    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()
        qs = IngredientType.objects.filter(nombre__iexact=nombre)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Ya existe un tipo de ingrediente con este nombre.")

        return nombre


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["ingredient_type", "quantity", "unit"]
        widgets = {
            "ingredient_type": forms.Select(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "unit": forms.TextInput(attrs={"class": "form-control"}),
        }

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "description", "category", "preparation_time", "portions"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4,'class': 'form-control rounded' }),
            "preparation_time": forms.TextInput(attrs={"placeholder": "Ejemplo: 1:30:00 para 1h 30min", 'class': 'form-control rounded'}),
            "title": forms.TextInput(attrs={'class': 'form-control rounded'}),
            "category": forms.Select(attrs={'class': 'form-control rounded'}),
            "portions": forms.NumberInput(attrs={'class': 'form-control rounded'}),
        }

class InstructionForm(forms.ModelForm):
    class Meta:
        model = Instruction
        fields = ["title", "details", "complexity", "n_step"]
        widgets = {
            "details": forms.Textarea(attrs={"rows": 3, 'class': 'form-control rounded'}),
            "title": forms.TextInput(attrs={'class': 'form-control rounded'}),
            "complexity": forms.NumberInput(attrs={'class': 'form-control rounded', 'placeholder': '1-5'}),
            "n_step": forms.NumberInput(attrs={'class': 'form-control rounded'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["score", "comment"]
        widgets = {
            "score": forms.NumberInput(attrs={"min": 0, "max": 5, "class": "form-control"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }