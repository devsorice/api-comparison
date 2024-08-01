from typing import List

from generating.auth.role import Role
from generating.backend.databases import Databases
from generating.backend.frameworks import BackendFramewoks
from generating.frontend.frameworks.frameworks import FrontendFramework, FrontendFrameworks
from generating.generators.app import App
from generating.generators.crud_dashboard.crud_dashboard_generator_vanilla_js import CrudDahboardVanillaJSGenerator
from generating.model.model import Model
from generating.frontend.frameworks.html.libraries.uikit import Uikit
from generating.frontend.frameworks.libraries import FrontendLibraries
import os

from generating.generators.file import ReadFile
from generating.frontend.frameworks.html.libraries.crud_lib import CrudLib

class CrudDashboard(App):
      def __init__(self,
                   name:str,
                   short_name:str|None=None,
                   roles:List[Role]=[],
                   models:List[Model]=[],
                   frontend:FrontendFramework=None,
                   backend:BackendFramewoks=None,
                   database:Databases=None
                   ):
          super().__init__(name, short_name)
          self.roles = roles
          self.models = models
          self.frontend_framework = frontend
          self.frontend  = frontend.get_frontend()

          self.backend = backend
          self.database = database

          self.frontend_libraries = {
            FrontendLibraries.UI_KIT:Uikit(),
            FrontendLibraries.CRUD_LIB:CrudLib()
          }
          self.active_frontend_libraries = []

          self.frontend_generators = {
            FrontendFrameworks.VANILLA_JS_AJAX:CrudDahboardVanillaJSGenerator()
          }
          self.static_files_folder = {
              FrontendFrameworks.VANILLA_JS_AJAX:'../../frontend/frameworks/html/static_files'
          }

          self.backend_generators  = {}
          self.database_generators = {}


      def get_icon_pack(self):
        return self.frontend_framework.get_icon_pack()

      def generate_code(self):
          if self.frontend is not None:
            frontend_generator = self.frontend_generators.get(self.frontend, None)
            if frontend_generator is not None:
                libs = self.frontend_framework.get_libraries()
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

      def get_models(self):
          return self.models

      def get_active_frontend_libraries(self):
          return self.active_frontend_libraries

      def get_static_asset_path(self, framework:FrontendFrameworks|BackendFramewoks, path:str=''):
        relative_path = self.static_files_folder.get(framework, None)
        if relative_path is not None:
          current_script_directory = os.path.dirname(os.path.abspath(__file__))
          if path!='':
            relative_path = f'{relative_path}/{path}'
          full_path = os.path.join(current_script_directory, relative_path)
          absolute_path = os.path.abspath(full_path)
          return absolute_path

      def add_static_asset(self,  framework:FrontendFrameworks|BackendFramewoks, from_path:str, destination_path:str):
         read_path = self.get_static_asset_path(framework, from_path)
         self.add_file(ReadFile(destination_path, read_path ))
