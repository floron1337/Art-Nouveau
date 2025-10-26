import datetime
from urllib.parse import urlparse
from ordered_set import OrderedSet

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

LOG_ENTRIES = []

class AccessLogEntry:
    _id_counter = 0

    def __init__(self, ip_client=None, url=None, data=None):
        self.id = AccessLogEntry._id_counter
        AccessLogEntry._id_counter += 1
        self.ip_client = ip_client
        self.url = url
        self._data = data if data else datetime.datetime.now()

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


def get_ip(request):
    str_lista_ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if str_lista_ip:
        return str_lista_ip.split(',')[-1].strip()
    else:
        return request.META.get('REMOTE_ADDR')

class BaseLoggableView(View):
    def dispatch(self, request, *args, **kwargs):
        LOG_ENTRIES.append(AccessLogEntry(
            get_ip(request),
            request.build_absolute_uri(),
            datetime.datetime.now()
        ))
        return super().dispatch(request, *args, **kwargs)

class IndexView(BaseLoggableView):
    def get(self, request):
        return render(request, "Art_Nouveau/index.html")

class AboutView(BaseLoggableView):
    def get(self, request):
        return render(request, "Art_Nouveau/about.html")

class ProductsView(BaseLoggableView):
    def get(self, request):
        return render(request, "Art_Nouveau/wip.html")

class ContactView(BaseLoggableView):
    def get(self, request):
        return render(request, "Art_Nouveau/wip.html")

class CartView(BaseLoggableView):
    def get(self, request):
        return render(request, "Art_Nouveau/wip.html")

class InfoView(BaseLoggableView):
    def afis_data(self, tip=None):
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

    def get(self, request):
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
        return HttpResponse(html)
