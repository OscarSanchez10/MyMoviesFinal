# Generated by Django 5.0.3 on 2024-04-12 21:34
# Este archivo de migración fue generado por Django 5.0.3 el 12 de abril de 2024 a las 21:34.

from django.db import migrations, models

class Migration(migrations.Migration):
    # Define una nueva migración.

    dependencies = [
        ('movies', '0002_job_person_movie_moviereview_moviecredit_and_more'),
    ]
    # Establece las dependencias de esta migración.

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='budget',
            field=models.IntegerField(),
        ),
        # Altera el campo 'budget' del modelo 'Movie' para ser un IntegerField.

        migrations.AlterField(
            model_name='movie',
            name='poster_path',
            field=models.URLField(),
        ),
        # Altera el campo 'poster_path' del modelo 'Movie' para ser un URLField.

        migrations.AlterField(
            model_name='movie',
            name='revenue',
            field=models.IntegerField(),
        ),
        # Altera el campo 'revenue' del modelo 'Movie' para ser un IntegerField.

        migrations.AlterField(
            model_name='movie',
            name='tmdb_id',
            field=models.IntegerField(unique=True),
        ),
        # Altera el campo 'tmdb_id' del modelo 'Movie' para ser un IntegerField único.
    ]
    # Define las operaciones de la migración.

