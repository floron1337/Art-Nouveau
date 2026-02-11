from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

class User(AbstractUser):
    """
    Custom user model that extends the standard Django AbstractUser.
    Inherits fields: username, password, email, first_name, last_name.
    """

    blocked = models.BooleanField(default=False, help_text="If checked, the user cannot log in.")

    phone = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=50, blank=True)
    county = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=255, blank=True)

    code = models.CharField(max_length=100, null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.username

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

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="products"
    )

    TYPE_CHOICES = [
        ('Digital', 'Digital'),
        ('Poster', 'Poster'),
        ('Painting', 'Painting'),
        ('Sculpture', 'Sculpture'),
        ('Photography', 'Photography'),
    ]

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    author = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/product_images/', blank=True, null=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_id': self.id})

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

class UserProductView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    view_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-view_date']  # Cele mai recente primele

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.view_date})"


class Discount(models.Model):
    TEMPLATE_CHOICES = [
        ('Art_Nouveau/promo_formal.txt', 'Formal Promo Message'),
        ('Art_Nouveau/promo_urgent.txt', 'Urgent Promo Message'),
    ]

    name = models.CharField(max_length=100)
    email_subject = models.CharField(max_length=200, default="New sale!")

    message_template = models.CharField(
        max_length=100,
        choices=TEMPLATE_CHOICES,
        default='Art_Nouveau/promo_formal.txt',
    )

    creation_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()
    percent = models.PositiveIntegerField(
        default=0,
        help_text="Enter a value between 1 and 100"
    )

    # 5. Categoriile la care se aplica reducerea
    categories = models.ManyToManyField(
        Category,
        related_name="promotions",
        verbose_name="Categorii participante"
    )

    def __str__(self):
        return self.name
