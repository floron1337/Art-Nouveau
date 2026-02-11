import secrets
from datetime import datetime, date, timedelta
import json
import os
import re
import time
import logging
from urllib.parse import urlparse

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import EmailMultiAlternatives, send_mass_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.core.cache import cache

from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.datastructures import OrderedSet
from django.utils.html import strip_tags
from django.views import View
from django.views.generic import TemplateView

from Art_Nouveau.constants import MAX_LAST_PRODUCT_VIEW_COUNT, K_MIN_VIEWS, MIN_SUSPICIOUS_LOGIN_TRIGGER, \
    LOW_STOCK_THRESHOLD
from Art_Nouveau.forms import ProductFilterForm, ContactForm, ProductForm, RegisterForm, LoginForm, DiscountForm
from Art_Nouveau.models import Product, Category, UserProductView, User

from Art_Nouveau.utils import get_ip, send_custom_admin_email

LOG_ENTRIES = []
logger = logging.getLogger('django')

class AccessLogEntry:
    _id_counter = 0

    def __init__(self, ip_client=None, url=None, data=None):
        self.id = AccessLogEntry._id_counter
        AccessLogEntry._id_counter += 1
        self.ip_client = ip_client
        self.url = url
        self._data = data if data else datetime.now()

    def __str__(self):
        return f"AccessLogEntry(id={self.id}, ip_client={self.ip_client}, url={self.url}, data={self._data})"

    def __repr__(self):
        return self.__str__()

    def lista_parametri(self):
        return [
            ('id', self.id),
            ('ip_client', self.ip_client),
            ('url', self.url),
            ('data', self._data)
        ]

    def url_complet(self):
        return self.url

    def data(self, format_str):
        return self._data.strftime(format_str)

    def pagina(self):
        if not self.url:
            return None

        parsed = urlparse(self.url)
        return parsed.path or '/'

class BaseLoggableView(View):
    def dispatch(self, request, *args, **kwargs):
        LOG_ENTRIES.append(AccessLogEntry(
            get_ip(request),
            request.build_absolute_uri(),
            datetime.now()
        ))
        return super().dispatch(request, *args, **kwargs)

class IndexView(BaseLoggableView):
    def get(self, request):
        return render(request, "Art_Nouveau/index.html")

class AboutView(BaseLoggableView):
    def get(self, request):
        return render(request, "Art_Nouveau/about.html")

