from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Product, Category, Exhibition, Award, Discount, User, UserProductView

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'category', 'price')  # afișează câmpurile în lista de obiecte
    list_filter = ('price', 'category')  # adaugă filtre laterale
    search_fields = ('name', 'author')  # permite căutarea după anumite câmpuri
    empty_value_display = 'null' # se va afișa cuvântul 'null; pentru campurile fără valori
    ordering = ['name', '-author'] #crescator pentru titlu; dar autorii aceleiași cărți în ordine descrescătoare
    list_per_page = 10 # numarul de înregistrări afișate pe pagină

    fieldsets = (
        ('Main Information', {
            'fields': ('name', 'category', 'author', 'price', 'type', 'stock'),
            'description': 'Mandatory fields for product creation'
        }),
        ('Additional Details', {
            'fields': ('description', 'image',),
            'classes': ('collapse',),  # face secțiunea colapsabilă
            'description': 'Optional fields, can be completed later'
        }),
    )

class UserAdmin(BaseUserAdmin):
    # Add the new fields to the fieldsets so they appear in the admin form
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'country', 'county', 'city', 'address', 'email_confirmed')}),
        ('User Status', {'fields': ('blocked',)}),
    )
    # Allow these fields to be filled when creating a user
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('phone', 'country', 'county', 'city', 'address')}),
    )

    def get_readonly_fields(self, request, obj=None):
        """
        Această metodă decide ce câmpuri NU pot fi editate.
        Dacă userul este 'Moderator', facem aproape totul read-only,
        cu excepția numelui, prenumelui, email-ului și statusului de blocare.
        """
        # Verificăm dacă userul care face cererea este în grupul 'Moderatori' și NU este superuser
        if request.user.groups.filter(name='Moderators').exists() and not request.user.is_superuser:
            # Lista câmpurilor pe care Moderatorul ARE voie să le modifice
            editable_fields = ['first_name', 'last_name', 'email', 'blocked']

            # Obținem lista tuturor câmpurilor modelului
            all_fields = [f.name for f in self.model._meta.fields]

            # Returnăm lista câmpurilor care NU sunt în lista celor editabile (adică devin Read-Only)
            # De asemenea, adăugăm 'password' și 'username' manual pentru siguranță
            readonly = [f for f in all_fields if f not in editable_fields]
            readonly.extend(['password', 'username', 'last_login', 'date_joined', 'groups', 'user_permissions'])

            return readonly

        # Pentru superuseri sau alți admini, comportamentul este cel standard
        return super().get_readonly_fields(request, obj)

class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'percent', 'creation_date', 'expiration_date')
    list_filter = ('creation_date', 'expiration_date')
    search_fields = ('name',)

admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Award)
admin.site.register(Exhibition)
admin.site.register(UserProductView)

admin.site.site_header = "Art Nouveau Admin Portal"
admin.site.site_title = "Art Nouveau Admin Portal"
admin.site.index_title = "Welcome! Please be careful, chief."