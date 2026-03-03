set -o errexit

# Change to root directory where requirements.txt is located
cd "$(dirname "$0")/.."

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate --noinput

if [[ "${CREATE_SUPERUSER,,}" == "true" ]]; then
    py manage.py create_superuser --noinput 
    
"
fi