class InfoView(BaseLoggableView):
    def afis_data(self, tip=None):
        zile = ['Luni', 'Marți', 'Miercuri', 'Joi', 'Vineri', 'Sâmbătă', 'Duminică']
        luni = ['Ianuarie', 'Februarie', 'Martie', 'Aprilie', 'Mai', 'Iunie',
                'Iulie', 'August', 'Septembrie', 'Octombrie', 'Noiembrie', 'Decembrie']
        acum = datetime.now()
        zi_sapt = zile[acum.weekday()]
        zi = acum.day
        luna = luni[acum.month - 1]
        an = acum.year
        ora = acum.strftime('%H:%M:%S')

        if tip == 'zi':
            continut = f"{zi_sapt}, {zi} {luna} {an}"
        elif tip == 'timp':
            continut = ora
        else:
            continut = f"{zi_sapt}, {zi} {luna} {an} {ora}"

        return f'''
        <section>
            <h2>Data și ora</h2>
            <p>{continut}</p>
        </section>
        '''

    def get(self, request):
        if not (request.user.groups.filter(name='Administrators').exists() or request.user.is_superuser):
            return Custom403View.as_view()(
                request,
                exception_repr="You need to be an administrator to access this page"
            )

        messages.debug(request, f"Debug: Info Page accessed by IP {get_ip(request)} at {datetime.now()}")

        data_param = request.GET.get("data")
        sectiune_data = self.afis_data(data_param)

        parametri = request.GET
        numar_parametri = len(parametri)
        nume_parametri = ", ".join(parametri.keys()) if numar_parametri > 0 else "Niciun parametru"

        sectiune_parametri = f"""
                <section>
                    <h2>Parametri</h2>
                    <p>Numar parametri: {numar_parametri}</p>
                    <p>Nume parametri:{nume_parametri}</p>
                </section>
            """

        tabel_param = request.GET.get("tabel")
        sectiune_tabel = ""

        if tabel_param:
            if tabel_param == "tot":
                campuri = [attr for attr in vars(LOG_ENTRIES[0]).keys()] if LOG_ENTRIES else []
            else:
                campuri = tabel_param.split(",")

            header = "".join(f"<th>{c}</th>" for c in campuri)

            randuri = ""
            for acc in LOG_ENTRIES:
                randuri += "<tr>" + "".join(f"<td>{getattr(acc, c, '-')}</td>" for c in campuri) + "</tr>"

            sectiune_tabel = f"""
                    <section>
                        <h2>Accesari</h2>
                        <table border="1" cellpadding="5" cellspacing="0" style="border-collapse:collapse;">
                            <tr>{header}</tr>
                            {randuri}
                        </table>
                    </section>
                    """

        sectiune_stats = "<h2>Statistici</h2>"

        if len(LOG_ENTRIES) > 0:
            cnt_dict = {}

            for log in LOG_ENTRIES:
                pagina = log.pagina()
                if pagina not in cnt_dict:
                    cnt_dict[pagina] = 1
                else:
                    cnt_dict[pagina] += 1

            maxim = max(cnt_dict.items(), key=lambda x: x[1])
            minim = min(cnt_dict.items(), key=lambda x: x[1])

            sectiune_stats += f"<p>Cea mai accesata pagina: {maxim[0]} ({maxim[1]} accesari)</p>"
            sectiune_stats += f"<p>Cea mai putin accesata pagina: {minim[0]} ({minim[1]} accesari)</p>"
        else:
            sectiune_stats = "<p>Nu exista inregistrari in log.</p>"

        logger.debug(f'Accessed Info page with params: {nume_parametri}')

        return HttpResponse(f'''
                <head>
                    <title>Info</title>
                </head>
                <body>
                    <h1>Informatii despre server</h1>
                    {sectiune_data}
                    {sectiune_parametri}
                    {sectiune_tabel}
                    {sectiune_stats}
                </body>
            ''')

class LogsView(BaseLoggableView):
    def get(self, request):
        if not (request.user.groups.filter(name='Administrators').exists() or request.user.is_superuser):
            return Custom403View.as_view()(
                request,
                exception_repr="You need to be an administrator to access this page"
            )

        ultimele = request.GET.get("ultimele")
        accesari = request.GET.get("accesari")
        dubluri = request.GET.get("dubluri", "false").lower() == "true"
        iduri = request.GET.getlist("iduri")
        err = ''
        if ultimele is not None:
            try:
                ultimele = int(ultimele)
                if ultimele <= 0:
                    raise ValueError
            except (TypeError, ValueError):
                err = '<p style="color:red;">Parametru invalid. Se vor afisa toate inregistrarile.</p>'
                ultimele = len(LOG_ENTRIES)

            if ultimele > len(LOG_ENTRIES):
                err = '<p style="color:red;">Parametru prea mare. Se vor afisa toate inregistrarile.</p>'
                ultimele = len(LOG_ENTRIES)
        else:
            ultimele = len(LOG_ENTRIES) + 1

        html = '<head><title>Logs</title></head><body><h1>Log accesari</h1><table border="1" cellpadding="5" cellspacing="0" style="border-collapse:collapse;">'
        html += '<tr><th>ID</th><th>IP Client</th><th>URL</th><th>Data</th><th>Pagina</th></tr>'

        id_list = []

        if iduri:
            for l in iduri:
                id_list.extend(l.split(','))

            id_list = [int(i) for i in id_list if i.isdigit() and int(i) < len(LOG_ENTRIES)]

            if not dubluri:
                id_list = OrderedSet(id_list)
        else:
            id_list = [x for x in range(len(LOG_ENTRIES))]

        for i in id_list:
            acc = LOG_ENTRIES[i]
            html += f'<tr><td>{acc.id}</td><td>{acc.ip_client}</td><td>{acc.url_complet()}</td><td>{acc.data("%d.%m.%Y %H:%M:%S")}</td><td>{acc.pagina()}</td></tr>'

        html += '</table>'

        html += err

        if accesari == "nr":
            html += f"<p>Numar total de accesari: {len(LOG_ENTRIES)}</p>"
        elif accesari == "detalii":
            html += '<ul style="list-style-type:disc; color:#444; font-size:16px; line-height:1.6;">'
            for i in id_list:
                acc = LOG_ENTRIES[i]
                html += f"<li>{acc.data('%d.%m.%Y %H:%M:%S')}</li>"
            html += '</ul>'
        html += '</body>'

        logger.debug(f'Accessed logs page with {len(LOG_ENTRIES)} entries')

        return HttpResponse(html)

