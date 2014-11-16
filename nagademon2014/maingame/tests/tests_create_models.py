# -*- coding: utf-8 -*-
from __future__ import (print_function, division, absolute_import, unicode_literals)

import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import (PlayerCharacter, Scene, Choice1Sceneto1Scene, Place,
                    NPCharacter, Quest, ObjectType, OneObject, GameSession, HistoryScenesandChoices)


def utils_create_two_player_character(testcase):
    testcase.pc1 = PlayerCharacter.objects.create(short_name="pc1", first_name="fname1", last_name='lname1', gender=1,
                                                  description="desc")
    testcase.pc2 = PlayerCharacter.objects.create(short_name="pc2", first_name="fname2", last_name='lname2', gender=2,
                                                  description="desc")


def utils_create_two_np_character(testcase):
    testcase.npc1 = NPCharacter.objects.create(short_name="npc1", first_name="fname1", last_name='lname1', gender=1,
                                                  description="desc")
    testcase.npc2 = NPCharacter.objects.create(short_name="npc2", first_name="fname2", last_name='lname2', gender=2,
                                                  description="desc")


def utils_create_two_scenes_with_one_place(testcase):
    testcase.p = p = Place.objects.create(short_name="p1", name="Pname", text="Ptext", filename="Pfilename")
    testcase.sc1 = Scene.objects.create(short_name="sc1", name="sc1", text="tsc1", filename="sc1filename")
    testcase.sc2 = Scene.objects.create(short_name="sc2", name="sc2", text="tsc2", filename="sc2filename",
                         place=p)


def utils_create_object_type():
    tobj1 = ObjectType.create(name='crowbar', short_name='crowbar')
    tobj2 = ObjectType.create(name='mug', short_name='mug')
    return tobj1, tobj2


def utils_create_game_session(testcase, user, character):
    halloween = datetime.datetime(year=2014, month=10, day=31, hour=23, minute=59)
    testcase.gsession = GameSession.objects.create(start_date=halloween, player=user, active=True,
                                                   character=character)


def utils_create_two_scene_one_choice_by_scene(testcase):
    utils_create_two_scenes_with_one_place(testcase)
    testcase.ch1 = Choice1Sceneto1Scene.objects.create(text="Choic1", for_scene=testcase.sc1, next_scene=testcase.sc2)
    testcase.ch2 = Choice1Sceneto1Scene.objects.create(text="Choic2", for_scene=testcase.sc2, next_scene=testcase.sc1)


class CreateModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='user2')

    def test_create_player_character_01(self):
        utils_create_two_player_character(self)
        self.assertIsInstance(self.pc2, PlayerCharacter)
        self.assertEqual(2, PlayerCharacter.objects.all().count())

    def test_create_np_character_01(self):
        utils_create_two_np_character(self)
        self.assertIsInstance(self.npc2, NPCharacter)
        self.assertEqual(2, NPCharacter.objects.all().count())

    def test_create_place(self):
        Place.objects.create(short_name="pc1", name="Pname", text="Ptext", filename="Pfilename")
        self.assertEqual(1, Place.objects.all().count())

    def test_create_scene(self):
        utils_create_two_scenes_with_one_place(self)
        self.assertEqual(2, Scene.objects.all().count())

    def test_create_choice(self):
        utils_create_two_scene_one_choice_by_scene
        self.assertEqual(2, Choice1Sceneto1Scene.objects.all().count())
        self.assertEqual(1, self.sc1.current_choices_set.all().count())
        ch = self.sc1.current_choices_set.all()[0]
        self.assertEqual(self.ch1, ch)

    def test_create_quest(self):
        utils_create_two_scenes_with_one_place(self)
        utils_create_two_np_character(self)
        Quest.objects.create(short_name="qu1", title="title", text="Text",
                             timedelta=12,
                             given_by=self.npc1,
                             scene=self.sc1,
                             validation_function='FU')
        self.assertEqual(1, Quest.objects.all().count())

    def test_create_objecttype(self):
        ObjectType.create(name='crowbar', short_name='crowbar')
        ObjectType.create(name='coffee mug', short_name='cmug')
        self.assertEqual(1, ObjectType.objects.all().count())

    def test_create_oneobject(self):
        utils_create_two_scenes_with_one_place(self)
        objtype1, objtype2 = utils_create_object_type()
        OneObject.objects.create(name="Mom's Crowbar", initial_place=self.p,
                                    store_in=self.p, type=objtype1)
        OneObject.objects.create(name="Best Pyro of the Year", initial_place=self.p, type=objtype2)
        self.assertEqual(2, OneObject.objects.all().count())
        self.assertEqual(self.p, OneObject.objects.all()[0])

    def test_create_game_session(self):
        utils_create_two_player_character(self)
        utils_create_game_session(self, self.user, self.pc2)
        self.assertEqual(1, GameSession.objects.all().count())

    def test_create_history(self):
        utils_create_two_scene_one_choice_by_scene(self)
        utils_create_two_player_character(self)
        utils_create_game_session(self, self.user, self.pc2)

        HistoryScenesandChoices.objects.create(order=1,
                                               scene=self.sc1,
                                               choice=self.ch1,
                                               place=self.p,
                                               game_session=self.gm)
        self.assertEqual(1, HistoryScenesandChoices.objects.all().count())
