
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
from generating.generators.crud_dashboard.crud_dashboard_generator import CrudDashboardBackendGenerator
from generating.generators.file import GeneratedFile, ReadFile, StringFile
from generating.frontend.frameworks.html.elements.favicon import Favicon
from generating.frontend.frameworks.html.elements.html_element import HtmlElement
from generating.frontend.frameworks.html.elements.sidebar_element import SidebarHtmlElement
from generating.frontend.frameworks.html.elements.topbar_element import TopbarHtmlElement
import os

from generating.frontend.frameworks.frameworks import FrontendFrameworks
from generating.frontend.icons.icon import Icon
from generating.backend.frameworks.rust.rust import RustModel
from generating.backend.frameworks.frameworks import BackendFramewoks

class CrudDahboardRustAxumGenerator(CrudDashboardBackendGenerator):
    def model_to_file(self, path:str, model:RustModel)-> GeneratedFile | None:
        return GeneratedFile(path,
                             model.generate_rust_code
                             )

    def add_model_to_files(self, app, model:RustModel):
        file = self.model_to_file(f'backend/models/{model.model.slug_singular}.rs', model)
        app.add_file(file)



    def generate(self, app):
        self.fr = BackendFramewoks.RUST_AXUM

        app.add_static_asset(self.fr, 'web_server/docker-compose.yml', 'backend/docker-compose.yml')
        app.add_static_asset(self.fr, 'web_server/Dockerfile',         'backend/Dockerfile')
        app.add_file(StringFile('frontend/up.sh', 'docker compose up -d --build --remove-orphans'))

        self.generate_models(app)

    def generate_models(self, app):
        for model in app.get_models():
            rust_model = RustModel(model)
            self.add_model_to_files(app,rust_model)

