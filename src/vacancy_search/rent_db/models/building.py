"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
"""
from django.conf import settings
from django.db import models
from django.db.models import Q, Subquery, OuterRef
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from lib.convert import *
from lib.functions import *
from .area import Area
from .arrival_type import ArrivalType
from .bike_parking_type import BikeParkingType
from .building_garage import BuildingGarage
from .building_type import BuildingType
from .city import City
from .company import Company
from .department import Department
from .elementary_school import ElementarySchool
from .existence import Existence
from .garage_type import GarageType
from .garage_status import GarageStatus
from .junior_high_school import JuniorHighSchool
from .management_type import ManagementType
from .owner import Owner
from .pref import Pref
from .room import Room
from .staff import Staff
from .station import Station
from .structure import Structure
from .tax_type import TaxType
from .trader import Trader


class Building(models.Model):
    """
    建物
    """
    id = models.AutoField(_('id'), db_column='id', primary_key=True)

    oid = models.CharField(_('oid'), db_column='oid', db_index=True, unique=True, max_length=50)
    file_oid = models.CharField(_('file_oid'), db_column='file_oid', db_index=True, unique=True, max_length=50)
    building_code = models.CharField(_('building_code'), db_column='building_code', max_length=20, db_index=True, null=True, blank=True)
    building_name = models.CharField(_('building_name'), db_column='building_name', max_length=100, db_index=True, null=True, blank=True)
    building_kana = models.CharField(_('building_kana'), db_column='building_kana', max_length=100, db_index=True, null=True, blank=True)
    building_old_name = models.CharField(_('building_old_name'), db_column='building_old_name', max_length=100, null=True, blank=True)

    postal_code = models.CharField(_('postal_code'), db_column='postal_code', max_length=10, null=True, blank=True)
    pref = models.ForeignKey(
        Pref,
        db_column='pref_id',
        related_name='buildings',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
        limit_choices_to=Q(is_trading_area=True) | Q(pk=0),
    )
    city = models.ForeignKey(
        City,
        db_column='city_id',
        related_name='buildings',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
        limit_choices_to=Q(is_trading_area=True, is_stopped=False) | Q(pk=0),
    )
    town_address = models.CharField(_('town_address'), db_column='town_address', max_length=255, null=True, blank=True)
    town_name = models.CharField(_('town_name'), db_column='town_name', max_length=100, null=True, blank=True)
    house_no = models.CharField(_('house_no'), db_column='house_no', max_length=100, null=True, blank=True)
    building_no = models.CharField(_('building_no'), db_column='building_no', max_length=100, null=True, blank=True)
    lat = models.FloatField(_('lat'), db_column='lat', db_index=True, default=0)
    lng = models.FloatField(_('lng'), db_column='lng', db_index=True, default=0)
    area = models.ForeignKey(
        Area,
        db_column='area_id',
        related_name='buildings',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
        limit_choices_to=Q(is_stopped=False) | Q(pk=0),
    )

    elementary_school = models.ForeignKey(
        ElementarySchool,
        db_column='elementary_school_id',
        related_name='buildings',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
        limit_choices_to=Q(is_stopped=False) | Q(pk=0),
    )
    elementary_school_distance = models.IntegerField(_('elementary_school_distance'), db_column='elementary_school_distance', default=0)

    junior_high_school = models.ForeignKey(
        JuniorHighSchool,
        db_column='junior_high_school_id',
        related_name='buildings',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
        limit_choices_to=Q(is_stopped=False) | Q(pk=0),
    )
    junior_high_school_distance = models.IntegerField(_('junior_high_school_distance'), db_column='junior_high_school_distance', default=0)
    around_note = models.CharField(_('around_note'), db_column='around_note', max_length=255, null=True, blank=True)

    management_type = models.ForeignKey(
        ManagementType,
        db_column='management_type_id',
        related_name='buildings',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )
    department = models.ForeignKey(
        Department,
        db_column='department_id',
        related_name='buildings',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
        limit_choices_to=Q(is_stopped=False, is_deleted=False) | Q(pk=0),
    )
    staff1 = models.ForeignKey(
        Staff,
        db_column='staff_id1',
        related_name='staff1_buildings',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
        limit_choices_to=Q(is_stopped=False, is_deleted=False) | Q(pk=0),
    )
    staff2 = models.ForeignKey(
        Staff,
        db_column='staff_id2',
        related_name='staff2_buildings',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
        limit_choices_to=Q(is_stopped=False, is_deleted=False) | Q(pk=0),
    )
    priority_level = models.IntegerField(_('priority_level'), db_column='priority_level', db_index=True, default=50)
    agency_department = models.ForeignKey(
        Department,
        db_column='agency_department_id',
        related_name='agency_buildings',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
        limit_choices_to=Q(is_stopped=False, is_deleted=False) | Q(pk=0),
    )

    owner = models.ForeignKey(
        Owner,
        db_column='owner_id',
        related_name='buildings',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )
    owner_note = models.CharField(_('owner_note'), db_column='owner_note', max_length=255, null=True, blank=True)
    trader = models.ForeignKey(
        Trader,
        db_column='trader_id',
        related_name='buildings',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )

    register_address = models.CharField(_('register_address'), db_column='register_address', max_length=255, null=True, blank=True)
    register_name = models.CharField(_('register_name'), db_column='register_name', max_length=255, null=True, blank=True)
    register_building_no = models.CharField(_('register_building_no'), db_column='register_building_no', max_length=255, null=True, blank=True)
    register_no = models.CharField(_('register_no'), db_column='register_no', max_length=50, null=True, blank=True)

    arrival_type1 = models.ForeignKey(
        ArrivalType,
        db_column='arrival_type_id1',
        related_name='buildings1',
        on_delete=models.PROTECT,
        default=0,
    )
    station1 = models.ForeignKey(
        Station,
        db_column='station_id1',
        related_name='buildings1',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
        limit_choices_to=Q(is_trading=True, is_stopped=False) | Q(pk=0),
    )
    station_time1 = models.IntegerField(_('station_time1'), db_column='station_time1', default=0)
    bus_stop1 = models.CharField(_('bus_stop1'), db_column='bus_stop1', max_length=50, null=True, blank=True)
    bus_stop_time1 = models.IntegerField(_('bus_stop_time1'), db_column='bus_stop_time1', default=0)

    arrival_type2 = models.ForeignKey(
        ArrivalType,
        db_column='arrival_type_id2',
        related_name='buildings2',
        on_delete=models.PROTECT,
        default=0,
    )
    station2 = models.ForeignKey(
        Station,
        db_column='station_id2',
        related_name='buildings2',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
        limit_choices_to=Q(is_trading=True, is_stopped=False) | Q(pk=0),
    )
    station_time2 = models.IntegerField(_('station_time2'), db_column='station_time2', default=0)
    bus_stop2 = models.CharField(_('bus_stop2'), db_column='bus_stop2', max_length=50, null=True, blank=True)
    bus_stop_time2 = models.IntegerField(_('bus_stop_time2'), db_column='bus_stop_time2', default=0)

    arrival_type3 = models.ForeignKey(
        ArrivalType,
        db_column='arrival_type_id3',
        related_name='buildings3',
        on_delete=models.PROTECT,
        default=0,
    )
    station3 = models.ForeignKey(
        Station,
        db_column='station_id3',
        related_name='buildings3',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
        limit_choices_to=Q(is_trading=True, is_stopped=False) | Q(pk=0),
    )
    station_time3 = models.IntegerField(_('station_time3'), db_column='station_time3', default=0)
    bus_stop3 = models.CharField(_('bus_stop3'), db_column='bus_stop3', max_length=50, null=True, blank=True)
    bus_stop_time3 = models.IntegerField(_('bus_stop_time3'), db_column='bus_stop_time3', default=0)

    building_type = models.ForeignKey(
        BuildingType,
        db_column='building_type_id',
        related_name='buildings',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )
    building_type_comment = models.CharField(_('building_type_comment'), db_column='building_type_comment', max_length=100, null=True, blank=True)
    structure = models.ForeignKey(
        Structure,
        db_column='structure_id',
        related_name='buildings',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )
    structure_comment = models.CharField(_('structure_comment'), db_column='structure_comment', max_length=100, null=True, blank=True)
    building_rooms = models.IntegerField(_('building_rooms'), db_column='building_rooms', default=0)
    building_floors = models.IntegerField(_('building_floors'), db_column='building_floors', default=0)
    building_undergrounds = models.IntegerField(_('building_undergrounds'), db_column='building_undergrounds', default=0)
    build_year = models.IntegerField(_('build_year'), db_column='build_year', db_index=True, default=1970)
    build_month = models.IntegerField(_('build_month'), db_column='build_month', default=1)

    bike_parking_type = models.ForeignKey(
        BikeParkingType,
        db_column='bike_parking_type_id',
        related_name='buildings',
        on_delete=models.PROTECT,
        default=0,
    )
    with_bike_parking_roof = models.BooleanField(_('with_bike_parking_roof'), db_column='with_bike_parking_roof', default=False)
    bike_parking_fee_lower = models.IntegerField(_('bike_parking_fee_lower'), db_column='bike_parking_fee_lower', default=0)
    bike_parking_fee_upper = models.IntegerField(_('bike_parking_fee_upper'), db_column='bike_parking_fee_upper', default=0)
    bike_parking_fee_tax_type = models.ForeignKey(
        TaxType,
        db_column='bike_parking_fee_tax_type_id',
        related_name='bike_parking_fee_buildings',
        on_delete=models.PROTECT,
        default=0,
    )
    bike_parking_note = models.CharField(_('bike_parking_note'), db_column='bike_parking_note', max_length=255, null=True, blank=True)
    garage_type = models.ForeignKey(
        GarageType,
        db_column='garage_type_id',
        related_name='buildings',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )
    garage_status = models.ForeignKey(
        GarageStatus,
        db_column='garage_status_id',
        related_name='buildings',
        on_delete=models.PROTECT,
        default=0,
    )
    garage_distance = models.IntegerField(_('garage_distance'), db_column='garage_distance', default=0)
    garage_fee_lower = models.IntegerField(_('garage_fee_lower'), db_column='garage_fee_lower', default=0)
    garage_fee_upper = models.IntegerField(_('garage_fee_upper'), db_column='garage_fee_upper', default=0)
    garage_fee_tax_type = models.ForeignKey(
        TaxType,
        db_column='garage_fee_tax_type_id',
        related_name='garage_fee_buildings',
        on_delete=models.PROTECT,
        default=0,
    )
    garage_charge_lower = models.IntegerField(_('garage_charge_lower'), db_column='garage_charge_lower', default=0)
    garage_charge_upper = models.IntegerField(_('garage_charge_upper'), db_column='garage_charge_upper', default=0)
    garage_charge_tax_type = models.ForeignKey(
        TaxType,
        db_column='garage_charge_tax_type_id',
        related_name='garage_charge_buildings',
        on_delete=models.PROTECT,
        default=0,
    )
    garage_note = models.CharField(_('garage_note'), db_column='garage_note', max_length=255, null=True, blank=True)
    building_management_company = models.CharField(_('building_management_company'), db_column='building_management_company', max_length=100, null=True, blank=True)
    building_management_address = models.CharField(_('building_management_address'), db_column='building_management_address', max_length=255, null=True, blank=True)
    building_management_tel = models.CharField(_('building_management_tel'), db_column='building_management_tel', max_length=20, null=True, blank=True)
    building_management_no = models.CharField(_('building_management_no'), db_column='building_management_no', max_length=50, null=True, blank=True)
    building_management_note = models.CharField(_('building_management_note'), db_column='building_management_note', max_length=255, null=True, blank=True)

    agreement_existence = models.ForeignKey(
        Existence,
        db_column='agreement_existence_id',
        related_name='agreement_existence_buildings',
        on_delete=models.PROTECT,
        default=0,
    )
    apartment_manager_comment = models.CharField(_('apartment_manager_comment'), db_column='apartment_manager_comment', max_length=100, null=True, blank=True)

    auto_lock_no = models.CharField(_('auto_lock_no'), db_column='auto_lock_no', max_length=20, null=True, blank=True)

    is_hidden_vacancy = models.BooleanField(_('is_hidden_vacancy'), db_column='is_hidden_vacancy', db_index=True, default=False)
    is_vacancy_recommend = models.BooleanField(_('is_vacancy_recommend'), db_column='is_vacancy_recommend', db_index=True, default=False)
    vacancy_rent_comment = models.CharField(_('vacancy_rent_comment'), db_column='vacancy_rent_comment', max_length=100, null=True, blank=True)
    vacancy_condo_fees_comment = models.CharField(_('vacancy_condo_fees_comment'), db_column='vacancy_condo_fees_comment', max_length=100, null=True, blank=True)
    vacancy_water_comment = models.CharField(_('vacancy_water_comment'), db_column='vacancy_water_comment', max_length=100, null=True, blank=True)
    vacancy_electric_comment = models.CharField(_('vacancy_electric_comment'), db_column='vacancy_electric_comment', max_length=100, null=True, blank=True)
    vacancy_gas_comment = models.CharField(_('vacancy_gas_comment'), db_column='vacancy_gas_comment', max_length=100, null=True, blank=True)
    vacancy_internet_comment = models.CharField(_('vacancy_internet_comment'), db_column='vacancy_internet_comment', max_length=100, null=True, blank=True)
    vacancy_cancel_notice_comment = models.CharField(_('vacancy_cancel_notice_comment'), db_column='vacancy_cancel_notice_comment', max_length=100, null=True, blank=True)
    vacancy_short_cancel_comment = models.CharField(_('vacancy_short_cancel_comment'), db_column='vacancy_short_cancel_comment', max_length=100, null=True, blank=True)
    vacancy_payment_comment = models.CharField(_('vacancy_payment_comment'), db_column='vacancy_payment_comment', max_length=100, null=True, blank=True)
    vacancy_guarantee_comment = models.CharField(_('vacancy_guarantee_comment'), db_column='vacancy_guarantee_comment', max_length=100, null=True, blank=True)
    vacancy_insurance_comment = models.CharField(_('vacancy_insurance_comment'), db_column='vacancy_insurance_comment', max_length=100, null=True, blank=True)
    vacancy_guarantor_limit_comment = models.CharField(_('vacancy_guarantor_limit_comment'), db_column='vacancy_guarantor_limit_comment', max_length=100, null=True, blank=True)
    vacancy_document_price_comment = models.CharField(_('vacancy_document_price_comment'), db_column='vacancy_document_price_comment', max_length=100, null=True, blank=True)
    vacancy_renewal_fee_comment = models.CharField(_('vacancy_renewal_fee_comment'), db_column='vacancy_renewal_fee_comment', max_length=100, null=True, blank=True)
    vacancy_renewal_charge_comment = models.CharField(_('vacancy_renewal_charge_comment'), db_column='vacancy_renewal_charge_comment', max_length=100, null=True, blank=True)
    vacancy_auto_lock_comment = models.CharField(_('vacancy_auto_lock_comment'), db_column='vacancy_auto_lock_comment', max_length=100, null=True, blank=True)
    vacancy_security_comment = models.CharField(_('vacancy_security_comment'), db_column='vacancy_security_comment', max_length=100, null=True, blank=True)
    vacancy_bike_parking_comment = models.CharField(_('vacancy_bike_parking_comment'), db_column='vacancy_bike_parking_comment', max_length=100, null=True, blank=True)
    vacancy_garage_comment = models.CharField(_('vacancy_garage_comment'), db_column='vacancy_garage_comment', max_length=100, null=True, blank=True)
    vacancy_cleaning_comment = models.CharField(_('vacancy_cleaning_comment'), db_column='vacancy_cleaning_comment', max_length=100, null=True, blank=True)
    vacancy_change_lock_comment = models.CharField(_('vacancy_change_lock_comment'), db_column='vacancy_change_lock_comment', max_length=100, null=True, blank=True)
    vacancy_portal_note = models.CharField(_('vacancy_portal_note'), db_column='vacancy_portal_note', max_length=255, null=True, blank=True)
    vacancy_catch_copy = models.CharField(_('vacancy_catch_copy'), db_column='vacancy_catch_copy', max_length=100, null=True, blank=True)
    vacancy_appeal = models.CharField(_('vacancy_appeal'), db_column='vacancy_appeal', max_length=255, null=True, blank=True)
    vacancy_note = models.TextField(_('vacancy_note'), db_column='vacancy_note', max_length=2000, null=True, blank=True)

    is_hidden_web = models.BooleanField(_('is_hidden_web'), db_column='is_hidden_web', db_index=True, default=False)
    web_catch_copy = models.CharField(_('web_catch_copy'), db_column='web_catch_copy', max_length=100, null=True, blank=True)
    web_appeal = models.CharField(_('web_appeal'), db_column='web_appeal', max_length=255, null=True, blank=True)
    web_note = models.TextField(_('web_note'), db_column='web_note', max_length=2000, null=True, blank=True)

    tenant_note = models.TextField(_('tenant_note'), db_column='tenant_note', max_length=2000, null=True, blank=True)
    garbage_note = models.TextField(_('garbage_note'), db_column='garbage_note', max_length=2000, null=True, blank=True)
    private_note = models.TextField(_('private_note'), db_column='private_note', max_length=2000, null=True, blank=True)
    management_note = models.TextField(_('management_note'), db_column='management_note', max_length=2000, null=True, blank=True)

    is_deleted = models.BooleanField(_('is_deleted'), db_column='is_deleted', db_index=True, default=False)

    class Meta:
        managed = False
        db_table = 'building'
        ordering = ['building_kana', 'id']
        verbose_name = _('building')
        verbose_name_plural = _('buildings')

    def __init__(self, *args, **kwargs):
        self.auth_user = None  # 閲覧レベル判定用のユーザ
        self.is_residential = False  # 居住用が対象の場合はTrue
        self.is_non_residential = False  # 非居住用が対象の場合はTrue

        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.building_name

    """
    内部メソッド
    """
    @classmethod
    def __get_nearest_station_text(cls,
                                   arrival_type,
                                   station,
                                   station_time,
                                   bus_stop,
                                   bus_stop_time,
                                   ):
        ans = None
        if station:
            if station.id != 0:
                ans = xstr(station.railway.name) + ' ' + xstr(station.name)
                ans += ' 駅まで' + xstr(arrival_type.name)
                ans += xstr(station_time) + '分'
                if xint(arrival_type.id) == 2:
                    ans += '（バス停 ' + xstr(bus_stop)
                    if xint(bus_stop_time) > 0:
                        ans += 'まで徒歩' + xstr(bus_stop_time) + '分'
                    ans += '）'
        return ans

    """
    プロパティ
    """
    @property
    def idb64(self):
        return base64_decode_id(self.pk)

    @property
    def all_rooms(self):
        if not self.auth_user:
            raise Exception

        return self.rooms.order_by('room_no', 'id').all()

    @property
    def facilities(self):
        return self.building_facilities.filter(
            is_deleted=False,
        ).order_by('priority', 'facility__priority', 'id').all()

    @property
    def garages(self):
        return self.building_garages.filter(
            garage_status__id__in=[1, 3, 4],
            is_deleted=False,
        ).order_by('priority', 'garage_name', 'id').all()

    @property
    def landmarks(self):
        return self.building_landmarks.filter(
            is_deleted=False,
        ).order_by('priority', 'landmark__priority', 'id').all()

    @property
    def files(self):
        return self.building_files.filter(
            is_publish_vacancy=True,
            is_deleted=False,
        ).order_by('priority', 'id').all()

    @property
    def movies(self):
        return self.building_movies.filter(
            is_publish_vacancy=True,
            is_deleted=False,
        ).order_by('priority', 'movie_type__priority', 'id').all()

    @property
    def panoramas(self):
        return self.building_panoramas.filter(
            is_publish_vacancy=True,
            is_deleted=False,
        ).order_by('priority', 'panorama_type__priority', 'id').all()

    @property
    def pictures(self):
        return self.building_pictures.filter(
            is_publish_vacancy=True,
            is_deleted=False,
        ).order_by('priority', 'picture_type__priority', 'id').all()

    """
    表示用プロパティ
    """
    @property
    def address(self):
        ans = None
        if self.pref:
            ans = xstr(self.pref.name)
            if self.pref.id != 0 and self.city:
                ans += xstr(self.city.name)
                if self.city.id != 0:
                    ans += xstr(self.town_address)
                    ans += xstr(self.house_no)
                    if self.building_no:
                        ans += ' ' + xstr(self.building_no)
        return ans

    @property
    def area_text(self):
        ans = None
        if self.area.id != 0:
            ans = self.area.name

        return ans

    @property
    def nearest_station1(self):
        return Building.__get_nearest_station_text(
            self.arrival_type1,
            self.station1,
            self.station_time1,
            self.bus_stop1,
            self.bus_stop_time1,
        )

    @property
    def nearest_station2(self):
        return Building.__get_nearest_station_text(
            self.arrival_type2,
            self.station2,
            self.station_time2,
            self.bus_stop2,
            self.bus_stop_time2,
        )

    @property
    def nearest_station3(self):
        return Building.__get_nearest_station_text(
            self.arrival_type3,
            self.station3,
            self.station_time3,
            self.bus_stop3,
            self.bus_stop_time3,
        )

    @property
    def building_type_text(self):
        ans = None
        if self.building_type.id != 0:
            ans = self.building_type.name
            if self.building_type_comment:
                ans += '（{0}）'.format(self.building_type_comment)

        return ans

    @property
    def build_year_month(self):
        ans = None
        if self.build_year:
            ans = xstr(self.build_year) + '年'
            if self.build_month:
                ans += xstr(self.build_month) + '月'
            ans += '築'
        return ans

    @property
    def structure_text(self):
        ans = None
        if self.structure.id != 0:
            ans = self.structure.name
            if self.structure_comment:
                ans += '（{0}）'.format(self.structure_comment)

        return ans

    @property
    def elementary_school_text(self):
        ans = None
        if self.elementary_school.id != 0:
            ans = self.elementary_school.name

        return ans

    @property
    def elementary_school_distance_text(self):
        ans = None
        if self.elementary_school.id != 0 and self.elementary_school_distance > 0:
            ans = '{0} m'.format(self.elementary_school_distance)

        return ans

    @property
    def junior_high_school_text(self):
        ans = None
        if self.junior_high_school.id != 0:
            ans = self.junior_high_school.name

        return ans

    @property
    def junior_high_school_distance_text(self):
        ans = None
        if self.junior_high_school.id != 0 and self.junior_high_school_distance > 0:
            ans = '{0} m'.format(self.junior_high_school_distance)

        return ans

    @property
    def garage_status_text(self):
        ans = None
        if self.garage_type.is_exist and self.garage_status.id != 0:
            ans = self.garage_status.name

        return ans

    @property
    def garage_distance_text(self):
        ans = None
        if self.garage_type.id != 0 and self.garage_distance > 0:
            ans = '{0} m'.format(self.garage_distance)

        return ans

    @property
    def garage_fee_text(self):
        ans = None
        if self.garage_type.is_paid:
            if self.garage_fee_lower > 0 or self.garage_fee_upper > 0:
                ans = ''
                if self.garage_fee_lower > 0:
                    ans += '{0:,} 円'.format(self.garage_fee_lower)
                if self.garage_fee_upper > 0 and self.garage_fee_upper > self.garage_fee_lower:
                    ans += ' 〜 {0:,} 円'.format(self.garage_fee_upper)
                if self.garage_fee_tax_type.text:
                    ans += ' ' + self.garage_fee_tax_type.text

                if ans == '':
                    ans = None

        return ans

    @property
    def garage_charge_text(self):
        ans = None
        if self.garage_charge_lower > 0 or self.garage_charge_upper > 0:
            ans = ''
            if self.garage_charge_lower > 0:
                ans += '{0:,} 円'.format(self.garage_charge_lower)
            if self.garage_charge_upper > 0 and self.garage_charge_upper > self.garage_charge_lower:
                ans += ' 〜 {0:,} 円'.format(self.garage_charge_upper)
            if self.garage_charge_tax_type.text:
                ans += ' ' + self.garage_charge_tax_type.text

            if ans == '':
                ans = None

        return ans

    @property
    def bike_parking_type_text(self):
        ans = None
        if self.bike_parking_type.id != 0:
            ans = self.bike_parking_type.name

        return ans

    @property
    def bike_parking_roof_text(self):
        ans = None
        if self.bike_parking_type.is_exist and self.with_bike_parking_roof:
            ans = '屋根付き'

        return ans

    @property
    def bike_parking_fee_text(self):
        ans = None
        if self.bike_parking_type.id != 0:
            if self.bike_parking_type.is_paid:
                ans = ''
                if self.bike_parking_fee_lower > 0:
                    ans += '{0:,} 円'.format(self.bike_parking_fee_lower)
                if self.bike_parking_fee_upper > 0 and self.bike_parking_fee_upper > self.bike_parking_fee_lower:
                    ans += ' 〜 {0:,} 円'.format(self.bike_parking_fee_upper)
                if self.bike_parking_fee_tax_type.text:
                    ans += ' ' + self.bike_parking_fee_tax_type.text

                if ans == '':
                    ans = None

        return ans

    @property
    def department_name_text(self):
        company = Company.objects.get(pk=settings.COMPANY_ID)
        ans = company.company_name
        if self.department.id != 0:
            ans += " {0}".format(self.department.department_name)

        return ans

    @property
    def department_tel_text(self):
        ans = None
        if self.department.id != 0:
            ans = self.department.tel

        return ans

    @property
    def staff1_text(self):
        ans = None
        if self.staff1.id != 0:
            ans = self.staff1.last_name
            if self.staff1.department.id != 0:
                ans += "（{0}）".format(self.staff1.department.department_name)

        return ans

    @property
    def staff2_text(self):
        ans = None
        if self.staff2.id != 0:
            ans = self.staff2.last_name
            if self.staff2.department.id != 0:
                ans += "（{0}）".format(self.staff2.department.department_name)

        return ans

    @property
    def register_text(self):
        ans = ''

        if self.register_building_no:
            ans += "登記番号: {0}".format(self.register_building_no)

        if self.register_address:
            if ans != '':
                ans += ' / '
            ans += "登記地番: {0}".format(self.register_address)
            if self.register_building_no:
                ans += "（家屋番号: {0}）".format(self.register_building_no)

        if self.register_building_no:
            if ans != '':
                ans += ''

        return ans

    @property
    def agreement_existence_text(self):
        ans = None
        if self.agreement_existence_id != 0:
            ans = self.agreement_existence.name

        return ans

    @property
    def vacancy_recommend_comment(self):
        ans = None
        if self.is_vacancy_recommend:
            if self.vacancy_catch_copy:
                ans = self.vacancy_catch_copy
            elif self.vacancy_appeal:
                ans = self.vacancy_appeal

        return ans

    @property
    def trader_name_text(self):
        ans = None
        if self.trader:
            if self.trader.id != 0:
                ans = self.trader.trader_name

        return ans

    @property
    def trader_tel_text(self):
        ans = None
        if self.trader:
            if self.trader.id != 0:
                ans = self.trader.tel1

        return ans

    @property
    def owner_name_text(self):
        ans = None
        if self.owner:
            if self.owner.id != 0:
                ans = self.owner.owner_name

        return ans

    @property
    def owner_tel_text(self):
        ans = None
        if self.owner:
            if self.owner.id != 0:
                ans = self.owner.tel1

        return ans
