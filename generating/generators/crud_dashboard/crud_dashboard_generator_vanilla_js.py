
####THIS CLASS WILL GENERATE
######README.MD with explanation and all the stack used
#####FRONTEND REPOSITORY
#####BACKEND  REPOSITORY  + SWAGGER DOCUMENTATION
#####SQL MIGRATION OR MONGO MIGRATIONS
from typing import List
from generating.frontend.html_element import HtmlElement
from generating.frontend.sidebar_element import SidebarHtmlElement
from generating.generators.app import App
from generating.generators.crud_dashboard.crud_dashboard_generator import CrudDashboardFrontendGenerator
from generating.model.model import Model


class CrudDahboardVanillaJSGenerator(CrudDashboardFrontendGenerator):
    def generate(self, app:App):
        sidebar_html_element = self.generate_sidebar(app)
        topbar_html_element  = self.generate_topbar()


    def generate_sidebar(self, app:App):
        sidebar_items = [
            {'icon': 'fa-home', 'title': 'Home', 'link': '/home'},
            {'title': 'Profile', 'link': '/profile'},  # No icon here
            HtmlElement(tag='div', content='Custom HTML Element', attributes={'class': 'custom-element'})
        ]
        ####SHOULD LOOP THE MODELS
        sidebar = SidebarHtmlElement(attributes={'class': 'sidebar'}, elements=sidebar_items)
        return sidebar

