import re
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from datetime import date, datetime
from .models import Category, Product, User, Discount
from .utils import send_custom_admin_email
import logging

logger = logging.getLogger('django')

class ProductFilterForm(forms.Form):
    name = forms.CharField(
        required=False,
        label='Product Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by name...'})
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label='Category',
        empty_label="All Categories",
        error_messages={
            'invalid_choice': 'The selected category does not exist. Please do not modify form values manually.'
        }
    )

    description = forms.CharField(
        required=False,
        label='Description',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Keywords...'})
    )

    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        label='Min Price',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        label='Max Price',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )

    items_per_page = forms.TypedChoiceField(
        required=False,
        label='Items per page',
        choices=[(5, '5'), (10, '10'), (20, '20'), (50, '50')],
        coerce=int,  # Converteste valoarea in int automat
        empty_value=5,  # Valoare default daca nu e selectat nimic
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # --- VALIDARE 1: Lungimea numelui ---
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and len(name) < 2:
            raise ValidationError("The product name must trigger a search of at least 2 characters.")
        return name

    # --- VALIDARE 2: Pret negativ pe min_price ---
    def clean_min_price(self):
        min_price = self.cleaned_data.get('min_price')
        if min_price is not None and min_price < 0:
            raise ValidationError("Price cannot be negative. Please enter a positive value.")
        return min_price

    # --- VALIDARE 3: Pret Minim > Pret Maxim (Validare Cross-field) ---
    def clean(self):
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')

        if min_price is not None and max_price is not None:
            if min_price > max_price:
                raise ValidationError("Minimum price cannot be greater than maximum price.")

        return cleaned_data


def validate_age_18(value):
    """
    Checks if the sender is an adult (over 18 years old).
    """
    today = date.today()
    # Calculate age accounting for month and day
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError("You must be over 18 years old to submit this form.")


def validate_message_content(value):
    """
    Checks:
    1. Message contains between 5 and 100 words.
    2. No word exceeds 15 characters.
    """
    # Define words as alphanumeric sequences
    words = [w for w in re.split(r'[^a-zA-Z0-9]+', value) if w]

    if not (5 <= len(words) <= 100):
        raise ValidationError(f"The message must contain between 5 and 100 words. (Current: {len(words)})")

    for word in words:
        if len(word) > 15:
            raise ValidationError(f"The word '{word}' is too long. Maximum 15 characters allowed per word.")


def validate_no_links(value):
    """
    Checks that there are no links (http:// or https://).
    """
    if "http://" in value.lower() or "https://" in value.lower():
        raise ValidationError("The text cannot contain links (http/https).")


def validate_cnp_content(value):
    """
    Checks CNP validity:
    1. Only digits.
    2. First digit is 1, 2, 5, or 6.
    3. The next 6 digits form a valid date.
    """
    if not value.isdigit():
        raise ValidationError("The CNP must contain digits only.")

    first_digit = int(value[0])
    if first_digit not in [1, 2, 5, 6]:
        raise ValidationError("The CNP must start with the digit 1, 2, 5, or 6.")

    # Date validation from CNP (YYMMDD)
    year_prefix = "19" if first_digit in [1, 2] else "20"
    year_str = year_prefix + value[1:3]
    month_str = value[3:5]
    day_str = value[5:7]

    try:
        datetime(int(year_str), int(month_str), int(day_str))
    except ValueError:
        raise ValidationError("Digits 2-7 of the CNP do not form a valid date.")


def validate_email_domain(value):
    """
    Checks the email domain against a blocklist.
    """
    domain = value.split('@')[-1]
    forbidden_domains = ['guerillamail.com', 'yopmail.com']
    if domain in forbidden_domains:
        raise ValidationError(f"The domain '{domain}' is not allowed (temporary email).")


def validate_text_start_cap_chars(value):
    """
    Checks if text starts with a capital letter and contains only letters, spaces, and hyphens.
    """
    if not value:
        return
    # Regex: Start with Uppercase, followed by letters, spaces, hyphens
    if not re.match(r'^[A-Z][a-zA-Z\s\-]*$', value):
        raise ValidationError(
            "The field must start with a capital letter and contain only letters, spaces, or hyphens.")


def validate_internal_capitalization(value):
    """
    Checks if a capital letter follows a space or hyphen.
    """
    if not value:
        return

    # Split text by space or hyphen
    parts = re.split(r'[\s\-]', value)
    for part in parts:
        # If we have a part (avoiding double spaces) and it doesn't start with uppercase
        if part and not part[0].isupper():
            raise ValidationError(f"The section '{part}' must start with a capital letter (compound names).")


def validate_message_type(value):
    """
    Checks if the message type was selected.
    """
    if value == 'neselectat':
        raise ValidationError("Please select a valid message type.")


class ContactForm(forms.Form):
    TIP_MESAJ_CHOICES = [
        ('neselectat', 'Not Selected'),
        ('reclamatie', 'Complaint'),
        ('intrebare', 'Question'),
        ('review', 'Review'),
        ('cerere', 'Request'),
        ('programare', 'Appointment'),
    ]

    prenume = forms.CharField(
        max_length=10,
        required=False,
        label="First Name",
        validators=[validate_text_start_cap_chars, validate_internal_capitalization]
    )

    nume = forms.CharField(
        max_length=10,
        required=True,
        label="Last Name",
        validators=[validate_text_start_cap_chars, validate_internal_capitalization]
    )

    cnp = forms.CharField(
        min_length=13,
        max_length=13,
        required=False,
        label="Personal Numeric Code (CNP)",
        help_text="Enter exactly 13 characters (digits only).",
        validators=[validate_cnp_content]
    )

    data_nasterii = forms.DateField(
        required=True,
        label="Date of Birth",
        widget=forms.DateInput(attrs={'type': 'date'}),
        validators=[validate_age_18]
    )

    email = forms.EmailField(
        required=True,
        label="E-mail",
        validators=[validate_email_domain]
    )

    confirmare_email = forms.EmailField(
        required=True,
        label="Confirm E-mail"
    )

    tip_mesaj = forms.ChoiceField(
        choices=TIP_MESAJ_CHOICES,
        initial='neselectat',
        label="Message Type",
        validators=[validate_message_type]
    )

    subiect = forms.CharField(
        max_length=100,
        required=True,
        label="Subject",
        validators=[validate_no_links, validate_text_start_cap_chars]
    )

    zile_asteptare = forms.IntegerField(
        min_value=0,
        max_value=30,
        required=True,
        label="Minimum waiting days (For reviews/requests the minimum waiting days must be set from 4 upwards, and for requests/questions from 2 upwards. Maximum is 30.)"
    )

    mesaj = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        required=True,
        label="Message (please sign at the end)",
        validators=[validate_message_content, validate_no_links]
    )

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get('email')
        confirmare_email = cleaned_data.get('confirmare_email')
        mesaj = cleaned_data.get('mesaj')
        nume = cleaned_data.get('nume')
        tip_mesaj = cleaned_data.get('tip_mesaj')
        zile_asteptare = cleaned_data.get('zile_asteptare')
        cnp = cleaned_data.get('cnp')
        data_nasterii = cleaned_data.get('data_nasterii')

        if email and confirmare_email and email != confirmare_email:
            self.add_error('confirmare_email', "Email addresses do not match.")

        if mesaj and nume:
            mesaj_curat = mesaj.rstrip(' .,!?;:')
            cuvinte = mesaj_curat.split()

            if cuvinte:
                ultimul_cuvant = cuvinte[-1]
                # Verificare case-insensitive (Popescu == popescu)
                if ultimul_cuvant.lower() != nume.lower():
                    self.add_error('mesaj', f"The message must be signed with your Last Name ({nume}) at the end.")
            else:
                self.add_error('mesaj', "The message is empty or contains only punctuation.")

        # 3. Validare: Zile așteptare vs Tip Mesaj
        if zile_asteptare is not None and tip_mesaj and tip_mesaj != 'neselectat':
            if tip_mesaj in ['review', 'cerere']:
                if zile_asteptare < 4:
                    self.add_error('zile_asteptare',
                                   f"For '{tip_mesaj}', the minimum waiting time must be at least 4 days.")

            elif tip_mesaj in ['intrebare', 'cerere']:
                # Nota: 'cerere' apare in ambele cerinte (4 si 2). Deoarece 4 > 2, regula de mai sus (4) primeaza.
                # Aici tratam specific 'intrebare'.
                if tip_mesaj == 'intrebare' and zile_asteptare < 2:
                    self.add_error('zile_asteptare', "For questions, the minimum waiting time must be at least 2 days.")

        # 4. Validare: CNP corespunde cu Data Nasterii
        if cnp and data_nasterii:
            # Verificam dacă CNP-ul are lungimea si structura de baza corecta (cifre)
            if len(cnp) == 13 and cnp.isdigit():
                s = int(cnp[0])
                aa = int(cnp[1:3])
                ll = int(cnp[3:5])
                zz = int(cnp[5:7])

                # Determinam secolul
                prefix_an = 0
                if s in [1, 2]:
                    prefix_an = 1900
                elif s in [5, 6]:
                    prefix_an = 2000

                if prefix_an > 0:
                    an_cnp = prefix_an + aa
                    try:
                        data_din_cnp = date(an_cnp, ll, zz)

                        if data_din_cnp != data_nasterii:
                            self.add_error('cnp', "The CNP does not match the provided Date of Birth.")
                            self.add_error('data_nasterii', "The Date of Birth does not match the provided CNP.")
                    except ValueError:
                        self.add_error('cnp', "The date encoded in the CNP is invalid.")

        return cleaned_data

