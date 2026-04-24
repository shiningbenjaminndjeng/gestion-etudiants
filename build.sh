#!/usr/bin/env bash
set -o errexit
 
pip install -r requirements.txt
 
python manage.py collectstatic --no-input
 
# ✅ Forcer la migration meme si la DB a déjà des tables
python manage.py migrate --run-syncdb
 
