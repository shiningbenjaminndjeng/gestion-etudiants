#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

# ══════════════════════════════════════════════════════════════
# RESET PROPRE DES TABLES ETUDIANTS
# Supprime les anciennes tables cassées et repart de zéro.
# Idempotent : si les tables n'existent pas, aucune erreur.
# ══════════════════════════════════════════════════════════════
python manage.py shell << 'PYEOF'
from django.db import connection

with connection.cursor() as c:
    print(">>> Nettoyage des tables etudiants...")

    # Supprimer les tables dans le bon ordre (FK d'abord)
    c.execute("DROP TABLE IF EXISTS etudiants_etudiant_unites CASCADE;")
    c.execute("DROP TABLE IF EXISTS etudiants_etudiant CASCADE;")
    c.execute("DROP TABLE IF EXISTS etudiants_uniteenseignement CASCADE;")

    # Réinitialiser l'historique des migrations pour cette app
    c.execute("DELETE FROM django_migrations WHERE app = 'etudiants';")

    print(">>> Tables supprimées, historique de migration effacé.")

PYEOF

# Appliquer la migration unique propre
python manage.py migrate

echo ">>> Build terminé avec succès."
