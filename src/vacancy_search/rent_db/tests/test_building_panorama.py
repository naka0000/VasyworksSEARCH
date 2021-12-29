"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
from unittest import TestCase
from django.db import transaction
from rent_db.models import Building
from users.models import User
import warnings


class BuildingPanoramaModelTest(TestCase):
    """
    建物パノラマのテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')
        self.building = Building.objects.get(pk=2)      # 表示項目確認用マンション
        self.panorama = self.building.building_panoramas.first()

        if transaction.get_autocommit():
            transaction.set_autocommit(False)

    def tearDown(self):
        transaction.rollback()

    def test_building_panorama_cache_file_url(self):
        self.building.auth_user = User.objects.get(username='t-kanri')
        file_oid = '7112299ba5e743428e02a0824a3582d0'   # 表示項目確認用マンション
        cache_file_name = '3b43b26e5cb64efdb3622e1d75e46948.JPG'      # エントランス
        self.assertEqual(
            self.panorama.cache_file_url,
            '/viewer/cache_media/buildings/' + file_oid + '/' + cache_file_name,
        )
