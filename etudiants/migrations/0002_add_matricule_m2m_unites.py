# etudiants/migrations/0002_add_matricule_m2m_unites.py
import django.db.models.deletion
from django.db import migrations, models


def generate_matricules(apps, schema_editor):
    """Génère un matricule unique pour chaque étudiant existant."""
    Etudiant = apps.get_model('etudiants', 'Etudiant')
    for i, etudiant in enumerate(Etudiant.objects.order_by('id'), start=1):
        etudiant.matricule = f'MAT{i:05d}'
        etudiant.save(update_fields=['matricule'])


def migrate_unite_to_unites(apps, schema_editor):
    """Copie la relation FK unite → table M2M unites."""
    Etudiant = apps.get_model('etudiants', 'Etudiant')
    # On lit la colonne unite_id directement (l'ancien FK existe encore)
    for etudiant in Etudiant.objects.all():
        # unite_id est encore présent à ce stade de la migration
        unite_id = etudiant.unite_id if hasattr(etudiant, 'unite_id') else None
        if unite_id:
            etudiant.unites.add(unite_id)


class Migration(migrations.Migration):

    dependencies = [
        ('etudiants', '0001_initial'),
    ]

    operations = [
        # ── 1. Ajout matricule (nullable le temps de remplir les données) ──
        migrations.AddField(
            model_name='etudiant',
            name='matricule',
            field=models.CharField(
                blank=True, default='', max_length=20, verbose_name='Matricule'
            ),
        ),

        # ── 2. Génération des matricules pour les enregistrements existants ──
        migrations.RunPython(generate_matricules, migrations.RunPython.noop),

        # ── 3. Ajout de la relation M2M ──
        migrations.AddField(
            model_name='etudiant',
            name='unites',
            field=models.ManyToManyField(
                blank=True,
                related_name='etudiants',
                to='etudiants.uniteenseignement',
                verbose_name="Unités d'enseignement",
            ),
        ),

        # ── 4. Migration des données FK → M2M ──
        migrations.RunPython(migrate_unite_to_unites, migrations.RunPython.noop),

        # ── 5. Suppression de l'ancien FK unite ──
        migrations.RemoveField(
            model_name='etudiant',
            name='unite',
        ),

        # ── 6. Contrainte unique + champ obligatoire sur matricule ──
        migrations.AlterField(
            model_name='etudiant',
            name='matricule',
            field=models.CharField(
                max_length=20, unique=True, verbose_name='Matricule'
            ),
        ),
    ]
