echo "BUILD START"
pip3 install -r requirement.txt
pip3 install django
python3.9 manage.py collectstatic --noinput --clear
echo "BUILD END"
