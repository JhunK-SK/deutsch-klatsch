from django.test import TestCase, SimpleTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from django.contrib.auth.models import Group

class UserSignupTest(TestCase):
    
    username = 'newuser'
    email = 'newuser@email.com'
    
    def setUp(self):
        url = reverse('account_signup')
        self.response = self.client.get(url)
        
    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'account/signup.html')
        self.assertContains(self.response, 'Sign Up')
        self.assertNotContains(self.response, 'This should not be on the page.')
        
    def test_signup_form(self):
        general_user_group = Group.objects.create(name='general_user')
        new_user = get_user_model().objects.create_user(
            self.email, self.username)
        new_user.groups.add(general_user_group)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)
        self.assertEqual(get_user_model().objects.all()[0].groups.all()[0], general_user_group)


class CustomUserTests(TestCase):
    # Test creating a plain user and a superuser
    # Since a signal for grouping has been added, there should be defined group before creating new users.
    def setUp(self):
        general_group = Group.objects.create(name='general_user')
    
    
    def test_creste_user(self):
        User = get_user_model()
        testuser = User.objects.create_user(
            email='test@email.com',
            username='testname',
            password='testpass'
        )
        self.assertEqual(testuser.email, 'test@email.com')
        self.assertEqual(testuser.username, 'testname')
        self.assertTrue(testuser.is_active)
        self.assertFalse(testuser.is_staff)
        self.assertFalse(testuser.is_superuser)
        
    def test_create_superuser(self):
        User = get_user_model()
        superuser = User.objects.create_superuser(
            email='supertest@email.com',
            username='supertest',
            password='superpass'
        )
        self.assertEqual(superuser.email, 'supertest@email.com')
        self.assertEqual(superuser.username, 'supertest')
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

# class LoginPageTests(SimpleTestCase):
    
#     def setUp(self):
#         url = reverse('account_login')
#         self.response = self.client.get(url)
        
#     def test_login_page_status_code(self):
#         response = self.client.get('/accounts/login/')
#         self.assertEqual(response.status_code, 200)
    
#     def test_login_page_by_name(self):
#         self.assertEqual(self.response.status_code, 200)
        
#     def test_login_page_template(self):
#         self.assertTemplateUsed(self.response, 'accounts/login.html')
        
#     def test_login_page_contains_correct_html(self):
#         self.assertContains(self.response, 'Login')
        
#     def test_login_page_does_not_contain_incorrect_html(self):
#         self.assertNotContains(self.response, 'it should not be contained')
        
#     def test_login_page_url_resolves_login_view(self):
#         view = resolve(reverse('account_login'))
#         self.assertEqual(view.func.__name__, LoginView.as_view().__name__)


# class SignupPageTests(SimpleTestCase):
    
#     def setUp(self):
#         url = reverse('account_signup')
#         self.response = self.client.get(url)
        
#     def test_signup_page_status_code(self):
#         response = self.client.get('/accounts/signup/')
#         self.assertEqual(response.status_code, 200)
    
#     def test_signup_page_by_name(self):
#         self.assertEqual(self.response.status_code, 200)
        
#     def test_signup_page_template(self):
#         self.assertTemplateUsed(self.response, 'accounts/signup.html')
        
#     def test_signup_page_contains_correct_html(self):
#         self.assertContains(self.response, 'Sign up')
        
#     def test_signup_page_does_not_contain_incorrect_html(self):
#         self.assertNotContains(self.response, 'it should not be contaisignup')
        
#     def test_signup_page_url_resolves_login_view(self):
#         view = resolve(reverse('account_signup'))
#         self.assertEqual(view.func.__name__, SignupView.as_view().__name__)