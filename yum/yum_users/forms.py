from django import forms
from core.models import IngredientType

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
        if IngredientType.objects.filter(nombre__iexact=nombre).exists():
            raise forms.ValidationError("Este nombre ya está registrado. Debe ser único.")
        return nombre