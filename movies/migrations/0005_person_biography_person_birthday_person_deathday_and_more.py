# Generated by Django 5.0.3 on 2024-05-19 07:27
# Este archivo de migración fue generado por Django 5.0.3 el 19 de mayo de 2024 a las 07:27.

from django.db import migrations, models

class Migration(migrations.Migration):
    # Define una nueva migración.

    dependencies = [
        ('movies', '0004_alter_movie_budget_alter_movie_poster_path_and_more'),
    ]
    # Establece las dependencias de esta migración.

    operations = [
        migrations.AddField(
            model_name='person',
            name='biography',
            field=models.TextField(blank=True, null=True),
        ),
        # Agrega el campo 'biography' al modelo 'Person' como un TextField opcional.

        migrations.AddField(
            model_name='person',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        # Agrega el campo 'birthday' al modelo 'Person' como un DateField opcional.

        migrations.AddField(
            model_name='person',
            name='deathday',
            field=models.DateField(blank=True, null=True),
        ),
        # Agrega el campo 'deathday' al modelo 'Person' como un DateField opcional.

        migrations.AddField(
            model_name='person',
            name='place_of_birth',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        # Agrega el campo 'place_of_birth' al modelo 'Person' como un CharField opcional.

        migrations.AddField(
            model_name='person',
            name='profile_path',
            field=models.URLField(blank=True, null=True),
        ),
        # Agrega el campo 'profile_path' al modelo 'Person' como un URLField opcional.

        migrations.AddField(
            model_name='person',
            name='tmdb_id',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
        # Agrega el campo 'tmdb_id' al modelo 'Person' como un IntegerField opcional, único y que puede ser nulo.
    ]
    # Define las operaciones de la migración.
