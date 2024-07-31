
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
from generating.generators.file import GeneratedFile
from generator.generating.frontend.frameworks.html.elements.html_element import HtmlElement
from generator.generating.frontend.frameworks.html.elements.sidebar_element import SidebarHtmlElement
from generator.generating.frontend.frameworks.html.elements.topbar_element import TopbarHtmlElement


class CrudDahboardVanillaJSGenerator(CrudDashboardFrontendGenerator):
    def page_to_file(self, path:str, page:HtmlPage)-> GeneratedFile | None:
        return GeneratedFile(path,
                             page.build
                             )

    def add_page_to_files(self, app, path:str, page:HtmlPage):
        file = self.page_to_file(path, page)
        app.add_file(file)

    def generate(self, app):
        sidebar_html_element = self.generate_sidebar(app)
        topbar_html_element  = self.generate_topbar(app)

        dashboard_page      = self.generate_dashboard_page(app)
        self.add_page_to_files(app, 'dashboard.html', dashboard_page)

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


            self.add_page_to_files(app, f'{model.slug_singular}/create.html', create_page)
            self.add_page_to_files(app, f'{model.slug_singular}/list.html', list_page)
            self.add_page_to_files(app, f'{model.slug_singular}/show.html', show_page)
            self.add_page_to_files(app, f'{model.slug_singular}/update.html', update_page)





    def generate_sidebar(self, app):
        sidebar_items = [
            {'icon': 'fa-home', 'title': 'Home', 'link': '/home'},
            {'title': 'Profile', 'link': '/profile'},  # No icon here
            HtmlElement(tag='div', content='Custom HTML Element', attributes={'class': 'custom-element'})
        ]
        ####SHOULD LOOP THE MODELS
        sidebar = SidebarHtmlElement(attributes={'class': 'sidebar'}, elements=sidebar_items)
        return sidebar

    def generate_topbar(self, app):
        topbar_items = [
          HtmlElement(tag='div', content='Custom HTML Element', attributes={'class': 'custom-element'})
        ]
        topbar = TopbarHtmlElement(topbar_items)
        return topbar

    def generate_dashboard_page(self, app):
      dashboard_page = DashboardPage('dashboard')
      return dashboard_page
