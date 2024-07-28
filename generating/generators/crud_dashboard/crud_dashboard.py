from typing import Dict, List

from generating.auth.role import Role
from generating.backend.databases import Databases
from generating.backend.frameworks import BackendFramewoks
from generating.frontend.frameworks import FrontendFrameworks
from generating.generators.backend_generator import BackendGenerator
from generating.generators.crud_dashboard.crud_dashboard_generator_vanilla_js import CrudDahboardVanillaJSGenerator
from generating.generators.database_generator import DatabaseGenerator
from generating.generators.frontend_generator import FrontendGenerator
from generating.model.model import Model


class CrudDashboard:
      def __init__(self):
        self.backend_generators:  Dict[BackendFramewoks, BackendGenerator]    = {}
        self.frontend_generators: Dict[FrontendFrameworks, FrontendGenerator] = {}
        self.database_generators: Dict[Databases, DatabaseGenerator] = {}
        self.frontend_generators[FrontendFrameworks.VANILLA_JS_AJAX]   = CrudDahboardVanillaJSGenerator()

      def generate_code(self, roles:List[Role], models:List[Model], frontend:FrontendFrameworks=None, backend:BackendFramewoks=None, database:Databases=None):
          if frontend is not None:
            frontend_generator = self.frontend_generators.get(frontend, None)
            if frontend_generator is not None:
                frontend_generator.generate(models)

          if backend is not None:
            backend_generator = self.backend_generators.get(backend, None)
            if backend_generator is not None:
                backend_generator.generate(models)

          if database is not None:
            database_generator = self.database_generators.get(database, None)
            if database_generator is not None:
                database_generator.generate(models)
