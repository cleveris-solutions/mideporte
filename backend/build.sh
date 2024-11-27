#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r ../requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

python populate_db.py

# Apply any outstanding database migrations
python manage.py migrate

#frontend setup
cd ../frontend

npm install
npm run build

cd ../backend
python manage.py collectstatic --noinput
