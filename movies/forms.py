from django import forms
# Importa el módulo de formularios de Django.

from movies.models import MovieReview
# Importa el modelo MovieReview del módulo movies.models.

class ReviewForm(forms.ModelForm):
    # Define una clase de formulario llamada ReviewForm que hereda de forms.ModelForm.

    class Meta:
        # Define una clase interna Meta que proporciona metadatos para el formulario.

        model = MovieReview
        # Establece el modelo asociado al formulario como MovieReview.

        fields = ['rating', 'review']
        # Define los campos del formulario como 'rating' y 'review'.

        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'text-gray-400', 'min': 1, 'max': 100}),
            'review': forms.Textarea(attrs={'class': 'text-gray-400', 'rows': 3, 'cols': 60}),
        }
        # Define widgets para los campos del formulario. Aquí se especifica el tipo de entrada y los atributos HTML adicionales.

        labels = {
            'rating': 'Rating',
            'review': 'Review',
        }
        # Define etiquetas personalizadas para los campos del formulario.

        help_texts = {
            'rating': 'Rate the movie between 1 and 100.',
        }
        # Define textos de ayuda para los campos del formulario.

        error_messages = {
            'rating': {
                'required': 'Rating is required.',
                'min_value': 'Rating must be at least 1.',
                'max_value': 'Rating cannot be more than 100.',
            },
            'review': {
                'required': 'Review is required.',
            },
        }
        # Define mensajes de error personalizados para los campos del formulario.

