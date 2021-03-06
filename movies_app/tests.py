from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from .serializers import *


class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username="testuser",
                                        email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            self.assertIsNotNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
            User.objects.create_user(email='')
            User.objects.create_user(email='normal@user.com', password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(username="testsuperuser",
                                                   email='super@user.com', password='foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        try:
            self.assertIsNotNone(admin_user.username)
            self.assertIsNotNone(admin_user.profile)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(username="testsuperuser",
                                          email='super@user.com', password='foo', is_superuser=False)


class UserFormValidationTests(TestCase):
    def test_singup_validation(self):
        input_data = {
            'username': 'zhomart',
            'email': 'email',
            'password': 'password'
        }

        self.assertFalse(UserSignUpSerializer(data=input_data).is_valid())

        input_data['email'] = 'email@gmail.com'
        self.assertTrue(UserSignUpSerializer(data=input_data).is_valid())

    def test_login_validation(self):
        input_data = {
            'username': 'zhomart',
            'email': 'email',
            'password': 'password'
        }

        self.assertFalse(UserSignInSerializer(data=input_data).is_valid())

        input_data['email'] = 'email@gmail.com'
        self.assertTrue(UserSignInSerializer(data=input_data).is_valid())
