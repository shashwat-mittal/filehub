from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models

from files.utils import get_size_in_largest_unit

User = get_user_model()


class Directory(models.Model):
    """
    Metadata for a directory.
    It has a one-to-many relation with itself to enable a directory tree.
    """

    id = models.UUIDField("id", primary_key=True, default=uuid4, editable=False)
    name = models.CharField("name", max_length=256)
    created_on = models.DateTimeField("created on", auto_now_add=True)
    last_modified = models.DateTimeField("last modified", auto_now=True)
    parent_directory = models.ForeignKey(
        "self",
        null=True,
        on_delete=models.CASCADE,
        related_name="subdirs",
        related_query_name="subdir",
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="dirs", related_query_name="dir"
    )

    class Meta:
        verbose_name_plural = "directories"

    def __str__(self) -> str:
        return self.name


class File(models.Model):
    """
    Metadata of a file.
    """

    id = models.UUIDField("id", primary_key=True, default=uuid4, editable=False)
    name = models.CharField("name", max_length=256)

    # filled using the file's mime type value
    type = models.CharField("file type", max_length=75)

    # represented in bytes
    size = models.PositiveBigIntegerField("file size")

    uploaded_on = models.DateTimeField("uploaded on", auto_now_add=True)
    directory = models.ForeignKey(
        Directory,
        on_delete=models.CASCADE,
        related_name="files",
        related_query_name="file",
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="files", related_query_name="file"
    )

    def __str__(self) -> str:
        return self.name

    def get_size(self) -> str:
        """
        Returns the size of the file in the largest possible unit.
        """
        unit, size = get_size_in_largest_unit(self.size)
        return f"{size} {unit}"
