# -*- coding: utf-8 -*-

from __future__ import (print_function, division, absolute_import, unicode_literals)
from django.utils.encoding import python_2_unicode_compatible

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models

from .history_elements import Scene, Choice1Sceneto1Scene, Place, PlayerCharacter

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
    choice = models.ForeignKey(Choice1Sceneto1Scene, blank=True, null=True)
    place = models.ForeignKey(Place, blank=True, null=True)
    game_session = models.ForeignKey(GameSession)

    def __str__(self):
        return " History scene number %s (scene = %s and choice %s for game session ID %s " % (self.order,
                                        self.scene, self.choice, self.game_session.pk)
