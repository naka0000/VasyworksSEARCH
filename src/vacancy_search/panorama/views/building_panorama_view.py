"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
"""
import os
import datetime
from abc import ABCMeta, abstractmethod
from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.utils.translation import gettext_lazy as _
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.views.generic import TemplateView, FormView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from dateutil.relativedelta import relativedelta
from PIL import Image
from lib.convert import *
from rent_db.models import *


class BuildingPanoramaView(TemplateView):
    """
    建物パノラマ
    """
    template_name = 'panorama/panorama.html'

    def __init__(self, **kwargs):
        self.user = None
        self.company = None
        self.panorama = None

        super().__init__(**kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = self.request.user
        if not self.user:
            raise Http404

        self.company = Company.get_instance()

        panorama_id = 0
        try:
            idb64 = force_text(urlsafe_base64_decode(kwargs.get('idb64')))
            if idb64.isdecimal():
                panorama_id = xint(idb64)
        except ValueError:
            raise Http404

        self.panorama = get_object_or_404(BuildingPanorama, pk=panorama_id)
        self.panorama.building.auth_user = self.user

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        context['company'] = self.company
        context['building'] = self.panorama.building
        context['panorama'] = self.panorama

        return context
