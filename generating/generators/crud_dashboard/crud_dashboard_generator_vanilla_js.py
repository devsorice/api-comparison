
####THIS CLASS WILL GENERATE
######README.MD with explanation and all the stack used
#####FRONTEND REPOSITORY
#####BACKEND  REPOSITORY  + SWAGGER DOCUMENTATION
#####SQL MIGRATION OR MONGO MIGRATIONS
from typing import List
from generating.frontend.frameworks.html.html_element import HtmlElement
from generating.frontend.frameworks.html.sidebar_element import SidebarHtmlElement
from generating.frontend.frameworks.html.topbar_element import TopbarHtmlElement
from generating.frontend.pages.create_page import CreatePage
from generating.frontend.pages.dashboard_page import DashboardPage
from generating.frontend.pages.list_page import ListPage
from generating.frontend.pages.page import Page
from generating.frontend.pages.show_page import ShowPage
from generating.frontend.pages.update_page import UpdatePage
from generating.generators.app import App
from generating.generators.crud_dashboard.crud_dashboard import CrudDashboard
from generating.generators.crud_dashboard.crud_dashboard_generator import CrudDashboardFrontendGenerator
from generating.generators.file import GeneratedFile
from generating.model.model import Model


class CrudDahboardVanillaJSGenerator(CrudDashboardFrontendGenerator):
    def page_to_file(self, path:str, page:Page)-> GeneratedFile | None:
        return GeneratedFile(path,
                             page.build
                             )

    def generate(self, app:CrudDashboard):
        sidebar_html_element = self.generate_sidebar(app)
        topbar_html_element  = self.generate_topbar(app)

        dashboard_page      = self.generate_dashboard_page(app)
        app.add_file('dashboard.html', dashboard_page)

        for model in app.models:
            create_page    =  CreatePage(f'Crea {model.title_singular}')
            list_page      =  ListPage(f'Lista {model.title_singular}')
            show_page      =  ShowPage(f'Mostra {model.title_singular}')
            update_page    =  UpdatePage(f'Aggiorna {model.title_singular}')

            create_page.header_element.add_children(topbar_html_element)
            list_page.header_element.add_children(topbar_html_element)
            show_page.header_element.add_children(topbar_html_element)
            update_page.header_element.add_children(topbar_html_element)

            create_page.body_element.add_children(sidebar_html_element)
            list_page.body_element.add_children(sidebar_html_element)
            show_page.body_element.add_children(sidebar_html_element)
            update_page.body_element.add_children(sidebar_html_element)

            app.add_file(f'{model.slug_singular}/create.html', create_page)
            app.add_file(f'{model.slug_singular}/list.html', list_page)
            app.add_file(f'{model.slug_singular}/show.html', show_page)
            app.add_file(f'{model.slug_singular}/update.html', update_page)





    def generate_sidebar(self, app:CrudDashboard):
        sidebar_items = [
            {'icon': 'fa-home', 'title': 'Home', 'link': '/home'},
            {'title': 'Profile', 'link': '/profile'},  # No icon here
            HtmlElement(tag='div', content='Custom HTML Element', attributes={'class': 'custom-element'})
        ]
        ####SHOULD LOOP THE MODELS
        sidebar = SidebarHtmlElement(attributes={'class': 'sidebar'}, elements=sidebar_items)
        return sidebar

    def generate_topbar(self, app:CrudDashboard):
        topbar_items = [
          HtmlElement(tag='div', content='Custom HTML Element', attributes={'class': 'custom-element'})
        ]
        topbar = TopbarHtmlElement(topbar_items)
        return topbar

    def generate_dashboard_page(self, app:CrudDashboard):
      dashboard_page = DashboardPage('dashboard')
      return dashboard_page