class ProductsView(BaseLoggableView):
    default_items_per_page = 5

    def get(self, request, category_slug=None):
        product_list_query = Product.objects.all().select_related('category')

        all_categories = Category.objects.all()

        current_category = None
        category_error_msg = None
        repagination_warning = None  # Variabila noua pentru mesajul cerut

        if category_slug:
            try:
                current_category = get_object_or_404(Category, slug=category_slug)
                product_list_query = product_list_query.filter(category=current_category)
            except Exception:
                current_category = None
                category_error_msg = "Category not found. Showing all products."
                messages.error(request, "Category not found. Showing all products.")

        form = ProductFilterForm(request.GET)

        if current_category:
            if 'category' in form.fields:
                del form.fields['category']

        current_items_per_page = self.default_items_per_page

        if form.is_valid():
            data = form.cleaned_data

            if data.get('name'):
                product_list_query = product_list_query.filter(name__icontains=data['name'])

            if data.get('description'):
                # Search in description OR short_description
                from django.db.models import Q
                product_list_query = product_list_query.filter(
                    Q(description__icontains=data['description']) |
                    Q(short_description__icontains=data['description'])
                )

            if data.get('min_price') is not None:
                product_list_query = product_list_query.filter(price__gte=data['min_price'])

            if data.get('max_price') is not None:
                product_list_query = product_list_query.filter(price__lte=data['max_price'])

            if data.get('items_per_page'):
                current_items_per_page = data['items_per_page']

            # If not on a category page (slug) and a category is selected in the form
            if not current_category and data.get('category'):
                product_list_query = product_list_query.filter(category=data['category'])

        sort_param = request.GET.get('sort', '')

        if sort_param == 'a':
            product_list_query = product_list_query.order_by('price')
        elif sort_param == 'd':
            product_list_query = product_list_query.order_by('-price')
        else:
            product_list_query = product_list_query.order_by('-id')

        if settings.DEBUG:
            count = product_list_query.count()
            messages.debug(request, f"Query returned {count} products.")

        paginator = Paginator(product_list_query, current_items_per_page)
        page_number = request.GET.get('page', 1)
        try:
            current_page_num = int(page_number)
        except ValueError:
            current_page_num = 1

        if current_page_num > 1:
            repagination_warning = (
                "Caution: Changing pagination settings while navigating may cause "
                "you to skip products or view previously seen items."
            )
            messages.warning(request,"Caution: Changing filters while on a deeper page may cause you to miss items. Consider resetting to page 1.")

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
            # Daca pagina nu e int, nu avem warning de repaginare
            repagination_warning = None
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
            repagination_warning = None

        # Construim parametrii URL
        params = request.GET.copy()
        if 'page' in params:
            del params['page']
        search_params = params.urlencode()

        context = {
            'products': page_obj.object_list,
            'page_obj': page_obj,
            'paginator': paginator,
            'menu_categories': all_categories,
            'current_category': current_category,
            'current_sort': sort_param,
            'category_error_msg': category_error_msg,
            'filter_form': form,
            'search_params': search_params,
            # Trimitem mesajul nou in template
            'repagination_warning': repagination_warning
        }

        return render(request, 'Art_Nouveau/products.html', context)

