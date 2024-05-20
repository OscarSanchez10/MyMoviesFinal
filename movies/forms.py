from django import forms
from movies.models import MovieReview

class ReviewForm(forms.ModelForm):
    class Meta:
        model = MovieReview
        fields = ['rating', 'review']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'text-gray-400', 'min': 1, 'max': 100}),
            'review': forms.Textarea(attrs={'class': 'text-gray-400', 'rows': 3, 'cols': 60}),
        }
        labels = {
            'rating': 'Rating',
            'review': 'Review',
        }
        help_texts = {
            'rating': 'Rate the movie between 1 and 100.',
        }
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
