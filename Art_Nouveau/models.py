from django.db import models


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon_url = models.URLField(max_length=300, blank=True)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    TYPE_CHOICES = [
        ('Digital', 'Digital'),
        ('Poster', 'Poster'),
        ('Painting', 'Painting'),
        ('Sculpture', 'Sculpture'),
        ('Photography', 'Photography'),
    ]

    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField(blank=True)
    physical = models.BooleanField(default=False)

    def __str__(self):
        return self.type_name


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="products"
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="products"
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    author = models.CharField(max_length=100)
    price = models.FloatField()
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    author = models.CharField(max_length=100)
    image_url = models.URLField(max_length=300)

    def __str__(self):
        return f"Image {self.image_id} - {self.product.name}"


class Discount(models.Model):
    discount_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="discounts"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    percentage = models.FloatField()
    title = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.title} ({self.percentage}%)"


class Award(models.Model):
    award_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="awards"
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    award_image_url = models.URLField(max_length=300, blank=True)

    def __str__(self):
        return self.name


class Exhibition(models.Model):
    exhibition_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="exhibitions"
    )
    description = models.TextField(blank=True)
    banner_image_url = models.URLField(max_length=300, blank=True)

    def __str__(self):
        return f"Exhibition #{self.exhibition_id} - {self.product.name}"
