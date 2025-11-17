from django.contrib import admin

from .models import Product, Category, Subcategory, Exhibition, Award, Discount, Image


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'category', 'price')  # afișează câmpurile în lista de obiecte
    list_filter = ('price', 'category')  # adaugă filtre laterale
    search_fields = ('name', 'author')  # permite căutarea după anumite câmpuri
    empty_value_display = 'null' # se va afișa cuvântul 'null; pentru campurile fără valori
    ordering = ['name', '-author'] #crescator pentru titlu; dar autorii aceleiași cărți în ordine descrescătoare
    list_per_page = 5 # numarul de înregistrări afișate pe pagină

    fieldsets = (
        ('Main Information', {
            'fields': ('name', 'category', 'author', 'price', 'subcategory'),
            'description': 'Mandatory fields for product creation'
        }),
        ('Additional Details', {
            'fields': ('description', 'image'   ),
            'classes': ('collapse',),  # face secțiunea colapsabilă
            'description': 'Optional fields, can be completed later'
        }),
    )

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Image)
admin.site.register(Discount)
admin.site.register(Award)
admin.site.register(Exhibition)

admin.site.site_header = "Art Nouveau Admin Portal"
admin.site.site_title = "Art Nouveau Admin Portal"
admin.site.index_title = "Welcome! Please be careful, chief."