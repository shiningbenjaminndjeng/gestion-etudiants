# etudiants/migrations/0002_add_matricule_m2m_unites.py
from django.db import migrations, models


def generate_matricules(apps, schema_editor):
    """Génère un matricule unique pour chaque étudiant existant."""
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("SELECT id FROM etudiants_etudiant ORDER BY id")
        rows = cursor.fetchall()
        for i, (etudiant_id,) in enumerate(rows, start=1):
            cursor.execute(
                "UPDATE etudiants_etudiant SET matricule = %s WHERE id = %s",
                [f'MAT{i:05d}', etudiant_id]
            )


def migrate_fk_to_m2m(apps, schema_editor):
    """Copie les anciennes relations FK unite -> M2M via SQL pur."""
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = 'etudiants_etudiant' AND column_name = 'unite_id'
        """)
        if cursor.fetchone() is None:
            return
        cursor.execute("""
            INSERT INTO etudiants_etudiant_unites (etudiant_id, uniteenseignement_id)
            SELECT id, unite_id FROM etudiants_etudiant
            WHERE unite_id IS NOT NULL
            ON CONFLICT DO NOTHING
        """)


class Migration(migrations.Migration):

    dependencies = [
        ('etudiants', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='etudiant',
            name='matricule',
            field=models.CharField(blank=True, default='', max_length=20, verbose_name='Matricule'),
        ),
        migrations.RunPython(generate_matricules, migrations.RunPython.noop),
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
        migrations.RunPython(migrate_fk_to_m2m, migrations.RunPython.noop),
        migrations.RemoveField(model_name='etudiant', name='unite'),
        migrations.AlterField(
            model_name='etudiant',
            name='matricule',
            field=models.CharField(max_length=20, unique=True, verbose_name='Matricule'),
        ),
    ]
