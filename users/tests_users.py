

import logging

from django.test import TestCase
from django.test.client import Client

from users.models import QuestrUserProfile
# from users.forms import QuestrUserCreationForm
# Create your tests here.
class SignupCase(TestCase):
    """Tests for User case"""
    def setUp(self):
        super(SignupCase, self).setUp()
        self.client = Client()
        self.username = "gaumire"
        self.first_name = "Gaurav"
        self.last_name = "Ghimire"
        self.password1 = "123456"
        self.password2 = "123456"
        self.email = "gaurav.ghimire@gmail.com"
        self.city = "Toronto"
        self.streetaddress = "16 Brookers Lane"
        self.postalcode = "M8V0A5"
        self.phonenum = "+1234567890"
        self.useraddress = dict(city=self.city,streetaddress=self.streetaddress,postalcode=self.postalcode)

        # useraddress = {}
        # useraddress['city'] = user_form.cleaned_data['city']
        # useraddress['address']=user_form.cleaned_data['address']
        # useraddress['postalcode']=user_form.cleaned_data['postalcode']

        self.post_data={'first_name':self.first_name,'last_name':self.last_name,'displayname':self.username,\
        'password1':self.password1,'password2':self.password2,'email':self.email, 'city':self.city, 'streetaddress':self.streetaddress,\
        'postalcode':self.postalcode, 'phonenum':self.phonenum}                        

    def test_signup_url(self):
        response = self.client.get('/user/signup/')
        self.assertEqual(response.status_code, 200)

    # def test_signup_validated(self):
    #     response = self.client.post('/user/signup/', data=self.post_data)
    #     # print dir(response)
    #     print response.content

    def test_user_is_created(self):
        response = self.client.post('/user/signup/', data=self.post_data)
        user = QuestrUserProfile.objects.get(email=self.email)
        # Signup should always redirect
        self.assertEqual(response.url, "http://testserver/user/home/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(user.displayname, self.username)

        #Testing after a user signs up and opens the same page when logged in
        response = self.client.get('/user/signup/')
        self.assertEqual(response.url, "http://testserver/user/home/")
        self.assertEqual(response.status_code, 302)

    def tests_superuser_created(self):
        # Testing a creation of a super user
        QuestrUserProfile.objects.create_superuser(self.email, self.password1)
        user = QuestrUserProfile.objects.get(email=self.email)
        self.assertEqual(user.is_superuser, True)
