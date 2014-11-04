# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models


@python_2_unicode_compatible
class PlayerCharacter(models.Model):
    first_name = models.CharField("Firstname of Character", max_length=50)
    last_name = models.CharField("Lastname of Character", max_length=50)
    gender = models.PositiveSmallIntegerField(u"Gender of Character")
    description = models.TextField("Description")

    def __str__(self):
        return u"%s  %s" % (self.first_name, self.last_name)


@python_2_unicode_compatible
class Place(models.Model):
    name = models.CharField("Scene's Name", max_length=200)
    filename = models.CharField("Scene's Filename", max_length=80)
    text = models.TextField("Scene's Text")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Scene(models.Model):
    name = models.CharField("Scene's Name", max_length=200)
    filename = models.CharField("Scene's Filename", max_length=80)
    text = models.TextField("Scene's Text")
    final = models.BooleanField("Final Round ?", default=False)
    place = models.ForeignKey(Place, verbose_name="Scene's Place",
                              blank=True, null=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Choice(models.Model):
    text = models.CharField("Choice's Text", max_length=400)
    for_scene = models.ForeignKey(Scene, verbose_name="Current Scene",
                                  related_name="current_choices_set")
    next_scene = models.ForeignKey(Scene, verbose_name="Next Scene",
                                   related_name="leading_choices_set")

    def __str__(self):
        return "%s |scene :%s" % (self.text, self.for_scene)
