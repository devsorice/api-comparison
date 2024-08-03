from typing import List
from generating.generators.app import App
from generating.generators.frontend_generator import FrontendGenerator
from generating.model.model import Model
from generating.generators.backend_generator import BackendGenerator


class CrudDashboardFrontendGenerator(FrontendGenerator):
    def generate_sidebar(self, App:App):
        pass
    def generate_topbar(self, App:App):
        pass
    def generate_auth_page(self, App:App):
        pass
    def generate_list_page(self, App:App):
        pass
    def generate_show_page(self, App:App):
        pass
    def generate_create_page(self, App:App):
        pass
    def generate_update_page(self, App:App):
        pass
    def generate_dashboard_page(self, App:App):
        pass



class CrudDashboardBackendGenerator(BackendGenerator):
    def generate_models(self, App:App):
        pass
