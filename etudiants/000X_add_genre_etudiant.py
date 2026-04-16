# etudiants/migrations/000X_add_genre_etudiant.py
# Générez automatiquement via : python manage.py makemigrations
# Ce fichier est fourni à titre indicatif.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etudiants', '0001_initial'),   # ← ajustez selon votre dernière migration
    ]

    operations = [
        migrations.AddField(
            model_name='etudiant',
            name='genre',
            field=models.CharField(
                choices=[('M', 'Masculin'), ('F', 'Féminin')],
                default='M',
                max_length=1,
                verbose_name='Genre',
            ),
        ),
    ]
