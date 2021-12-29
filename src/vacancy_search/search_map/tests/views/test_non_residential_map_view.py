"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
from unittest import TestCase
from django.test import Client
from django.urls import reverse
import warnings


class NonResidentialSearchMapViewTest(TestCase):
    """
    非居住用地図検索ビューのテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')
        self.client = Client()

        response = self.client.post(
            reverse('login'),
            {'username': 't-kanri', 'password': 'guest1234', },
            follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_get_menu_index_view(self):
        url = reverse('search_map_non_residential_map')
        url += '?lat=35.0038&lng=135.777'    # 祇園
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
