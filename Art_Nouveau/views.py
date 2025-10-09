import datetime
from urllib.parse import urlparse

from django.http import HttpResponse

def index(request):
    return HttpResponse('''
    <head>
        <title>Art Nouveau</title>
    </head>
    <body>
        <h1>Art Nouveau</h1>
        <p>
        Proiectul presupune dezvoltarea unei aplicații web
         care oferă utilizatorilor posibilitatea de a vizualiza,
          achiziționa și crea opere de artă printr-un magazin online. 
          Imaginile vor putea fi clasificate în funcție de stilul 
          artistic din care fac parte, iar fiecare lucrare va include 
          informații despre autor, preț și o descriere. De asemenea, 
          aplicația va permite încărcarea, crearea și editarea imaginilor 
          prin intermediul unui editor integrat. După încărcare, fiecare 
          imagine va fi transmisă moderatorilor pentru evaluare, 
          urmând ca aceștia să aprobe sau să respingă publicarea pe site.
        </p>
    </body>
    ''')

def afis_data(tip=None):
    zile = ['Luni', 'Marți', 'Miercuri', 'Joi', 'Vineri', 'Sâmbătă', 'Duminică']
    luni = ['Ianuarie', 'Februarie', 'Martie', 'Aprilie', 'Mai', 'Iunie',
            'Iulie', 'August', 'Septembrie', 'Octombrie', 'Noiembrie', 'Decembrie']
    acum = datetime.datetime.now()
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

def info(request):
    param = request.GET.get("data")
    sectiune_data = afis_data(param)

    return HttpResponse(f'''
        <head>
            <title>Info</title>
        </head>
        <body>
            <h1>Informatii despre server</h1>
            {sectiune_data}
        </body>
    ''')

class Accesare:
    _id_counter = 1

    def __init__(self, ip_client=None, url=None, data=None):
        self.id = Accesare._id_counter
        Accesare._id_counter += 1
        self.ip_client = ip_client
        self.url = url
        self._data = data if data else datetime.datetime.now()

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