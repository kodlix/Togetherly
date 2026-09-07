from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from .models import Household, Membership


class AuthenticatedTestCase(TestCase):
    user_counter = 0

    def create_user(self, **kwargs):
        type(self).user_counter += 1
        defaults = {
            "username": f"test-user-{self.user_counter}",
            "password": "test-password",
        }
        defaults.update(kwargs)
        return get_user_model().objects.create_user(**defaults)

    def login_user(self, user=None):
        user = user or self.create_user()
        self.client.force_login(user)
        return user

    def logout_user(self):
        self.client.logout()


class HealthViewTests(AuthenticatedTestCase):
    def test_root_redirects_to_chores_health_endpoint(self):
        response = self.client.get("/")

        self.assertRedirects(response, reverse("chores:health"))

    def test_health_endpoint_returns_ok(self):
        response = self.client.get(reverse("chores:health"))

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "ok"})


class MembershipModelTests(AuthenticatedTestCase):
    def setUp(self):
        self.user = self.create_user()
        self.household = Household.objects.create(name="Home")

    def test_user_can_belong_to_multiple_households(self):
        other_household = Household.objects.create(name="Cabin")

        Membership.objects.create(
            user=self.user,
            household=self.household,
            role=Membership.Role.MEMBER,
        )
        Membership.objects.create(
            user=self.user,
            household=other_household,
            role=Membership.Role.MEMBER,
        )

        self.assertEqual(self.user.household_memberships.count(), 2)

    def test_household_has_at_most_one_owner_and_admin(self):
        Membership.objects.create(
            user=self.user,
            household=self.household,
            role=Membership.Role.OWNER,
        )
        other_user = self.create_user()
        duplicate_owner = Membership(
            user=other_user,
            household=self.household,
            role=Membership.Role.OWNER,
        )

        with self.assertRaises(IntegrityError):
            duplicate_owner.save()


class HouseholdViewTests(AuthenticatedTestCase):
    def test_anonymous_user_is_rejected(self):
        response = self.client.get(reverse("chores:households"))

        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_create_and_list_only_their_households(self):
        user = self.login_user()
        response = self.client.post(
            reverse("chores:households"),
            {"name": "Home"},
        )

        self.assertEqual(response.status_code, 201)
        household = Household.objects.get(name="Home")
        self.assertTrue(
            Membership.objects.filter(
                user=user,
                household=household,
                role=Membership.Role.OWNER,
            ).exists()
        )

        other_user = self.create_user()
        other_household = Household.objects.create(name="Other")
        Membership.objects.create(
            user=other_user,
            household=other_household,
            role=Membership.Role.MEMBER,
        )
        response = self.client.get(reverse("chores:households"))

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "households": [
                    {
                        "id": household.id,
                        "name": "Home",
                        "archived": False,
                        "role": Membership.Role.OWNER,
                    }
                ]
            },
        )
