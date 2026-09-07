from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Household(models.Model):
    name = models.CharField(max_length=200)
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name", "id")

    def __str__(self):
        return self.name


class Membership(models.Model):
    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        ADMIN = "admin", "Admin"
        MEMBER = "member", "Member"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="household_memberships"
    )
    household = models.ForeignKey(
        Household,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("user", "household"),
                name="unique_household_membership",
            ),
            models.UniqueConstraint(
                fields=("household", "role"),
                condition=models.Q(role__in=("owner", "admin")),
                name="unique_active_household_owner_or_admin",
            ),
        ]
        ordering = ("household", "user")

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.role not in self.Role.values:
            raise ValidationError({"role": "Select a valid household role."})

        if self.household_id and self.household.archived:
            return

        if self.role in (self.Role.OWNER, self.Role.ADMIN):
            existing = (
                type(self)
                .objects.filter(
                    household_id=self.household_id,
                    role=self.role,
                )
                .exclude(pk=self.pk)
            )
            if existing.exists():
                role_name = self.Role(self.role).label
                raise ValidationError(
                    {"role": f"An active household can have only one {role_name}."}
                )

    def __str__(self):
        return f"{self.user} - {self.household} ({self.role})"


# Create your models here.
