from django import forms


class NameForm(forms.Form):
    your_name = forms.CharField(label="Nombre",help_text="100 car. max.", max_length=100, 
    error_messages={"required": "El nombre es obligatorio"},
    widget=forms.Textarea(attrs={"class":"text-gray-400", "rows": 3, "cols": 60})
)
