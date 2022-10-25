pip3 install virtualenv
virtualenv --system-site-packages -p `which python3` --seeder=pip venv
source venv/bin/activate
if [ -e requirements.txt ]; then pip3 install -r requirements.txt --upgrade-strategy=eager; fi