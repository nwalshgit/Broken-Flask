# tests.py
import os, sys
import unittest
from flask import abort, url_for
from flask_testing import TestCase
from flask_login import current_user

from app import create_app, db
from app.models import Department, Employee, Role
from app.admin.views import list_departments

from test_base import TestBase

class MyTest(TestBase):
    """Test Departments, Roles, Employee Pages"""
    def test_01_department_pages(self):
        #Test Registering a user
        testuser = Employee(first_name="testfirst",last_name="testlast",email="test@email.com",username="testuser",password="testpassword",is_admin=False)
        testadmin = Employee(first_name="adminfirst",last_name="adminsecond",email="admin@email.com",username="testadmin",password="testpassword",is_admin=True)
        db.session.add(testuser)
        db.session.add(testadmin)
        
        #Test going to departments with non-admin user
        target_url = url_for('admin.list_departments')
        redirect_url = url_for('auth.login')
        response = self.client.get(target_url)
        self.assertEqual(302,response.status_code, "###Test depertment pages: without logging in")
        #self.assertRedirects(response, redirect_url)
        #self.assertTrue(b"302 Error" in response.data)

        #TODO
        assert False, "Tests are not finished"
        self.login("testuser","testpassword")
        response = self.client.get(url_for('admin.list_departments'), follow_redirects=True)
        #rv=list_departments()
        print("Response:",response.data)
        #print("Response",rv,"\nCode",rv.status_code,"\nData:",rv.data)


        #Logout when already logged out
        #target_url = url_for('auth.logout')
        #redirect_url = url_for('auth.login', next=target_url)
        #response = self.client.get(target_url)
        #self.assertEqual(302,response.status_code)
        #self.assertRedirects(response, redirect_url)
        #self.assertTrue(b"403 Error" in response.data)

if __name__ == '__main__':
    unittest.main()
