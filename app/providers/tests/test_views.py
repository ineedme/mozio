import json
from django.contrib.gis.geos import Point
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from django.core.cache import caches
from model_bakery import baker
import os
from rest_framework.test import APITestCase, APIClient

from providers.models import Provider, ServiceArea
from providers.serializers import ProviderSerializer, ServiceAreaSerializer, ResultsSerializer


class ProviderViewSetTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.provider_data = {
            'name': 'Test Provider',
            'email': 'test@provider.com',
            'phone_number': '1234567890',
            'language': 'en',
            'currency': 'USD'
        }
        self.provider = self.client.post(
            reverse('provider-list'),
            self.provider_data,
            format='json'
        )

    def test_create_provider(self):
        response = self.client.post(
            reverse('provider-list'),
            self.provider_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_providers(self):
        response = self.client.get(reverse('provider-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_provider(self):
        response = self.client.get(
            reverse('provider-detail', kwargs={'pk': self.provider.data['id']})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_provider(self):
        response = self.client.put(
            reverse('provider-detail', kwargs={'pk': self.provider.data['id']}),
            self.provider_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_provider(self):
        response = self.client.delete(
            reverse('provider-detail', kwargs={'pk': self.provider.data['id']})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ServiceAreaViewSetTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.provider_data = {
            'name': 'Test Provider',
            'email': 'test@provider.com',
            'phone_number': '1234567890',
            'language': 'en',
            'currency': 'USD'
        }
        self.provider = self.client.post(
            reverse('provider-list'),
            self.provider_data,
            format='json'
        )
        self.service_area_data = {
            'name': 'Test Service Area',
            'price': 10.00,
            'provider': self.provider.data['id'],
            'area': {
                'type': 'Polygon',
                'coordinates': [
                    [
                        [0, 0],
                        [0, 50],
                        [50, 50],
                        [50, 0],
                        [0, 0]
                    ]
                ]
            }
        }
        self.service_area = self.client.post(
            reverse('servicearea-list'),
            self.service_area_data,
            format='json'
        )

    def test_create_service_area(self):
        response = self.client.post(
            reverse('servicearea-list'),
            self.service_area_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_service_areas(self):
        response = self.client.get(reverse('servicearea-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_service_area(self):
        response = self.client.get(
            reverse(
                'servicearea-detail',
                kwargs={'pk': self.service_area.data['id']}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_service_area(self):
        response = self.client.put(
            reverse(
                'servicearea-detail',
                kwargs={'pk': self.service_area.data['id']}
            ),
            self.service_area_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_service_area(self):
        response = self.client.delete(
            reverse(
                'servicearea-detail',
                kwargs={'pk': self.service_area.data['id']}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ProvidersInTheAreaTest(APITestCase):
    """Test endpoint that takes a lat/lng pair and return a list of all polygons that include the given lat/lng"""

    def setUp(self):
        self.provider = baker.make(Provider, name="Uber")
        self.service_area = baker.make(
            ServiceArea,
            name="Test Service Area",
            price=10.00,
            provider=self.provider,
            area='POLYGON((0 0, 0 50, 50 50, 50 0, 0 0))'
        )

    def test_get_providers_in_the_area(self):
        response = self.client.get(
            reverse('servicearea-get-providers-in-the-area'),
            {'lat': 25, 'lng': 25}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Service Area')

    def test_get_providers_in_the_area_no_results(self):
        response = self.client.get(
            reverse('servicearea-get-providers-in-the-area'),
            {'lat': 100, 'lng': 100}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_providers_in_the_area_invalid_request(self):
        response = self.client.get(
            reverse('servicearea-get-providers-in-the-area')
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
