
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
from generating.generators.file import GeneratedFile, ReadFile
from generating.frontend.frameworks.html.elements.favicon import Favicon
from generating.frontend.frameworks.html.elements.html_element import HtmlElement
from generating.frontend.frameworks.html.elements.sidebar_element import SidebarHtmlElement
from generating.frontend.frameworks.html.elements.topbar_element import TopbarHtmlElement
import os
import sys

class CrudDahboardVanillaJSGenerator(CrudDashboardFrontendGenerator):
    def page_to_file(self, path:str, page:HtmlPage)-> GeneratedFile | None:
        return GeneratedFile(path,
                             page.build
                             )

    def add_page_to_files(self, app, path:str, page:HtmlPage):
        file = self.page_to_file('frontend/pages/'+path, page)
        app.add_file(file)


    def generate(self, app):
        current_script_directory = os.path.dirname(os.path.abspath(__file__))
        sidebar_css_relative_path = '../../frontend/frameworks/html/css/sidebar.css'
        sidebar_css_full_path = os.path.join(current_script_directory, sidebar_css_relative_path)
        sidebar_css_absolute_path = os.path.abspath(sidebar_css_full_path)


        app.add_file(GeneratedFile('frontend/start_frontend.sh', lambda: 'python -m http.server 8230'))
        app.add_file(ReadFile('frontend/css/sidebar.css', sidebar_css_absolute_path))

        favicon              = Favicon(app_short_name=app.short_name, app_long_name=app.name)
        for file in favicon.get_files():
           app.add_file(GeneratedFile('frontend/'+file.get_path(), file.get_read_function()))

        sidebar_html_element = self.generate_sidebar(app)
        topbar_html_element  = self.generate_topbar(app)

        dashboard_page      = self.generate_dashboard_page(app)
        for framework in app.get_active_frontend_libraries():
           framework.process_page(dashboard_page)
        self.add_page_to_files(app, 'dashboard.html', dashboard_page)

        for model in app.models:
            create_page    =  CreatePage(f'Crea {model.title_singular}', favicon=favicon)
            list_page      =  ListPage(f'Lista {model.title_singular}', favicon=favicon)
            show_page      =  ShowPage(f'Mostra {model.title_singular}', favicon=favicon)
            update_page    =  UpdatePage(f'Aggiorna {model.title_singular}', favicon=favicon)

            create_page.header_element.add_children(topbar_html_element)
            list_page.header_element.add_children(topbar_html_element)
            show_page.header_element.add_children(topbar_html_element)
            update_page.header_element.add_children(topbar_html_element)

            create_page.body_element.add_children(sidebar_html_element)
            list_page.body_element.add_children(sidebar_html_element)
            show_page.body_element.add_children(sidebar_html_element)
            update_page.body_element.add_children(sidebar_html_element)


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
            {'icon': 'fa-home', 'title': 'Home', 'href': '/home'},
            {'title': 'Profile', 'href': '/profile'},  # No icon here
            HtmlElement(tag='div', content='Custom HTML Element', attributes={'class': 'custom-element'}),
            {'title':'test children', 'icon':'fa-file-word', 'open':False,
             'children':[
                  {
                      "title" : "Utenti",
                      "href" : "/users/list"
                  },
                  {
                      "title" : "Aggiungi Utente",
                      "href" : "/users/add"
                  }
             ] }
        ]
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
