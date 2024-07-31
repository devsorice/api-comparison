from typing import List

from generating.auth.role import Role
from generating.backend.databases import Databases
from generating.backend.frameworks import BackendFramewoks
from generating.frontend.frameworks.frameworks import FrontendFrameworks
from generating.generators.app import App
from generating.generators.crud_dashboard.crud_dashboard_generator_vanilla_js import CrudDahboardVanillaJSGenerator
from generating.model.model import Model
from generating.frontend.frameworks.html.libraries.uikit import Uikit
from generating.frontend.frameworks.libraries import FrontendLibraries


class CrudDashboard(App):
      frontend_libraries = {
          FrontendLibraries.UI_KIT:Uikit()
      }
      active_frontend_libraries = []

      frontend_generators = {
         FrontendFrameworks.VANILLA_JS_AJAX:CrudDahboardVanillaJSGenerator()
      }
      backend_generators  = {}
      database_generators = {}

      def __init__(self,
                   name:str,
                   short_name:str|None=None,
                   roles:List[Role]=[],
                   models:List[Model]=[],
                   frontend:FrontendFrameworks=None,
                   backend:BackendFramewoks=None,
                   database:Databases=None
                   ):
          super().__init__(name, short_name)
          self.roles = roles
          self.models = models
          self.frontend = frontend
          self.backend = backend
          self.database = database



      def generate_code(self):
          if self.frontend is not None:
            frontend_generator = self.frontend_generators.get(self.frontend, None)
            if frontend_generator is not None:
                libs = self.frontend.getLibraries()
                if libs is not None:
                  for lib in libs:
                      lib_instance = self.frontend_libraries.get(lib, None)
                      self.active_frontend_libraries.append(lib_instance)
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


      def get_active_frontend_libraries(self):
          return self.active_frontend_libraries

