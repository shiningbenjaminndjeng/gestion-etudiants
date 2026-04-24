# etudiants/migrations/0002_add_matricule_m2m_unites.py
#
# CORRECTION CRITIQUE :
#   Le FK "unite" (0001) et le M2M "unites" (0002) avaient tous les deux
#   related_name='etudiants' → clash Django → rollback → 500 partout.
#   Solution : le M2M utilise un related_name temporaire ('etudiants_tmp')
#   pendant la coexistence, puis on le renomme en 'etudiants' après
#   suppression du FK.

from django.db import migrations, models


def generate_matricules(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("SELECT id FROM etudiants_etudiant ORDER BY id")
        rows = cursor.fetchall()
        for i, (etudiant_id,) in enumerate(rows, start=1):
            cursor.execute(
                "UPDATE etudiants_etudiant SET matricule = %s WHERE id = %s",
                [f'MAT{i:05d}', etudiant_id]
            )


def migrate_fk_to_m2m(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = 'etudiants_etudiant'
              AND column_name = 'unite_id'
        """)
        if cursor.fetchone() is None:
            return
        cursor.execute("""
            INSERT INTO etudiants_etudiant_unites (etudiant_id, uniteenseignement_id)
            SELECT id, unite_id
            FROM etudiants_etudiant
            WHERE unite_id IS NOT NULL
            ON CONFLICT DO NOTHING
        """)


class Migration(migrations.Migration):

    dependencies = [
        ('etudiants', '0001_initial'),
    ]

    operations = [

        # ── 1. Ajout matricule (nullable d'abord) ─────────────────────────
        migrations.AddField(
            model_name='etudiant',
            name='matricule',
            field=models.CharField(
                blank=True, default='', max_length=20, verbose_name='Matricule'
            ),
        ),

        # ── 2. Génération des matricules pour les lignes existantes ────────
        migrations.RunPython(generate_matricules, migrations.RunPython.noop),

        # ── 3. Ajout M2M avec related_name TEMPORAIRE ──────────────────────
        #       NE PAS utiliser 'etudiants' ici : le FK 'unite' l'utilise
        #       déjà → SystemCheckError → rollback → 500.
        migrations.AddField(
            model_name='etudiant',
            name='unites',
            field=models.ManyToManyField(
                blank=True,
                related_name='etudiants_tmp',           # ← temporaire
                to='etudiants.uniteenseignement',
                verbose_name="Unités d'enseignement",
            ),
        ),

        # ── 4. Copie des données FK → M2M (SQL pur) ───────────────────────
        migrations.RunPython(migrate_fk_to_m2m, migrations.RunPython.noop),

        # ── 5. Suppression du FK 'unite' (libère related_name='etudiants') ─
        migrations.RemoveField(
            model_name='etudiant',
            name='unite',
        ),

        # ── 6. Renommage related_name temporaire → 'etudiants' définitif ──
        migrations.AlterField(
            model_name='etudiant',
            name='unites',
            field=models.ManyToManyField(
                blank=True,
                related_name='etudiants',               # ← nom définitif
                to='etudiants.uniteenseignement',
                verbose_name="Unités d'enseignement",
            ),
        ),

        # ── 7. Matricule unique et obligatoire ─────────────────────────────
        migrations.AlterField(
            model_name='etudiant',
            name='matricule',
            field=models.CharField(
                max_length=20, unique=True, verbose_name='Matricule'
            ),
        ),
    ]
