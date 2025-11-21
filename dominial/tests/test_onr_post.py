"""
Tests for ONR (Organização Nacional dos Registradores) API integration
"""
import unittest
import pytest
import requests
from django.test import TestCase, Client
from django.contrib.auth.models import User


class TestONRIntegration(TestCase):
    """Test ONR external API integration"""

    def setUp(self):
        """Set up test client and authenticated user"""
        self.client = Client()
        # Create and authenticate a test user for endpoints that require login
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.client.login(username='testuser', password='testpass123')

    @unittest.skip("External API test - ONR API may block automated requests with 403")
    def test_onr_external_api_post(self):
        """Test direct POST request to ONR external API"""
        url = 'https://www.registrodeimoveis.org.br/includes/consulta-cartorios.php'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
            'Accept': '*/*',
            'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.registrodeimoveis.org.br/cartorios',
        }
        data = 'estado=AC'

        try:
            response = requests.post(url, headers=headers, data=data, timeout=10)
            self.assertEqual(response.status_code, 200)
        except requests.exceptions.RequestException as e:
            # External API might be unavailable, skip test
            self.skipTest(f"External ONR API unavailable: {e}")

    @unittest.skip("Skipped: requires DEBUG=True (SECURE_SSL_REDIRECT=True causes 301 when DEBUG=False)")
    def test_verificar_cartorios_endpoint(self):
        """Test internal verificar-cartorios endpoint"""
        # URL already has trailing slash, no follow needed
        response = self.client.post('/dominial/verificar-cartorios/', data={'estado': 'SP'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('existem_cartorios', data)
