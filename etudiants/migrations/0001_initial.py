# etudiants/migrations/0001_initial.py
# Migration complète incluant TOUS les champs (genre inclus)
# Supprimez tous les anciens fichiers de migration et utilisez SEULEMENT celui-ci

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='UniteEnseignement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_unite', models.CharField(max_length=200)),
                ('nom_prof', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': "Unité d'enseignement",
                'ordering': ['nom_unite'],
            },
        ),
        migrations.CreateModel(
            name='Etudiant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('date_naissance', models.DateField()),
                ('lieu_naissance', models.CharField(max_length=150)),
                ('age', models.PositiveIntegerField()),
                ('ethnie', models.CharField(blank=True, max_length=100)),
                ('genre', models.CharField(
                    choices=[('M', 'Masculin'), ('F', 'Féminin')],
                    default='M',
                    max_length=1,
                    verbose_name='Genre',
                )),
                ('unite', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='etudiants',
                    to='etudiants.uniteenseignement',
                )),
                ('date_inscription', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Étudiant',
                'ordering': ['nom', 'prenom'],
            },
        ),
    ]
