# etudiants/migrations/0002_add_matricule_m2m_unites.py
#
# CORRECTION : L'ancienne version créait un conflit de related_name='etudiants'
# car le FK 'unite' et le M2M 'unites' avaient le même reverse accessor.
# FIX : on supprime d'abord le FK, PUIS on ajoute le M2M.
# Les données sont sauvegardées via SQL brut entre les deux opérations.

import django.db.models.deletion
from django.db import migrations, models

# Dictionnaire global pour transporter les données entre les étapes RunPython
_unite_mapping = {}


def generate_matricules(apps, schema_editor):
    """Génère MAT00001, MAT00002… pour chaque étudiant existant."""
    Etudiant = apps.get_model('etudiants', 'Etudiant')
    for i, etudiant in enumerate(Etudiant.objects.order_by('id'), start=1):
        etudiant.matricule = f'MAT{i:05d}'
        etudiant.save(update_fields=['matricule'])


def save_unite_ids(apps, schema_editor):
    """
    Lit unite_id (FK) en SQL brut AVANT de supprimer la colonne.
    Stocke le résultat dans _unite_mapping = { etudiant_id: unite_id }.
    """
    global _unite_mapping
    _unite_mapping = {}
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, unite_id FROM etudiants_etudiant WHERE unite_id IS NOT NULL"
            )
            for row in cursor.fetchall():
                _unite_mapping[row[0]] = row[1]
    except Exception:
        pass  # Si la colonne n'existe pas (base vierge), on ignore


def restore_unites_m2m(apps, schema_editor):
    """
    Recrée les relations dans la table M2M (après ajout du champ unites).
    Utilise le dictionnaire rempli par save_unite_ids.
    """
    global _unite_mapping
    if not _unite_mapping:
        return
    Etudiant = apps.get_model('etudiants', 'Etudiant')
    for etudiant_id, unite_id in _unite_mapping.items():
        try:
            e = Etudiant.objects.get(id=etudiant_id)
            e.unites.add(unite_id)
        except Exception:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('etudiants', '0001_initial'),
    ]

    operations = [
        # ── 1. Ajouter matricule (vide au départ) ─────────────────────────────
        migrations.AddField(
            model_name='etudiant',
            name='matricule',
            field=models.CharField(
                blank=True, default='', max_length=20, verbose_name='Matricule'
            ),
        ),

        # ── 2. Générer les matricules pour les lignes existantes ───────────────
        migrations.RunPython(generate_matricules, migrations.RunPython.noop),

        # ── 3. Sauvegarder les unite_id en mémoire (SQL brut) ─────────────────
        migrations.RunPython(save_unite_ids, migrations.RunPython.noop),

        # ── 4. Supprimer l'ancien FK 'unite' ─────────────────────────────────
        #       → le related_name='etudiants' est libéré AVANT d'ajouter le M2M
        migrations.RemoveField(
            model_name='etudiant',
            name='unite',
        ),

        # ── 5. Ajouter le M2M 'unites' (related_name libre maintenant) ────────
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

        # ── 6. Restaurer les relations dans la table M2M ──────────────────────
        migrations.RunPython(restore_unites_m2m, migrations.RunPython.noop),

        # ── 7. Rendre matricule unique et obligatoire ─────────────────────────
        migrations.AlterField(
            model_name='etudiant',
            name='matricule',
            field=models.CharField(
                max_length=20, unique=True, verbose_name='Matricule'
            ),
        ),
    ]
