from typing import List

from rest_framework.reverse import reverse, reverse_lazy
from rest_framework.test import APITestCase
from time import perf_counter
from rest_framework import status

from api.CRUD.serializers import MarkSerializer, UserSerializer
from api.tests.factories import UserFactory, BoardFactory, CardFactory, MarkFactory


class TestInvitation(APITestCase):

    def setUp(self):
        self.user = UserFactory()

        self.client.force_authenticate(user=self.user)
        self.url = reverse('invite-member-to-board')
        self.response_time = .1

    def test_invite_member_to_board(self):
        board = BoardFactory()

        start = perf_counter()
        response = self.client.post(self.url, data={'email': self.user.email, 'board': board.pk})
        end = perf_counter()

        self.assertIn(self.user, [user.user for user in board.member_boards.all()])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertLess(end - start, self.response_time)

    def test_adding_user_to_card(self):
        card = CardFactory()

        start = perf_counter()
        response = self.client.post(reverse('invite-member-to-card'), data={'email': self.user.email, 'card': card.pk})
        end = perf_counter()

        self.assertIn(self.user, [user.user for user in card.members.all()])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertLess(end - start, self.response_time)


class TestFavoriteBoardAPI(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.board = BoardFactory()
        self.url = reverse('favourite_boards')

        self.client.force_authenticate(user=self.user)
        self.response_time = .1

    def test_get_favourite_boards(self):
        start = perf_counter()
        response = self.client.get(self.url)
        end = perf_counter()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        self.assertLess(end - start, self.response_time)

    def test_addition_and_deletion_to_favorites(self):
        start = perf_counter()
        response = self.client.post(self.url, data={'board': self.board.pk})
        end = perf_counter()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(self.board, [board.board for board in self.user.users_faves.all()])
        self.assertLess(end - start, self.response_time)

        start = perf_counter()
        response = self.client.delete(self.url, data={'board': self.board.pk})
        end = perf_counter()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotIn(self.board, [board.board for board in self.user.users_faves.all()])
        self.assertLess(end - start, self.response_time)


class TestArchivingAPI(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.board = BoardFactory()
        self.url = reverse_lazy('archiving')

        self.client.force_authenticate(user=self.board.author)
        self.response_time = .1

    def test_get_archived_boards(self):
        start = perf_counter()
        response = self.client.get(self.url)
        end = perf_counter()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        self.assertLess(end - start, self.response_time)

    def test_archiving_and_restoring(self):
        start = perf_counter()
        response = self.client.post(self.url, data={'board': self.board.pk})
        end = perf_counter()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(end - start, self.response_time)

        start = perf_counter()
        response = self.client.delete(self.url, data={'board': self.board.pk})
        end = perf_counter()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.board.is_archived, False)
        self.assertLess(end - start, self.response_time)


class TestSearch(APITestCase):

    def setUp(self):
        self.user = UserFactory(first_name='Jonathan')

        self.client.force_authenticate(user=self.user)
        self.response_time = .1

    def test_search(self):
        start = perf_counter()
        response1 = self.client.get(reverse('search', kwargs={'query': 'Jo'}))
        end = perf_counter()

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertLess(end-start, self.response_time)


class TestMarking(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.mark = MarkFactory()
        self.card = CardFactory()

        self.client.force_authenticate(user=self.user)
        self.response_time = .1
        self.url = reverse('mark-a-card')

    def test_marking(self):
        start = perf_counter()
        response = self.client.post(self.url, data={'mark': self.mark.pk, 'card': self.card.pk})
        end = perf_counter()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(self.card, [card.card for card in self.mark.card_marks.all()])
        self.assertLess(end - start, self.response_time)

        start = perf_counter()
        response = self.client.delete(self.url, data={'mark': self.mark.pk, 'card': self.card.pk})
        end = perf_counter()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotIn(self.card, [card.card for card in self.mark.card_marks.all()])
        self.assertLess(end - start, self.response_time)
