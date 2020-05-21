"""=============================================================
~/creel_portal/creel_portal/tests/factories/common_factories.py
 Created: 03 Apr 2020 10:49:27

 DESCRIPTION:

  Factories for our user object. This factory should work equally as
  well for the built in django user or custom user models.

 A. Cottrill
=============================================================

"""


import factory

from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    email = "homer@simpsons.com"
    first_name = "Homer"
    last_name = "Simpson"

    @factory.lazy_attribute
    def username(a):

        my_username = a.last_name + a.first_name[:2]
        return my_username.lower()
