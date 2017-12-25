# tests.py
import os, sys
import unittest
from flask import abort, url_for
from flask_testing import TestCase

from app import create_app, db
from app.models import Department, Employee, Role

from test_base import TestBase

class MyTest(TestBase):
    def test_01_bad_registrations(self):
        #Test Registering with a bad email
        rv=self.register("testfirst","testsecond","bad_email","testuser","testpassword","testpassword",False)
        assert b'Invalid email address.' in rv.data, "###Test registering with a bad email: Failed to say invalid email"
        assert b'Register for an account' in rv.data, "###Test registering with a bad email: Failed to relaod registration page"
        
        #Test Registering with mismatched password
        rv=self.register("testfirst","testsecond","test@email.com","testuser","testpassword","badpassword",False)
        assert b'Invalid email address.' not in rv.data, "###Test registering with mismatched password: Email should be fine"
        assert b'Field must be equal to confirm_password' in rv.data, rv.data
        assert b'Register for an account' in rv.data, "###Test registering with a bad email: Failed to relaod registration page"

    def test_01_login_logout(self):
        #Login with malformed email
        rv = self.login('admin','wrongpassword')
        assert b'Login to your account' in rv.data, rv.data
        assert b'Invalid email address' in rv.data, rv.data
        
        #Login with email not in database
        rv = self.login('bad_email@walshis.com','wrongpassword')
        assert b'Login to your account' in rv.data, rv.data
        assert b'Invalid email or password' in rv.data, rv.data
        
        #Test Registering a user
        rv=self.register("testfirst","testsecond","test@email.com","testuser","testpassword","testpassword",False)
        assert b'Register for an account' not in rv.data, "###Test registering: Failed to go to dashboard page"
        assert b'<title>Login' in rv.data, "###Test registering: Failed to go to login page"

        #Login with valid user but incorrect password
        rv = self.login('test@email.com','wrongpassword')
        assert b'Login to your account' in rv.data, rv.data
        assert b'Invalid email or password' in rv.data, rv.data

        #Login with valid user and password
        rv = self.login('test@email.com','testpassword')
        assert b'<title>Dashboard' in rv.data, rv.data
        assert b'Hi, testuser!' in rv.data, rv.data

        #Logout when logged in
        target_url = url_for('auth.logout')
        redirect_url = url_for('auth.login')
        response = self.client.get(target_url)
        
        #Logout when already logged out
        target_url = url_for('auth.logout')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(302,response.status_code)
        self.assertRedirects(response, redirect_url)

    def test_02_403_forbidden(self):
        # create route to abort the request with the 403 Error
        @self.app.route('/403')
        def forbidden_error():
            abort(403)
        response = self.client.get('/403')
        self.assertEqual(response.status_code, 403)
        self.assertTrue(b"403 Error" in response.data)

    def test_03_404_not_found(self):
        response = self.client.get('/nothinghere')
        self.assertEqual(response.status_code, 404)
        self.assertTrue(b"404 Error" in response.data)

    def test_04_500_internal_server_error(self):
        # create route to abort the request with the 500 Error
        @self.app.route('/500')
        def forbidden_error():
            abort(500)
        response = self.client.get('/500')
        self.assertEqual(response.status_code, 500)
        self.assertTrue(b"500 Error" in response.data)

if __name__ == '__main__':
    unittest.main()
