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


class LoginViewTest(TestCase):
    """
    ログインビューのテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')
        self.client = Client()

    def test_get_login_view(self):
        url = reverse('login')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_post_login_view(self):
        url = reverse('login')
        response = self.client.post(
            url,
            {
                'username': 't-kanri',      # 管理 太郎
                'password': 'guest1234',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        user = response.context['user']
        self.assertEqual(user.username, 't-kanri')
        self.assertEqual(user.full_name, '管理 太郎')

    def test_post_login_failed_view(self):
        url = reverse('login')
        response = self.client.post(
            url,
            {
                'username': 't-kanri',      # 管理 太郎
                'password': 'abcd1234',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), 'ログインに失敗しました。')
