

#All Django Imports
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

#All local imports (libs, contribs, models)
from users.models import *

#All external imports (libs, packages)
import hashlib
import jsonfield
import logging
import pytz
import uuid

# Init Logger
logger = logging.getLogger(__name__)

PACKAGE_SELECTION = (
    ('car', 'Car'),
    ('van', 'Van'),
    ('minivan', 'Minivan'),
)

STATUS_SELECTION = (
    ('new', 'New'),
    ('accepted', 'Accepted'),
    ('completed', 'Completed')
)
CITY_SELECTION = (
    ('Toronto', 'Toronto'),
    ('Brampton', 'Brampton'),
    ('Markham', 'Markham'),
    ('Mississauga', 'Mississauga'),
    ('Richmond Hill', 'Richmond Hill'),
    ('Vaughan', 'Vaughan'),
    ('Oakville', 'Oakville')
)


def validate_pickuptime(pickup_time):
    if (
        pickup_time - timezone.now().astimezone(
            pytz.timezone(settings.TIME_ZONE))
    ).total_seconds() < 0:
        raise ValidationError('Pickup time cannot be before current time!')


class Quests(models.Model):

    # Calculating delivery code before hand and inserting
    # it as default so that it won't be tampered with.
    hashstring = hashlib.sha256(
        str(timezone.now()) + str(timezone.now()) + str(uuid.uuid4())
    ).hexdigest()
    calc_delivery_code = hashstring[:3]+hashstring[-2:]
    calc_tracking_number = hashstring[10:15]+hashstring[-15:-10]
    current_time = timezone.now

    questrs = models.ForeignKey(QuestrUserProfile, related_name='quests')
    description = models.TextField(_('description'), blank=True)
    title = models.CharField(
        _('title'),
        max_length=100,
        blank=False
    )
    reward = models.DecimalField(
        _('reward'),
        decimal_places=2,
        max_digits=1000)
    item_images = models.ImageField(
        _('item_images'),
        max_length=9999,
        upload_to='quest-item-cdn',
        blank=True
    )
    map_image = models.URLField(
        _('map_image'),
        max_length=9999,
        default=''
    )
    status = models.TextField(
        _('status'),
        choices=STATUS_SELECTION,
        default='New'
    )
    creation_date = models.DateTimeField(
        _('creation_date'),
        default=current_time
    )
    size = models.TextField(
        _('size'),
        choices=PACKAGE_SELECTION,
        default="backpack"
    )
    shipper = models.TextField(
        _('shipper'),
        blank=True,
        null=True
    )
    pickup = jsonfield.JSONField(_('pickup'), default={})
    dropoff = jsonfield.JSONField(_('dropoff'), default={})
    isaccepted = models.BooleanField(_('isaccepted'), default=False)
    isnotified = models.BooleanField(_('isnotified'), default=False)
    is_questr_reviewed = models.BooleanField(
        _('is_questr_reviewed'),
        default=False
    )
    is_shipper_reviewed = models.BooleanField(
        _('is_shipper_reviewed'),
        default=False
    )
    is_complete = models.BooleanField(_('is_complete'), default=False)
    ishidden = models.BooleanField(_('ishidden'), default=False)
    distance = models.DecimalField(
        _('distance'),
        decimal_places=2,
        max_digits=1000,
        default=0
    )
    delivery_date = models.DateTimeField(
        _('delivery_date'),
        blank=True,
        null=True
    )
    available_couriers = jsonfield.JSONField(
        _('available_couriers'),
        default={}
    )
    delivery_code = models.TextField(_('delivery_code'), blank=True)
    tracking_number = models.TextField(_('tracking_number'), blank=True)
    pickup_time = models.DateTimeField(
        _('pickup_time'),
        blank=True,
        validators=[validate_pickuptime]
    )
    considered_couriers = models.TextField(_('considered_couriers'), default=[])

    def __unicode__(self):
        return str(self.id)

    def get_delivery_code(self):
        hashstring = hashlib.sha256(
            str(timezone.now()) + str(timezone.now()) + str(uuid.uuid4())
        ).hexdigest()
        return hashstring[:3]+hashstring[-2:]

    def get_tracking_number(self):
        hashstring = hashlib.sha256(
            str(timezone.now()) + str(timezone.now()) + str(uuid.uuid4())
        ).hexdigest()
        return hashstring[10:15]+hashstring[-15:-10]

        #Overriding
    def save(self, *args, **kwargs):
        if not self.delivery_code:
            self.delivery_code = self.get_delivery_code()

        if not self.tracking_number:
            self.tracking_number = self.get_tracking_number()

        if not self.pickup_time:
            logging.warn("no pickup time")
            self.pickup_time = self.creation_date

        super(Quests, self).save(*args, **kwargs)
        # self.create_item_images_normal()


