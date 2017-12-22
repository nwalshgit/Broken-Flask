echo "Upgrading pip..."
pip install --upgrade pip
echo "Installing ConfigParser (converts text file in python dict)..."
pip install ConfigParser
echo "Installing mysqlclient (has mysql_config)..."
pip install mysqlclient
echo "Installing pymysql (needed for python3 connections to mysql)..."
pip install pymysql
echo "Installing Flask (webserver)..."
pip install Flask
echo "Installing Flask-SQLAlchemy (wraps DB in flask objects)..."
pip install Flask-SQLAlchemy
echo "Installing flask-login (tools for handy authentication hashes)..."
pip install flask-login
echo "Installing flask-migrate (provides db changes when objects changed)..."
pip install flask-migrate
echo "Installing WTForms-SQLAlchemy (wraps DB in forms)..."
pip install WTForms-SQLAlchemy
echo "Installing Flask-WTF (tools for secure forms, captcha)..."
pip install Flask-WTF
echo "Installing flask-bootstrap (allows use of wtf and utils libraries)..."
pip install flask-bootstrap
echo "Installing Flask-Testing (allows the use of unittesting)..."
pip install Flask-Testing
