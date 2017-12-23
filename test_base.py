# tests.py
import os, sys
import unittest
from flask import abort, url_for
from flask_testing import TestCase

from app import create_app, db
from app.models import Department, Employee, Role

class TestBase(TestCase):
    def create_app(self):
        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(SQLALCHEMY_DATABASE_URI='mysql://unittestuser:unittestpassword@localhost/unittestdb')
        app.config.update(WTF_CSRF_ENABLED = False)
        return app

    def setUp(self):
        """Will be called before every test"""
        db.create_all()
        # create test admin user
        admin = Employee(username="admin", password="admin20", is_admin=True)
        # create test non-admin user
        employee = Employee(username="test_uesr", password="test20")
        # save users to database
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()

    def tearDown(self):
        """Will be called after every test"""
        db.session.remove()
        db.drop_all()

    """Define functions to load login and logout webpages"""
    def register(self, first_name,last_name,email,username,password,confirm_password,admin):
        rv = self.client.post('/register', data=dict(email=email,username=username,first_name=first_name,last_name=last_name,password=password,confirm_password=confirm_password,submit='Register'), follow_redirects=True)
        return(rv)
        #return Employee(email=email, username=username,password=password,is_admin=admin)

    def login(self, email,password):
        return self.client.post('/login', data=dict(email=email,password=password), follow_redirects=True)

def logout(self):
        return self.client.get('/logout', follow_redirects=True)

if __name__ == '__main__':
    unittest.main()