def validate_starts_with_upper(value):
    """Checks if the text starts with an uppercase letter."""
    if not value:
        return
    if not value[0].isupper():
        raise ValidationError(
            "The text must start with a capital letter (custom error).",
            code='invalid_capital'
        )

def validate_no_numbers(value):
    """Checks that the text does not contain digits."""
    if any(char.isdigit() for char in value):
        raise ValidationError(
            "This field cannot contain numbers (custom error).",
            code='invalid_digits'
        )


class ProductForm(forms.ModelForm):
    acquisition_price = forms.FloatField(
        label="Acquisition Price ($)",
        min_value=0,
        help_text="Enter the base price paid to the artist/supplier.",
        error_messages={'required': "Acquisition price is required for calculation."}
    )

    markup_percentage = forms.IntegerField(
        label="Markup Percentage (%)",
        min_value=0,
        max_value=500,
        help_text="Percentage added to the base price to determine final selling price.",
        error_messages={'required': "Markup percentage is mandatory."}
    )

    # --- Overriding Model Fields to add Validators ---
    name = forms.CharField(
        label="Artwork Title",
        validators=[validate_starts_with_upper],  # External validator 1
        error_messages={'required': "The artwork title is required."}
    )

    author = forms.CharField(
        label="Artist Name",
        # Using two external validators here (ordering matters)
        validators=[validate_starts_with_upper, validate_no_numbers],
        error_messages={'required': "The artist's name is required."}
    )

    class Meta:
        model = Product
        # We EXCLUDE 'price' because it will be calculated
        fields = ['name', 'category', 'type', 'author', 'description', 'stock', 'image']

        # Custom Labels (at least 2 fields)
        labels = {
            'stock': 'Inventory Count',
            'image': 'Product Image',
            'type': 'Art Medium',
            'description': 'Detailed Description'
        }

        # Help Texts (at least 2 fields)
        help_texts = {
            'description': 'Please provide a comprehensive description of the artwork.',
            'image': 'Upload a high-resolution image (JPG/PNG).',
        }

        # Custom Widgets (Optional, for better UI)
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    # --- Field Validation 1: STOCK ---
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise ValidationError("Inventory count cannot be negative.")
        return stock

    # --- Field Validation 2: DESCRIPTION ---
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 20:
            raise ValidationError("The description is too short. Please use at least 20 characters.")
        return description

    # --- Field Validation 3: IMAGE ---
    def clean_image(self):
        image = self.cleaned_data.get('image')
        # If the user selected a type other than Digital, an image is mandatory
        # Note: We can access other fields in clean_FIELD, but usually clean() is better for cross-field.
        # Here we just check file size if an image exists.
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError("The image file is too large (Max 5MB).")
        return image

    # --- General Validation (Cross-field) ---
    def clean(self):
        cleaned_data = super().clean()

        prod_type = cleaned_data.get('type')
        stock = cleaned_data.get('stock')
        image = cleaned_data.get('image')

        # Cross-validation 1: Physical products must have stock
        physical_types = ['Poster', 'Painting', 'Sculpture']
        if prod_type in physical_types:
            if stock is not None and stock == 0:
                self.add_error('stock', f"For {prod_type}, you must have at least 1 item in stock.")

        # Cross-validation 2: Paintings must have an image uploaded
        if prod_type == 'Painting' and not image:
            self.add_error('image', "An image is mandatory for Paintings.")

        return cleaned_data

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        # Lista campurilor care vor aparea în formular
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'phone',
            'country',
            'county',
            'city',
            'address'
        ]

    # --- VALIDARE 1: Telefon ---
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Verificăm dacă utilizatorul a introdus ceva (fiind opțional în model, validam doar daca e completat)
        if phone:
            if not phone.isdigit():
                raise forms.ValidationError("Numarul de telefon trebuie să contina doar cifre.")
            if len(phone) < 10:
                raise forms.ValidationError("Numarul de telefon trebuie să aiba minim 10 cifre.")
        return phone

    # --- VALIDARE 2: Oras ---
    def clean_city(self):
        city = self.cleaned_data.get('city')
        if city:
            if any(char.isdigit() for char in city):
                raise forms.ValidationError("Numele orașului nu poate conține cifre.")
        return city

    # --- VALIDARE 3: Adresa ---
    def clean_address(self):
        address = self.cleaned_data.get('address')
        if address:
            if len(address) < 10:
                raise forms.ValidationError("Te rugam să introduci o adresa mai detaliata (minim 10 caractere).")
        return address

    # --- VALIDARE 4: verifica daca user-ul incearca sa-si faca cont cu numele admin
    def clean_username(self):
        username = self.cleaned_data.get('username')

        user_email = self.data.get('email', 'N/A')

        if username and username.lower() == 'admin':
            email_subject = "Suspicious user registration"
            email_body = f"Registration attempt email: {user_email}"

            send_custom_admin_email(email_subject, email_body)

            logger.critical(f"User with email {user_email} tried to create an account with the name admin.")

            # Reject registration
            raise ValidationError("This username is reserved.")

        return username

class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Remember me"
    )

class DiscountForm(forms.ModelForm):
    days_active = forms.IntegerField(
        min_value=1,
        initial=7,
        label="Discount duration",
        help_text="For how many days will the discount be active?"
    )

    class Meta:
        model = Discount
        fields = ['name', 'email_subject', 'message_template', 'days_active', 'categories', 'percent']
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'].initial = Category.objects.all()