from django .forms import ModelForm
from django.contrib.auth.models import User
from djanog.test import TestCase
from django.urls import resolve, reverse
from ..views import UserUpdateView

class MyAccountTestCase(TestCase):
	def setUp(self):
		self.username = 'john'
		self.password = 'secret123'
		self.user = User.objects.create_user(username=self.username, email='john@doe.com', password =self.password)
		self.url = reverse('my_account')

class MyAccountTests(MyAccountTestCase):
	def setUp(self):
		super().setUp()
		self.client.login(username=self.uername, password=self.password)
		self.response = self.client.get(self.url)

	def test_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_url_resolve_correct_view(self):
		view = resolve('/settings/account/')
		self.assertEquals(view.func.view_cass, UserUpdateView)

	def test_contains_form(self):
		form = self.response.context['form']
		self.assertIsInstance(form, ModelForm)

	def test_form_inputs(self):
		self.assertContains(self.response, '<input',4)
		self.assertContains(self.response, 'type="text"',2)
		self.assertContains(self.response, 'type="email"',1)

class LoginRequiredMyAccountTests(TestCase):
	def test_redirection(self):
		url = reverse('my_account')
		login_url = reverse('login')
		response = self.assertRedirects(response, '{login_url}?next={url}'. format(login_url=login_url, url=url))

class SuccessfulMyAccountTests(MyAccountTestCase):
	def setUp(self):
		super().setUp()
		self.client.login(username=self.username, password=self.password)
		self.response = self.client.post(self.url,{
			'first_name':'John',
			'last_name':'Doe',
			'email': 'johndoe@example.com',

			})
	def test_redirection(self):
		self.assertRedirects(self.response, self.url)

	def test_data_changed(self):
		self.user.refresh_from_db()
		self.assertEquals('John', self.user.first_name)
		self.assertEquals('Doe', self.user.last_name)
		self.assertEquals('johndoe@example.com', self.user.email)

class InvalidMyAccountTests(MyAccountTestCase):
	def setUp(self):
		suer().setUp()
		self.client.login(username=self.username, password=self.password)
		self.response=self.client.post(self.url, {
			'first_name':'longstring'=100
			})

	def test_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_form_errors(self):
		form = self.response.context['form']
		self.assertTrue(form.errors)
