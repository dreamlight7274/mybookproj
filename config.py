# database config
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'bookproj'
USERNAME = 'root'
PASSWORD = 'root'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

# session secretkey
SECRET_KEY = 'library'