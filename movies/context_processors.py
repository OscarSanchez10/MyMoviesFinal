from django.contrib.auth.models import User
# Importa el modelo de usuario predeterminado de Django.

def user_context(request):
    # Define una función llamada user_context que toma una solicitud (request) como argumento.

    return {
        'user_name': request.user.username if request.user.is_authenticated else 'Guest'
    }
    # Devuelve un diccionario con el nombre de usuario del usuario actual si está autenticado, de lo contrario, devuelve 'Guest'.
