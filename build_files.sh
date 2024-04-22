echo "BUILD START"
pip3 install -r requirement.txt
python3.9 manage.py collectstatic --noinput --clear
echo "BUILD END"
