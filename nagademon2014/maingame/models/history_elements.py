# -*- coding: utf-8 -*-

from __future__ import (print_function, division, absolute_import, unicode_literals)
from django.utils.encoding import python_2_unicode_compatible

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models

USER_MODEL = settings.AUTH_USER_MODEL


@python_2_unicode_compatible
class Character(models.Model):
    short_name = models.CharField(_("NPC's short Name"), max_length=20, unique=True)
    first_name = models.CharField("Firstname of Character", max_length=50)
    last_name = models.CharField("Lastname of Character", max_length=50)
    gender = models.PositiveSmallIntegerField(u"Gender of Character")
    description = models.TextField("Description")

    def __str__(self):
        return u"%s  %s" % (self.first_name, self.last_name)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class PlayerCharacter(Character):

    def __str__(self):
        return u"PC : %s  %s" % (self.first_name, self.last_name)


@python_2_unicode_compatible
class NPCharacter(Character):

    def __str__(self):
        return u"NPC : %s  %s" % (self.first_name, self.last_name)


class PlaceManager(models.Manager):
    def get_by_natural_key(self, short_name):
        return self.get(short_name=short_name)


@python_2_unicode_compatible
class Place(models.Model):
    objects = PlaceManager()
    begin_sound = models.CharField(_("Begin's Sound"), max_length=200, blank=True, null=True)
    ambiance_sound = models.CharField(_("Ambiance's Sound"), max_length=200, blank=True, null=True)
    short_name = models.CharField(_("Place's short Name"), max_length=20, unique=True)
    name = models.CharField("Scene's Name", max_length=200)
    filename = models.CharField("Scene's Filename", max_length=80)
    text = models.TextField("Scene's Text")

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.short_name,


@python_2_unicode_compatible
class Scene(models.Model):
    short_name = models.CharField(_("Scene's short Name"), max_length=20, unique=True)
    name = models.CharField("Scene's Name", max_length=200)
    filename = models.CharField("Scene's Filename", max_length=80)
    begin_sound = models.CharField(_("Begin's Sound"), max_length=200, blank=True, null=True)
    ambiance_sound = models.CharField(_("Ambiance's Sound"), max_length=200, blank=True, null=True)
    synopsis = models.TextField("Scene's synopsis, only for authors")
    final = models.BooleanField("Final Round ?", default=False)
    place = models.ForeignKey(Place, verbose_name="Scene's Place",
                              blank=True, null=True)
    is_active = models.BooleanField(_("Is active ?"), default=True)
    order = models.PositiveIntegerField(_("Scene's Order"), default=0)
    need_a_trigger = models.BooleanField(_("Activable only by a trigger"), default=False)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class PartScene(models.Model):
    text = models.CharField("Scene's Text", max_length=400)
    for_scene = models.ForeignKey(Scene, verbose_name="Scene")
    limited_to_player = models.ForeignKey(PlayerCharacter, blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "Text %s |for scene :%s" % (self.text, self.for_scene)


@python_2_unicode_compatible
class Choice1PartSceneto1Scene(models.Model):
    text = models.CharField("Choice's Text", max_length=400)
    for_part_scene = models.ForeignKey(PartScene, verbose_name="Current Part Scene",
                                  related_name="current_choices_set")
    next_scene = models.ForeignKey(Scene, verbose_name="Next Scene",
                                   related_name="leading_choices_set",
                                   null=True, blank=True)
    next_part_scene = models.ForeignKey(PartScene, verbose_name="Next Part Scene",
                                   related_name="leading_choices_set",
                                   null=True, blank=True)

    def __str__(self):
        return "%s |for scene %s , part scene id :%s" % (self.text,
                                                         self.for_part_scene.for_scene,
                                                         self.for_part_scene.id)


@python_2_unicode_compatible
class Quest(models.Model):
    short_name = models.CharField(_("Quest's short Name"), max_length=20, unique=True)
    title = models.CharField("Quest's Title", max_length=140)
    text = models.TextField("Quest's Text")
    time_frame = models.PositiveIntegerField(_("Maximum Time (in minutes) for validate the Quest"), default=0)
    given_by = models.ForeignKey(NPCharacter, verbose_name=_('Given by'))
    scene = models.ForeignKey(Scene, verbose_name=_("Scene who Quest is activable"),
                              related_name=_("quests_for_scene"))
    scene_after = models.ForeignKey(Scene, verbose_name=_("Scene after the End's Quest"),
                                   related_name=_("finished_quests_for_scene"))
    apparition_function = models.CharField(_("Name of Apparition's Function"), max_length=120, blank=True, null=True)
    validation_function = models.CharField(_("Name of Validation's Function"), max_length=120)

    def __str__(self):
        return "%s | for scene :%s, by NPC %s in time %s" % (self.title, self.scene, self.given_by,
                                                          self.timedelta)


class ObjectType(models.Model):
    name = models.CharField(u"Type Object Name", max_length=200)
    description = models.TextField("Type's Description", blank=True, null=True)
    short_name = models.CharField(_("Type Object's short Name"), max_length=20, unique=True)


class OneObject(models.Model):
    name = models.CharField(_("Type Object Name"), max_length=200)
    type = models.ForeignKey(ObjectType, verbose_name=_("Object's Type"))
    description = models.TextField("Object's Description", blank=True, null=True)
    initial_place = models.ForeignKey(Place, verbose_name=_("Object's Initial place"),
                                            related_name=_("initial_objects_set"), blank=True, null=True)
    stored_in = models.ForeignKey(Place, related_name=_("objects_stored_set"),
                                  verbose_name=_("Where the object is stored"), blank=True, null=True)
