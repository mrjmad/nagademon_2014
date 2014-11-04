# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import PlayerCharacter, Scene, Choice, Place


def utils_create_two_player_character(testcase):
    testcase.pc1 = PlayerCharacter.objects.create(first_name="fname1", last_name='lname1', gender=1,
                                                  description="desc")
    testcase.pc2 = PlayerCharacter.objects.create(first_name="fname2", last_name='lname2', gender=2,
                                                  description="desc")


def create_two_scenes_with_one_place(testcase):
    testcase.p = p = Place.objects.create(name="Pname", text="Ptext", filename="Pfilename")
    testcase.sc1 = Scene.objects.create(name="sc1", text="tsc1", filename="sc1filename")
    testcase.sc2 = Scene.objects.create(name="sc2", text="tsc2", filename="sc2filename",
                         place=p)


class CreateModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='user2')

    def test_create_player_character_01(self):
        utils_create_two_player_character(self)
        self.assertIsInstance(self.pc2, PlayerCharacter)
        self.assertEqual(2, PlayerCharacter.objects.all().count())

    def test_create_place(self):
        Place.objects.create(name="Pname", text="Ptext", filename="Pfilename")
        self.assertEqual(1, Place.objects.all().count())

    def test_create_scene(self):
        create_two_scenes_with_one_place(self)
        self.assertEqual(2, Scene.objects.all().count())

    def test_create_choice(self):
        create_two_scenes_with_one_place(self)
        ch1 = Choice.objects.create(text="Choic1", for_scene=self.sc1, next_scene=self.sc2)
        Choice.objects.create(text="Choic2", for_scene=self.sc2, next_scene=self.sc1)
        self.assertEqual(2, Choice.objects.all().count())
        self.assertEqual(1, self.sc1.current_choices_set.all().count())
        ch = self.sc1.current_choices_set.all()[0]
        self.assertEqual(ch1, ch)