class ProductView(BaseLoggableView):
    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)

        if request.user.is_authenticated:
            # daca produsul exista deja, atunci il stergem din istoric pentru a-l readauga
            UserProductView.objects.filter(user=request.user, product=product).delete()

            # adauga noua vizualizare
            UserProductView.objects.create(user=request.user, product=product)

            user_views = UserProductView.objects.filter(user=request.user).order_by('-view_date')
            if user_views.count() > MAX_LAST_PRODUCT_VIEW_COUNT:
                user_views.last().delete()
                messages.info(request,f"Welcome back, {request.user.username}. You are viewing details for '{product.name}'.")

        if product.stock <= LOW_STOCK_THRESHOLD:
            logger.warning(f"Low stock for product {product.name} (ID: {product.pk}). Remaining: {product.stock}")
            messages.warning(request, f"Hurry up! Only {product.stock} items left in stock for '{product.name}'.")

        return render(request, 'Art_Nouveau/product.html', {
            'product': product
        })


class ContactView(BaseLoggableView):
    def get(self, request):
        form = ContactForm()
        return render(request, 'Art_Nouveau/contact.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data.copy()

            # Calcul Varsta (Ani si Luni)
            data_nasterii = data.pop('data_nasterii')
            today = date.today()

            ani = today.year - data_nasterii.year
            luni = today.month - data_nasterii.month

            if today.day < data_nasterii.day:
                luni -= 1

            if luni < 0:
                ani -= 1
                luni += 12

            data['varsta'] = f"{ani} ani, {luni} luni"

            # Curatare Mesaj (Spatii si Majuscule)
            raw_msg = data['mesaj']

            # Transforma linii noi si spatii multiple intr-un singur spatiu
            clean_msg = re.sub(r'\s+', ' ', raw_msg).strip()

            # Transforma litera de după terminatori (.?!...) în majuscula
            def capitalize_match(match):
                return f"{match.group(1)}{match.group(2)}{match.group(3).upper()}"

            clean_msg = re.sub(r'([\.\?!]|\.\.\.)(\s*)([a-z])', capitalize_match, clean_msg)

            # Prima litera din mesaj mare
            if clean_msg:
                clean_msg = clean_msg[0].upper() + clean_msg[1:]

            data['mesaj'] = clean_msg

            # 3. Determinare Urgenta
            tip = data.get('tip_mesaj')
            zile = data.get('zile_asteptare')
            is_urgent = False

            minim_zile = None
            if tip in ['review', 'cerere']:
                minim_zile = 4
            elif tip == 'intrebare':
                minim_zile = 2

            if minim_zile is not None and zile == minim_zile:
                is_urgent = True

            data['urgent'] = is_urgent

            # Eliminare campuri inutile
            if 'confirmare_email' in data:
                del data['confirmare_email']

            # Adaugare Metadate (IP, Timestamp)

            data['ip_address'] = get_ip(request)
            acum = datetime.now()
            data['time_arrival'] = acum.strftime("%Y-%m-%d %H:%M:%S")

            # SALVARE IN FISIER

            app_path = os.path.dirname(__file__)
            mesaje_folder = os.path.join(app_path, 'messages')

            if not os.path.exists(mesaje_folder):
                os.makedirs(mesaje_folder)

            timestamp_secunde = int(time.time())
            nume_fisier = f"msg_{timestamp_secunde}"

            if is_urgent:
                nume_fisier += "_urgent"

            nume_fisier += ".json"
            full_path = os.path.join(mesaje_folder, nume_fisier)

            try:
                with open(full_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False, default=str)

                messages.success(request, f"Thank you, {data['nume']}! Your message has been sent successfully.")

            except Exception as e:
                logger.critical(f"We are unable to save messages to the server due to exception {e}. Fallback to sending mail to admins.")
                messages.error(request, f"Error saving message: {e}. Don't worry, a copy of your message has been sent to support.")
                # Trimitem un mail si administratorilor daca nu s-a reusit salvarea mesajelor
                send_custom_admin_email("Error saving message", str(f"""
                    {data}
                    
                    Exception: {e}
                """))

            form = ContactForm()

        return render(request, 'Art_Nouveau/contact.html', {'form': form})


class AddProductView(BaseLoggableView):
    def get(self, request):
        """
        Handles the display of the empty form.
        """

        # Verificăm permisiunea
        if not request.user.has_perm('Art_Nouveau.add_product'):
            # Apelăm direct view-ul tău custom de 403
            # Îi pasăm mesajul specific prin 'exception_repr', așa cum așteaptă clasa ta
            return Custom403View.as_view()(
                request,
                exception_repr="You are not allowed to add products to Art Nouveau"
            )

        form = ProductForm()
        return render(request, 'Art_Nouveau/add_product.html', {'form': form})

    def post(self, request):
        """
        Handles the form submission, validation, calculation, and saving.
        """
        if not request.user.has_perm('Art_Nouveau.add_product'):
            # Apelăm direct view-ul tău custom de 403
            # Îi pasăm mesajul specific prin 'exception_repr', așa cum așteaptă clasa ta
            return Custom403View.as_view()(
                request,
                exception_repr="You are not allowed to add products to Art Nouveau"
            )

        # We must include request.FILES because the model has an ImageField
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            # 1. Create the instance but don't save to DB yet (commit=False)
            product = form.save(commit=False)

            # 2. Extract data from the additional fields
            base_price = form.cleaned_data['acquisition_price']
            markup = form.cleaned_data['markup_percentage']

            # 3. Calculate the missing 'price' column
            # Formula: Base + (Base * Markup / 100)
            calculated_price = base_price + (base_price * markup / 100)
            product.price = round(calculated_price, 2)

            # 4. Save to database
            product.save()

            messages.success(
                request,
                f"Product '{product.name}' added successfully! Final Price: ${product.price}"
            )
            return redirect('products')  # Ensure this matches your URL name for the list

        else:
            # If the form is invalid, re-render the page with errors
            messages.error(request, "Please correct the errors below.")
            logger.error(f"Error creating product.")

            return render(request, 'Art_Nouveau/add_product.html', {'form': form})

class RegisterUserView(BaseLoggableView):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'Art_Nouveau/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # Generam string-ul aleator pentru cod
            user.code = secrets.token_hex(16)
            user.email_confirmed = False

            # Salvam acum utilizatorul in baza de date
            user.save()

            # 4. Construim link-ul de confirmare
            # build_absolute_uri('/') returneaza domeniul curent (ex: http://localhost:8000/)
            domain = request.build_absolute_uri('/')[:-1]
            link_confirmare = f"{domain}/confirm_mail/{user.code}/"

            context = {
                'nume': user.last_name,
                'prenume': user.first_name,
                'username': user.username,
                'link_confirmare': link_confirmare,
            }

            html_content = render_to_string('Art_Nouveau/confirmation_email.html', context)
            text_content = strip_tags(html_content)  # Varianta text simplu (fallback)

            try:
                email = EmailMultiAlternatives(
                    subject='Art Nouveau E-Mail Confirmation',
                    body=text_content,
                    from_email='florinvenis@gmail.com',
                    to=[user.email]
                )
                email.attach_alternative(html_content, "text/html")
                email.send()

                messages.success(request,
                                 f'User {user.username} has been created! Please check your email for confirmation.')
            except Exception as e:
                messages.warning(request, f'Account created, but no confirmation e-mail has been sent. Exception: {e}')
                logger.error(f"User {user.username} ID: {user.pk} account created, but no confirmation e-mail has been sent due to {e}")

            logger.info(f"User created successfully: {user.username}")
            return redirect('login')

        return render(request, 'Art_Nouveau/register.html', {'form': form})

class LoginUserView(LoginView, BaseLoggableView):
    form_class = LoginForm
    template_name = 'Art_Nouveau/login.html'

    #redirect_authenticated_user = True

    def form_valid(self, form):
        """
        Aceasta metoda ruleaza DOAR daca userul si parola sunt corecte.
        Aici verificam regulile de business (email confirmat, remember me).
        """
        user = form.get_user()

        if user.blocked:
            messages.error(self.request, "Your account has been blocked by a moderator!")
            # Returnam pagina de login cu eroarea, fara a loga utilizatorul
            return self.render_to_response(self.get_context_data(form=form))

        # 2. Verificam dacă are emailul confirmat
        if not user.email_confirmed and not user.is_superuser:
            messages.error(self.request, "You need to confirm your e-mail address before logging in!")
            # Returnam pagina de login cu eroarea, fara a loga utilizatorul
            return self.render_to_response(self.get_context_data(form=form))

        # 3. Dacă e confirmat, continuam logica de "Remember me"
        remember_me = form.cleaned_data.get('remember_me')
        if remember_me:
            self.request.session.set_expiry(86400)  # 1 zi
            messages.info(self.request, "You checked 'Remember me'. You will stay logged in for 24 hours.")
        else:
            self.request.session.set_expiry(0)  # La închiderea browserului

        logger.info(f"User logged in successfully: {user.username}")

        # 4. Apelăm super().form_valid(form) care face logarea efectivă (login(request, user))
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Aceasta metoda ruleaza cand userul sau parola sunt GRESITE.
        Aici implementam logica de securitate.
        """

        # 1. Identificam IP-ul si Username-ul incercat
        user_ip = get_ip(self.request)

        # Luam username-ul din datele brute (POST), deoarece form.cleaned_data poate nu exista daca validarea a esuat grav
        username_attempted = self.request.POST.get('username', 'unknown')

        # 2. Gestionare Cache pentru contorizare
        cache_key = f'login_fail_{user_ip}'
        attempts = cache.get(cache_key, 0)
        attempts += 1

        # Setam noua valoare cu timeout de 2 minute (120 secunde)
        cache.set(cache_key, attempts, timeout=120)

        # 3. Verificam limita
        if attempts >= MIN_SUSPICIOUS_LOGIN_TRIGGER:
            email_subject = "Suspicious Login"
            email_body = (
                f"Username attempted: {username_attempted}\n"
                f"IP Address: {user_ip}\n"
                f"Failed attempts in last 2 minutes: {attempts}"
            )

            # Trimitem emailul folosind functia helper creata anterior
            send_custom_admin_email(email_subject, email_body)

            # Optional: Stergem cheia pentru a nu trimite mail la fiecare click ulterior (spam protection)
            # sau o lasam sa expire singura. Aici aleg sa o sterg pentru a reseta ciclul.
            cache.delete(cache_key)

            logger.warning(f"Failed {attempts} login attempts for user: {username_attempted} from IP: {user_ip}")

        # 4. Returnam comportamentul standard (afisarea erorii in pagina)
        return super().form_invalid(form)

class ProfileView(LoginRequiredMixin, BaseLoggableView):
    def get(self, request):
        is_admin = request.user.groups.filter(name='Administrators').exists() or request.user.is_superuser

        if is_admin:
            messages.info(request, "You have Administrator privileges.")

        context = {
            'is_admin': is_admin
        }

        return render(request, 'Art_Nouveau/profile.html', context)

class ConfirmEmailView(BaseLoggableView):
    def get(self, request, code):
        User = get_user_model()
        user = get_object_or_404(User, code=code)

        if user.email_confirmed:
            messages.info(request, 'Email already confirmed.')
        else:
            user.email_confirmed = True
            user.save()
            messages.success(request, 'Email successfully confirmed. You can login now!')

        return render(request, 'Art_Nouveau/email_confirmation_success.html')

class CreateDiscountView(BaseLoggableView):
    template_name = 'Art_Nouveau/create_discount.html'

    def get(self, request):
        form = DiscountForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = DiscountForm(request.POST)

        if form.is_valid():
            promo = form.save(commit=False)

            # 1. Calculăm data expirării pe baza zilelor introduse
            days = form.cleaned_data['days_active']
            promo.expiration_date = timezone.now() + timedelta(days=days)
            promo.save()

            # Salvăm relația ManyToMany (categoriile) după ce obiectul are ID
            form.save_m2m()

            # --- LOGICA DE TRIMITERE EMAIL ---
            selected_categories = promo.categories.all()
            chosen_template = promo.message_template

            # Lista de mesaje pentru send_mass_mail
            # Format: (subiect, mesaj, expeditor, [lista_destinatari])
            mass_messages = []

            sender_email = 'office@artnouveau.com'

            for category in selected_categories:
                # 2. Selectăm userii cu minim K vizualizări în această categorie
                # Folosim filtrare pe relația cu UserProductView -> Product -> Category
                eligible_users = User.objects.filter(
                    userproductview__product__category=category
                ).annotate(
                    view_count=Count('userproductview')
                ).filter(
                    view_count__gte=K_MIN_VIEWS
                ).distinct()

                # Extragem adresele de email ale userilor eligibili
                recipient_list = [u.email for u in eligible_users if u.email]

                if not recipient_list:
                    continue  # Sărim peste categorie dacă nu are useri interesați

                # 3. Construim mesajul personalizat pentru acea categorie
                context = {
                    'subject': promo.email_subject,
                    'promotion_name': promo.name,
                    'category_name': category.name,  # Variabilă specifică categoriei curente
                    'discount': promo.percent,
                    'expiration_date': promo.expiration_date,
                }

                message_body = render_to_string(chosen_template, context)

                # Adăugăm tuplul în listă
                mass_messages.append((
                    promo.email_subject,
                    message_body,
                    sender_email,
                    recipient_list
                ))

            # 4. Trimitem totul printr-o singură comandă
            if mass_messages:
                send_mass_mail(tuple(mass_messages), fail_silently=False)
                messages.success(request,
                                 f"Promotion has been created and {len(mass_messages)} groups of emails have been sent!")
            else:
                messages.warning(request,
                                 f"Promotion created, but no eligible users were found to send emails to (K >= {K_MIN_VIEWS}).")

            return redirect('products')

        return render(request, self.template_name, {'form': form})


class Custom403View(BaseLoggableView, TemplateView):
    template_name = '403.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 1. Session Counter Logic
        # We keep the session key internal, but you can rename it if you want (e.g., 'error_403_count')
        current_count = self.request.session.get('cnt_403', 0)
        current_count += 1
        self.request.session['cnt_403'] = current_count

        # 2. Retrieve exception message if passed
        exception_msg = kwargs.get('exception_repr', None)

        # 3. Context variables translated to English
        context.update({
            'header_title': '',  # Left empty to trigger the default filter in template
            'custom_message': str(
                exception_msg) if exception_msg else "You do not have permission to access this resource.",
            'error_count': current_count,
            'max_errors': getattr(settings, 'N_MAX_403', 5),
        })

        return context

    def get(self, request, *args, **kwargs):
        # Suprascriem metoda GET doar pentru a forta statusul 403.
        # Logica de logging a rulat deja în dispatch-ul din BaseLoggableView.
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=403)

# Wrapper-ul pentru URL handler
def custom_403_handler(request, exception=None):
    """
    Wrapper necesar pentru handler403 din urls.py
    El se asteapta sa primeasca o functie pentru a putea executa toate
    functionalitatile cerute (contorizare sesiune, mesaj personalizat, logare ip etc)
    """
    return Custom403View.as_view()(request, exception_repr=exception)