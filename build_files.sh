echo "BUILD START"
python -m pip install -r requirements.txt
python manage.py collectstatics --noinput --clear
echo "BUILD END"
