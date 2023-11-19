from django.db import models
from django.utils import timezone
import os
from ordered_model.models import OrderedModel

# Create your models here.


def get_image_path(instance, filename):
    # Rename the uploaded file to the object's name
    return os.path.join("media", "properties", str(instance.property_name), filename)


class Slider(models.Model):
    image1 = models.FileField(("Image 1"), upload_to="media/slider")
    image2 = models.FileField(("Image 2"), upload_to="media/slider")
    image3 = models.FileField(("Image 3"), upload_to="media/slider")

    def __str__(self):
        return "Main Page Slider"

    class Meta:
        verbose_name = "Slider"
        verbose_name_plural = "Slider"


class Category(models.Model):
    category = models.TextField("Category", default="", max_length=5000, blank=True)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Bed(models.Model):
    bed = models.TextField("Bedrooms", default="", max_length=5000, blank=True)
    bed_value = models.TextField(
        "Bedroom Value (Do not put/edit anything here)",
        default="",
        max_length=5000,
        blank=True,
    )

    def __str__(self):
        return self.bed

    def save(self, *args, **kwargs):
        if self.bed:
            self.bed_value = self.bed.split(" ")[0]

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Bedroom"
        verbose_name_plural = "Bedrooms"


class Reviews(OrderedModel):
    client_name = models.TextField(
        "Client Name", default="", max_length=5000, blank=True
    )
    client_review = models.TextField(
        "Client Review", default="", max_length=50000, blank=True
    )
    client_image = models.FileField(("Client Photo"), upload_to="media/reviews")
    order = models.PositiveIntegerField(editable=False, db_index=True)

    def __str__(self):
        return "Main Page Reviews"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ("order",)


class Gallery(models.Model):
    image1 = models.FileField(("Image 1 (max size 150x150)"), upload_to="media/gallery")
    image2 = models.FileField(("Image 2 (max size 150x150)"), upload_to="media/gallery")
    image3 = models.FileField(("Image 3 (max size 150x150)"), upload_to="media/gallery")
    image4 = models.FileField(("Image 4 (max size 150x150)"), upload_to="media/gallery")
    image5 = models.FileField(("Image 5 (max size 150x150)"), upload_to="media/gallery")
    image6 = models.FileField(("Image 6 (max size 150x150)"), upload_to="media/gallery")

    def __str__(self):
        return "Gallery"

    class Meta:
        verbose_name = "Gallery"
        verbose_name_plural = "Gallery"


class Property(OrderedModel):
    property_name = models.TextField(
        ("Property Name"), default="", max_length=5000, blank=True
    )

    property_accommodation_type = models.TextField(
        ("Property Type (Appartments, Villa, Penthouse, etc.)"),
        default="",
        max_length=5000,
        blank=True,
    )

    property_location = models.TextField(
        ("Property Location (name)"),
        default="",
        max_length=5000,
        blank=True,
    )

    property_location_description = models.TextField(
        ("Property Location Description"),
        default="",
        max_length=50000,
        blank=True,
    )

    property_units = models.TextField(
        ("Property Units Description"),
        default="",
        max_length=50000,
        blank=True,
    )

    property_payment_plan = models.TextField(
        ("Property Payment Plan"),
        default="",
        max_length=5000,
        blank=True,
    )

    property_developer = models.TextField(
        ("Property Developer"),
        default="",
        max_length=5000,
        blank=True,
    )

    property_bed_number = models.TextField(
        ("Property Bed Number"),
        default="",
        max_length=5000,
        blank=True,
    )

    property_description = models.TextField(
        ("Property Description"),
        default="",
        max_length=50000,
        blank=True,
    )

    property_amenities = models.TextField(
        ("Property Amenities"),
        default="",
        max_length=50000,
        blank=True,
    )

    property_starting_price_aed = models.TextField(
        ("Property Starting Price (AED)"),
        default="",
        max_length=5000,
        blank=True,
    )

    property_starting_price_usd = models.TextField(
        ("Property Starting Price (USD)"),
        default="",
        max_length=5000,
        blank=True,
    )

    property_highlights = models.TextField(
        ("Highlights"),
        default="",
        max_length=5000,
        blank=True,
    )

    property_type = models.TextField(
        ("Property Type"),
        default="Offplan",
        max_length=5000,
        blank=True,
    )

    property_image1 = models.FileField(
        ("Image 1"), upload_to=get_image_path, default="", blank=True
    )
    property_image2 = models.FileField(
        ("Image 2"), upload_to=get_image_path, default="", blank=True
    )
    property_image3 = models.FileField(
        ("Image 3"), upload_to=get_image_path, default="", blank=True
    )
    property_image4 = models.FileField(
        ("Image 4"), upload_to=get_image_path, default="", blank=True
    )
    property_image5 = models.FileField(
        ("Image 5"), upload_to=get_image_path, default="", blank=True
    )
    property_image6 = models.FileField(
        ("Image 6"), upload_to=get_image_path, default="", blank=True
    )
    property_image7 = models.FileField(
        ("Image 7"), upload_to=get_image_path, default="", blank=True
    )
    property_image8 = models.FileField(
        ("Image 8"), upload_to=get_image_path, default="", blank=True
    )
    property_image9 = models.FileField(
        ("Image 9"), upload_to=get_image_path, default="", blank=True
    )

    date = models.DateTimeField(("Time added"), default=timezone.now())

    order = models.PositiveIntegerField(editable=False, db_index=True)

    def __str__(self):
        return self.property_name

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
        ordering = ("order",)
        # ordering = ["date"]


class MainPageProperty(Property):
    class Meta:
        proxy = True
