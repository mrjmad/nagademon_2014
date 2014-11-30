# -*- coding: utf-8 -*-

from __future__ import (print_function, division, absolute_import, unicode_literals)
from django.utils.encoding import python_2_unicode_compatible

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models

from .history_elements import (Scene, Choice1PartSceneto1Scene,
                               Place, PlayerCharacter, Quest, PartScene)

USER_MODEL = settings.AUTH_USER_MODEL


@python_2_unicode_compatible
class GameSession(models.Model):
    start_date = models.DateTimeField(_("Start date of game session"))
    player = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Player"))
    character = models.ForeignKey(PlayerCharacter, verbose_name=_("Character of Player"))
    active = models.BooleanField(_("Active or not"), default=False)

    def __str__(self):
        return " %s at %s active :  %s " % (self.player, self.start_date, self.active)


@python_2_unicode_compatible
class HistoryScenesandChoices(models.Model):
    order = models.PositiveIntegerField(_("Order"))
    scene = models.ForeignKey(Scene, blank=True, null=True)
    scene_part = models.ForeignKey(PartScene)
    choice = models.ForeignKey(Choice1PartSceneto1Scene, blank=True, null=True)
    place = models.ForeignKey(Place, blank=True, null=True)
    game_session = models.ForeignKey(GameSession, verbose_name=_("Game Session"))

    def __str__(self):
        return " History scene number %s (scene = %s , part scene %s  and choice %s for game session ID %s " % (self.order,
                                        self.scene, self.scene_part, self.choice, self.game_session.pk)


@python_2_unicode_compatible
class PlacesKnowsByPlayer(models.Model):
    game_session = models.ForeignKey(GameSession, verbose_name=_("Game Session"))
    place = models.ForeignKey(Place, verbose_name=_("Places the Player knows"))
    passage_number = models.PositiveIntegerField("number of Player's Passage", default=0)

    def __str__(self):
        return " %s was know by  " % (self.place, self.game_session.player)


@python_2_unicode_compatible
class QuestStatus(models.Model):
    name = models.CharField(u"Type Object Name", max_length=200)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class QuestsFoundByPlayer(models.Model):
    game_session = models.ForeignKey(GameSession, verbose_name=_("Game Session"))
    quest = models.ForeignKey(Quest)
    status = models.ForeignKey(QuestStatus)
    start_date = models.DateTimeField(_("Start date of the quest"))
    time_spent = models.PositiveIntegerField(_("Time (in minutes) with the Quest ON"), default=0)

    def __str__(self):
        return " %s was found by  " % (self.title, self.game_session.player)