class QuestComments(models.Model):
    quest = models.ForeignKey(Quests)
    questr = models.ForeignKey(QuestrUserProfile)
    time = models.DateTimeField(_('time'))
    comment = models.TextField(_('comment'))

    def __unicode__(self):
        return self.id


class QuestTransactional(models.Model):
    quest_code = models.CharField(_('quest_code'), max_length=64, unique=True)
    quest = models.ForeignKey(Quests)
    shipper = models.ForeignKey(QuestrUserProfile)
    transaction_type = models.IntegerField(_('transaction_type'), default=1)
    status = models.BooleanField(_('status'), default=False)

    def generate_hash(self):
        return hashlib.sha256(
            str(timezone.now()) + str(self.shipper.email)
        ).hexdigest()

    def get_truncated_quest_code(self):
        return self.quest_code[:7]

    def get_token_id(self):
        return self.quest_code[-6:]

    REQUIRED_FIELDS = [
        'quest_code', 'id', 'quest', 'shipper', 'transaction_type']

    def __unicode__(self):
        return "{0}:{1} {2}".format(self.quest_code, self.quest, self.shipper)

    #Overriding
    def save(self, *args, **kwargs):
        #check if the row with this hash already exists.
        if not self.quest_code:
            self.quest_code = self.generate_hash()
        # self.my_stuff = 'something I want to save in that field'
        super(QuestTransactional, self).save(*args, **kwargs)


class QuestToken(models.Model):
    token_id = models.CharField(_('id'), max_length=20, primary_key=True)
    timeframe = models.DateTimeField(_('create_date'), default=timezone.now)

    def is_alive(self):
        timedelta = timezone.now() - self.timeframe
        hours = 2
        allowable_time = float(hours * 60 * 60)
        return timedelta.total_seconds() < allowable_time

    def __unicode__(self):
        return "Token verifying ..."

    # Overriding
    def save(self, *args, **kwargs):
        if not self.timeframe:
            self.timeframe = timezone.now()
        super(QuestToken, self).save(*args, **kwargs)


class QuestEvents(models.Model):
    """Models for QuestEvents"""
    current_time = timezone.now

    quest = models.ForeignKey(Quests)
    event = models.IntegerField(_('event'), max_length=2, default=1)
    updated_on = models.DateTimeField(
        _('updated_on'),
        default=current_time
    )
    extrainfo = jsonfield.JSONField(
        _('extrainfo'),
        default='{}',
        max_length=9999
    )

    def save(self, *args, **kwargs):
        if not self.updated_on:
            self.updated_on = current_time
        super(QuestEvents, self).save(*args, **kwargs)

# class QuestPricing(models.Model):
#     """Pricing model for quests"""
#     current_time = timezone.now

#     pricing = jsonfield.JSONField(_('pricing'), default={})
#     questrs = models.ForeignKey(QuestrUserProfile, unique=True)
#     updated_on = models.DateTimeField(
#         _('updated_on'),
#         default=current_time
#     )

#     def save(self, *args, **kwargs):
#         if not self.updated_on:
#             self.updated_on = current_time
#         super(QuestPricing, self).save(*args, **kwargs)
