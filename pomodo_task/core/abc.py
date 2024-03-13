from django.db import models
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.utils import timezone

User = get_user_model()


class CoreModel(models.Model):
    """
    Abstract base class for models in the core app.
    Provides soft-delete functionality and automatic tracking of created_by and updated_by users.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_created",
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_updated",
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """Soft delete the object."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """Restore the soft-deleted object."""
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    def hard_delete(self):
        """Permanently delete the object from the database."""
        super().delete()

    def save(self, *args, **kwargs):
        """Automatically set created_by and updated_by fields."""
        user = getattr(self, "request", None) and self.request.user or None
        if self.pk:
            self.updated_by = user
        else:
            self.created_by = user
        super().save(*args, **kwargs)

    def clean(self):
        """Additional model validation."""
        if self.updated_at and self.created_at and self.updated_at < self.created_at:
            raise ValidationError("updated_at must be greater than created_at")
        super().clean()
