# tests.py
import os, sys
import unittest
from flask import abort, url_for
from flask_testing import TestCase

from app import create_app, db
from app.models import Department, Employee, Role

from test_base import TestBase

class TestModels(TestBase):
    def test_employee_model(self):
        """Test number of records in Employee table"""
        self.assertEqual(Employee.query.count(), 2)
    def test_department_model(self):
        """Test number of records in Department table"""
        self.assertEqual(Department.query.count(), 0)
        # create test department
        department = Department(name="IT", description="The IT Department")
        # save department to database
        db.session.add(department)
        db.session.commit()
        self.assertEqual(Department.query.count(), 1)
        # retrive department from database
        it = Department.query.filter_by(name="IT").first()
        self.assertEqual(it.description, "The IT Department")
        # edit a department
        it.description="My IT Department"
        db.session.commit()
        newit = Department.query.filter_by(name="IT").first()
        self.assertEqual(it.description, "My IT Department")

    def test_role_model(self):
        """Test number of records in Role table"""
        self.assertEqual(Role.query.count(), 0)
        # create test department
        role = Role(name="CEO", description="Run the whole company")
        # save department to database
        db.session.add(role)
        db.session.commit()
        self.assertEqual(Role.query.count(), 1)

#class TestViews(TestBase):
    def test_homepage_view(self):
        """Tes that the homepage is accessible without login"""
        response = self.client.get(url_for('home.homepage'))
        self.assertEqual(response.status_code, 200)
    def test_login_view(self):
        """Test that login page is accessible without login"""
        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)
    def test_logout_view(self):
        """Test that logout page is inaccessible without login
           and redirects to login page then to logout"""
        target_url = url_for('auth.logout')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)
    def test_dashboard_view(self):
        """Test that dashboard page is inaccessible without login
           and redirects to login page then to dashboard"""
        target_url = url_for('home.dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)
    def test_admin_dashboard_view(self):
        """Test that admin dashboard page is inaccessible without login
           and redirects to login page then to admin dashboard"""
        target_url = url_for('home.admin_dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)
    def test_departments_view(self):
        """Test that departments page is inaccessible without login
           and redirects to login page then to departments page"""
        target_url = url_for('admin.list_departments')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)
    def test_roles_view(self):
        """Test that roles page is inaccessible without login
           and redirects to login page then to roles page"""
        target_url = url_for('admin.list_roles')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)
    def test_employees_view(self):
        """Test that employees page is inaccessible without login
           and redirects to login page then to employees page"""
        target_url = url_for('admin.list_employees')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

#class TestErrorPages(TestBase):
    def test_403_forbidden(self):
        # create route to abort the request with the 403 Error
        @self.app.route('/403')
        def forbidden_error():
            abort(403)
        response = self.client.get('/403')
        self.assertEqual(response.status_code, 403)
        self.assertTrue(b"403 Error" in response.data)
    def test_404_not_found(self):
        response = self.client.get('/nothinghere')
        self.assertEqual(response.status_code, 404)
        self.assertTrue(b"404 Error" in response.data)
    def test_500_internal_server_error(self):
        # create route to abort the request with the 500 Error
        @self.app.route('/500')
        def forbidden_error():
            abort(500)
        response = self.client.get('/500')
        self.assertEqual(response.status_code, 500)
        self.assertTrue(b"500 Error" in response.data)

if __name__ == '__main__':
    unittest.main()
