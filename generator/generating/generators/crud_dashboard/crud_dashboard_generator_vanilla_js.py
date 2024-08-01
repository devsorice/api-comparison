
####THIS CLASS WILL GENERATE
######README.MD with explanation and all the stack used
#####FRONTEND REPOSITORY
#####BACKEND  REPOSITORY  + SWAGGER DOCUMENTATION
#####SQL MIGRATION OR MONGO MIGRATIONS
from generating.frontend.frameworks.html.pages.create_page import CreatePage
from generating.frontend.frameworks.html.pages.dashboard_page import DashboardPage
from generating.frontend.frameworks.html.pages.list_page import ListPage
from generating.frontend.frameworks.html.pages.page import HtmlPage
from generating.frontend.frameworks.html.pages.show_page import ShowPage
from generating.frontend.frameworks.html.pages.update_page import UpdatePage
from generating.generators.crud_dashboard.crud_dashboard_generator import CrudDashboardFrontendGenerator
from generating.generators.file import GeneratedFile, ReadFile, StringFile
from generating.frontend.frameworks.html.elements.favicon import Favicon
from generating.frontend.frameworks.html.elements.html_element import HtmlElement
from generating.frontend.frameworks.html.elements.sidebar_element import SidebarHtmlElement
from generating.frontend.frameworks.html.elements.topbar_element import TopbarHtmlElement
import os

from generating.frontend.frameworks.frameworks import FrontendFrameworks
from generating.frontend.icons.icon import Icon

class CrudDahboardVanillaJSGenerator(CrudDashboardFrontendGenerator):
    def page_to_file(self, path:str, page:HtmlPage)-> GeneratedFile | None:
        return GeneratedFile(path,
                             page.build
                             )

    def add_page_to_files(self, app, path:str, page:HtmlPage):
        file = self.page_to_file('frontend/pages/'+path, page)
        app.add_file(file)

    def add_index_page(self, app, page:HtmlPage):
        file = self.page_to_file('frontend/index.html', page)
        app.add_file(file)


    def generate(self, app):
        self.fr = FrontendFrameworks.VANILLA_JS_AJAX
        self.icon_pack = app.get_icon_pack()

        app.add_static_asset(self.fr, 'css/sidebar.css',               'frontend/css/sidebar.css')
        app.add_static_asset(self.fr, 'js/sidebar.js',                 'frontend/js/sidebar.js')
        app.add_static_asset(self.fr, 'web_server/404.html',           'frontend/pages/errors/404.html')
        app.add_static_asset(self.fr, 'web_server/500.html',           'frontend/pages/errors/500.html')
        app.add_static_asset(self.fr, 'web_server/lighttpd.conf',      'frontend/lighttpd.conf')
        app.add_static_asset(self.fr, 'web_server/docker-compose.yml', 'frontend/docker-compose.yml')
        app.add_static_asset(self.fr, 'web_server/Dockerfile',         'frontend/Dockerfile')
        app.add_file(StringFile('frontend/up.sh', 'docker compose up -d --build --remove-orphans'))

        favicon              = Favicon(app_short_name=app.short_name, app_long_name=app.name)
        for file in favicon.get_files():
           app.add_file(GeneratedFile('frontend/'+file.get_path(), file.get_read_function()))

        sidebar_html_element = self.generate_sidebar(app)
        topbar_html_element  = self.generate_topbar(app)

        dashboard_page      = self.generate_dashboard_page(app)
        dashboard_page.header_element.add_children(topbar_html_element)
        dashboard_page.body_element.add_children(sidebar_html_element)

        for framework in app.get_active_frontend_libraries():
           framework.process_page(dashboard_page)
        self.icon_pack.load(dashboard_page)

        self.add_index_page(app, dashboard_page)

        for model in app.models:
            create_page    =  CreatePage(f'Crea {model.title_singular}',     favicon=favicon, description=f'Pagina con form per creare una nuova entità di tipo {model.title_singular}')
            list_page      =  ListPage(f'Lista {model.title_plural}',      favicon=favicon, description=f'Pagina di lista per cercare e visualizzare tutte le entità di tipo {model.title_singular} memorizzate')
            show_page      =  ShowPage(f'Mostra {model.title_singular}',     favicon=favicon, description=f'Pagina per visualizzare il dettaglio di una singola entità di tipo {model.title_singular}')
            update_page    =  UpdatePage(f'Aggiorna {model.title_singular}', favicon=favicon, description=f"Pagina con form per aggiornare un'entità di tipo {model.title_singular} già esistente")

            create_page.header_element.add_children(topbar_html_element)
            list_page.header_element.add_children(topbar_html_element)
            show_page.header_element.add_children(topbar_html_element)
            update_page.header_element.add_children(topbar_html_element)

            create_page.body_element.add_children(sidebar_html_element)
            list_page.body_element.add_children(sidebar_html_element)
            show_page.body_element.add_children(sidebar_html_element)
            update_page.body_element.add_children(sidebar_html_element)

            self.icon_pack.load(create_page)
            self.icon_pack.load(list_page)
            self.icon_pack.load(show_page)
            self.icon_pack.load(update_page)



            for framework in app.get_active_frontend_libraries():
                framework.process_page(create_page)
                framework.process_page(list_page)
                framework.process_page(show_page)
                framework.process_page(update_page)

            self.add_page_to_files(app, f'{model.slug_singular}/create.html', create_page)
            self.add_page_to_files(app, f'{model.slug_singular}/list.html', list_page)
            self.add_page_to_files(app, f'{model.slug_singular}/show.html', show_page)
            self.add_page_to_files(app, f'{model.slug_singular}/update.html', update_page)




    def generate_sidebar(self, app):
        sidebar_items = [
            {'title':'Dashboard', 'icon':self.icon_pack.translate_icon(Icon.HOME), 'href':'/index.html', 'selected':True}
        ]

        for model in app.get_models():
            item = {}
            item['open'] = False
            item['title'] = model.title_singular
            if hasattr(model, 'icon') and isinstance(model.icon, Icon):
              item['icon'] = self.icon_pack.translate_icon(model.icon)
            item['children'] = []
            item['children'].append({'title':f"Crea {model.title_singular}", 'href':f'/pages/{model.slug_singular}/create.html'})
            item['children'].append({'title':f"Lista {model.title_plural}", 'href':f'/pages/{model.slug_singular}/list.html'})
            item['children'].append({'title':f"Mostra {model.title_singular}", 'href':f'/pages/{model.slug_singular}/show.html'})
            item['children'].append({'title':f"Modifica {model.title_singular}", 'href':f'/pages/{model.slug_singular}/update.html'})
            sidebar_items.append(item)



        framework_sidebar = None
        for framework in app.get_active_frontend_libraries():
            created_sidebar = framework.generate_sidebar(sidebar_items, attributes={'class': 'sidebar'})
            if created_sidebar is not None:
                framework_sidebar = created_sidebar

        sidebar = framework_sidebar
        ####SHOULD LOOP THE MODELS
        if sidebar is None:
          sidebar = SidebarHtmlElement(attributes={'class': 'sidebar'}, elements=sidebar_items)

        sidebar.setup_sidebar()

        return sidebar

    def generate_topbar(self, app):
        topbar_items = [
          HtmlElement(tag='div', content='Custom HTML Element', attributes={'class': 'custom-element'})
        ]
        topbar = TopbarHtmlElement(topbar_items)
        return topbar

    def generate_dashboard_page(self, app):
      favicon        = Favicon(app_short_name=app.short_name, app_long_name=app.name)
      dashboard_page = DashboardPage('dashboard', favicon=favicon)
      return dashboard_page
