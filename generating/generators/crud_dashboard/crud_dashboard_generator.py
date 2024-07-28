from typing import List
from generating.generators.frontend_generator import FrontendGenerator
from generating.model.model import Model


class CrudDashboardFrontendGenerator(FrontendGenerator):
    def generate_sidebar(self):
        pass
    def generate_topbar(self):
        pass
    def generate_auth_page(self):
        pass
    def generate_list_page(self, model:Model):
        pass
    def generate_show_page(self, model:Model):
        pass
    def generate_create_page(self, model:Model):
        pass
    def generate_update_page(self, model:Model):
        pass
    def generate_dashboard_page(self, models:List[Model]=[]):
        pass
