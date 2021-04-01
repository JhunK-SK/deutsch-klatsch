from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve

from .views import index, AboutView


class HomePageTests(SimpleTestCase):
    
    def setUp(self):
        url = reverse('boards:home')
        self.response = self.client.get(url)
    
    def test_homepage_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_homepage_by_url_name(self):
        self.assertEqual(self.response.status_code, 200)
        
    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'home.html')
    
    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, 'Klatsch Boards')
        
    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'This should be not on the page')
        
    def test_homepage_resolve_indexview(self):
        view = resolve(reverse('boards:home'))
        self.assertEqual(view.func.__name__, index.__name__)
        
        
class AboutPageTest(SimpleTestCase):
    
    def setUp(self):
        url = reverse('boards:about')
        self.response = self.client.get(url)
    
    def test_aboutpage_status_code(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        
    def test_aboutpage_by_url_name(self):
        self.assertEqual(self.response.status_code, 200)
        
    def test_aboutpage_template(self):
        self.assertTemplateUsed(self.response, 'about.html')
    
    def test_aboutpage_contains_correct_html(self):
        self.assertContains(self.response, 'Talk about everything from inside of you.')
        
    def test_aboutpage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'This should be not on the page')
        
    def test_aboutpage_resolve_indexview(self):
        view = resolve(reverse('boards:about'))
        self.assertEqual(view.func.__name__, AboutView.as_view().__name__)