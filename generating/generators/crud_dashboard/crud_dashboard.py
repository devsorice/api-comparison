from typing import List

from generating.auth.role import Role
from generating.backend.databases import Databases
from generating.backend.frameworks import BackendFramewoks
from generating.frontend.frameworks.frameworks import FrontendFrameworks
from generating.generators.app import App
from generating.generators.crud_dashboard.crud_dashboard_generator_vanilla_js import CrudDahboardVanillaJSGenerator
from generating.model.model import Model


class CrudDashboard(App):
      frontend_generators = {
         FrontendFrameworks.VANILLA_JS_AJAX:CrudDahboardVanillaJSGenerator()
      }
      backend_generators  = {}
      database_generators = {}

      def __init__(self,
                   name:str,
                   roles:List[Role],
                   models:List[Model],
                   frontend:FrontendFrameworks=None,
                   backend:BackendFramewoks=None,
                   database:Databases=None
                   ):
          super.__init__(self, name)
          self.roles = roles
          self.models = models
          self.frontend = frontend
          self.backend = backend
          self.database = database



      def generate_code(self):
          if self.frontend is not None:
            frontend_generator = self.frontend_generators.get(self.frontend, None)
            if frontend_generator is not None:
                frontend_generator.generate(self)

          if self.backend is not None:
            backend_generator = self.backend_generators.get(self.backend, None)
            if backend_generator is not None:
                backend_generator.generate(self)

          if self.database is not None:
            database_generator = self.database_generators.get(self.database, None)
            if database_generator is not None:
                database_generator.generate(self)


      def save(self, path=''):
          for file in self.files:
              file.save(path)
