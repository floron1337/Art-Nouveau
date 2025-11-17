from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon_url = models.URLField(max_length=300, blank=True)
    slug = models.SlugField(max_length=110, unique=True, blank=True,
                            help_text="auto generated if left empty")

    icon_class = models.CharField(max_length=50, blank=True,
                                  help_text="Ex: 'fas fa-paint-brush' sau 'fa fa-palette'")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_products', kwargs={'category_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

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
    id = models.AutoField(primary_key=True)
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
    price = models.FloatField(default=0)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='Art_Nouveau/static/product_images/', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_id': self.id})

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
    products = models.ManyToManyField(Product, related_name="awards")
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    award_image_url = models.URLField(max_length=300, blank=True)

    def __str__(self):
        return self.name


class Exhibition(models.Model):
    exhibition_id = models.AutoField(primary_key=True)
    products = models.ManyToManyField(Product, related_name="exhibitions")
    description = models.TextField(blank=True)
    banner_image_url = models.URLField(max_length=300, blank=True)

    def __str__(self):
        return f"Exhibition #{self.exhibition_id}"
