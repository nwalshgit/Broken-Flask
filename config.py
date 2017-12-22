#https://scotch.io/tutorials/build-a-crud-web-app-with-python-and-flask-part-one

# config.py

class Config(object):
    """Common Configurations"""
    #Put any configurations here that are common across all environments
    DEBUG = True

class DevelopmentConfig(Config):
    """Development configurations"""
    # Statement for enabling the devielopment environment
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """Production configuration """
    DEBUG = False

class TestingConfig(Config):
    """Testing configurations"""
    TESTING = True

app_config = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
}

#  https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications
# Define the application directory
#import os
#BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database - we are working with
# SQLite for this example
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
#SQLALCHEMY_DATABASE_URI = 'mysql:///' + os.path.join(BASE_DIR, 'app.db')
#DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
#THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
#CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
#CSRF_SESSION_KEY = "sdkf8"

# Secret key for signing cookies
#SECRET_KEY = "sdkf8"
