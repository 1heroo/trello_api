from django.core.files.base import ContentFile

import api.models
import factory.fuzzy

from factory.django import DjangoModelFactory
from faker import Faker


class UserFactory(DjangoModelFactory):
    class Meta:
        model = api.models.MyUser
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(lambda user: '{}.{}@outlook.com'.format(user.first_name, user.last_name).lower())
    password = '123'


class BoardFactory(DjangoModelFactory):
    title = factory.fuzzy.FuzzyText(prefix='board_', length=20)
    is_archived = False
    author = factory.SubFactory(UserFactory)
    image = factory.LazyAttribute(
        lambda _: ContentFile(
            factory.django.ImageField()._make_data(
                {'width': 1024, 'height': 768}
            ), 'example.jpg'
        )
    )

    class Meta:
        model = api.models.Board


class ColumnFactory(DjangoModelFactory):
    title = factory.fuzzy.FuzzyText(prefix='column_', length=20)
    board = factory.SubFactory(BoardFactory)

    class Meta:
        model = api.models.Column


class CardFactory(DjangoModelFactory):
    title = factory.fuzzy.FuzzyText(prefix='card', length=20)
    description = factory.fuzzy.FuzzyText(length=200)
    deadline = factory.Faker('date')
    column = factory.SubFactory(ColumnFactory)
    created_at = factory.Faker('date')
    updated_at = factory.Faker('date')

    class Meta:
        model = api.models.Card


class MarkFactory(DjangoModelFactory):
    title = factory.fuzzy.FuzzyText(prefix='title_', length=15)
    colour = factory.fuzzy.FuzzyText(prefix='colour_', length=10)

    class Meta:
        model = api.models.Mark