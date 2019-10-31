

from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from quests.models import Quests, PACKAGE_SELECTION, CITY_SELECTION
from users.models import QuestrUserProfile

from rest_framework import exceptions, serializers, status

import simplejson as json
import logging

class QuestSerializer(serializers.ModelSerializer):
    questr = serializers.Field(source='questrs.displayname')
    class Meta:
        model = Quests
        fields = (
            'id',
            'title',
            'questr',
            'size',
            'description',
            'pickup',
            'dropoff',
            'pickup_time',
            'reward',
            'distance',
            'status',
            )

class NewQuestDataValidationSerializer(serializers.Serializer):
    title = serializers.CharField()
    size = serializers.ChoiceField(choices=PACKAGE_SELECTION)
    pickup_time = serializers.DateTimeField()
    description = serializers.CharField()
    srccity = serializers.ChoiceField(choices=CITY_SELECTION)
    srcaddress = serializers.CharField()
    srcaddress_2 = serializers.CharField(required=False)
    srcpostalcode = serializers.CharField()
    srcname = serializers.CharField()
    srcphone = serializers.CharField(required=False)
    dstcity = serializers.ChoiceField(choices=CITY_SELECTION)
    dstaddress = serializers.CharField()
    dstaddress_2 = serializers.CharField(required=False)
    dstpostalcode = serializers.CharField()
    dstname = serializers.CharField()
    dstphone = serializers.CharField(required=False)

class NewQuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quests
        fields = (
            'title',
            'size',
            'description',
            'pickup',
            'dropoff',
            'pickup_time',
            'reward',
            'distance',
            'questrs',
            'map_image'
            )

class PriceCalcSerializer(serializers.Serializer):
    size = serializers.ChoiceField(choices=PACKAGE_SELECTION, default="backpack")
    srccity = serializers.ChoiceField(choices=CITY_SELECTION, default="Toronto")
    srcaddress = serializers.CharField()
    srcaddress_2 = serializers.CharField(required=False)
    srcpostalcode = serializers.CharField()
    dstcity = serializers.ChoiceField(choices=CITY_SELECTION, default="Toronto")
    dstaddress = serializers.CharField()
    dstaddress_2 = serializers.CharField(required=False)
    dstpostalcode = serializers.CharField()

class StatusSeralizer(serializers.Serializer):
    status = serializers.BooleanField()

class QuestStatusSerializer(serializers.Serializer):
    quest = serializers.IntegerField()
    event = serializers.IntegerField()
    extrainfo = serializers.CharField()


class CourierSignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    class Meta:
        model = QuestrUserProfile
        fields = (
            'first_name',
            'last_name',
            'displayname',
            'phone',
            'password1',
            'password2',
            'email',
            )

    def restore_object(self, attrs, instance=None):
        instance = super(CourierSignupSerializer, self).restore_object(attrs, instance)
        instance.set_password(attrs['password2'])
        return instance

class CourierSignupValidationSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    displayname = serializers.CharField()
    phone = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    email = serializers.EmailField()

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')

        if len(password1) <=6 or len(password2) <=6:
            msg = _('Passwords must be of more than 6 characters.')
            raise serializers.ValidationError(dict(errors=msg, success=False))

        if password1 and password2 and password1 != password2:
            msg = _('Passwords do not match.')
            raise serializers.ValidationError(dict(errors=msg, success=False))

        return password2

class QuestrSerializer(serializers.ModelSerializer):

    avatar = serializers.Field('get_profile_pic')

    class Meta:
        model = QuestrUserProfile
        fields = (
            'id',
            'first_name',
            'last_name',
            'displayname',
            'email',
            'phone',
            'avatar',
            )

class QuestrUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestrUserProfile
        fields = (
            'id',
            'first_name',
            'last_name',
            'displayname',
            'email',
            'phone',
            'avatar',
            )