from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core import mail

# Create your tests here.

class PasswordResetTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_password_reset_page_loads(self):
        """Test that the password reset page loads correctly"""
        response = self.client.get(reverse('core:password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Reset Your Password')

    def test_password_reset_form_submission(self):
        """Test that password reset form submission works"""
        response = self.client.post(reverse('core:password_reset'), {
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to done page
        self.assertRedirects(response, reverse('core:password_reset_done'))

    def test_password_reset_email_sent(self):
        """Test that password reset email is sent"""
        self.client.post(reverse('core:password_reset'), {
            'email': 'test@example.com'
        })
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Password Reset', mail.outbox[0].subject)

    def test_password_reset_done_page(self):
        """Test that password reset done page loads"""
        response = self.client.get(reverse('core:password_reset_done'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Check Your Email')
