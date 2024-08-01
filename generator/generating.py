
from generating.auth.admin import AdminRole
from generating.auth.user import UserRole
from generating.backend.databases import Databases
from generating.backend.frameworks import BackendFramewoks
from generating.frontend.frameworks.frameworks import FrontendFramework, FrontendFrameworks
from generating.frontend.icons.fontawesome_icon_pack import FontAwesomeIconPack
from generating.frontend.icons.icon import Icon
from generating.generators.crud_dashboard.crud_dashboard import CrudDashboard
from generating.model.fields import EmailField, PrimaryKeyField, ShortTextField
from generating.model.model import Model
from generating.frontend.frameworks.libraries import FrontendLibraries

class UserModel(Model):
  icon           = Icon.USER
  slug_singular  = 'user'
  slug_plural    = 'users'
  title_singular = 'Utente'
  title_plural   = 'Utenti'


  fields = {
    'id': PrimaryKeyField(importance=2),
    'name': ShortTextField(is_title=True, listable=True, duplicateable=True),
    'email': EmailField(listable=True, importance=1)
  }

class TodolistEntryModel(Model):
  icon           = Icon.CHECK
  slug_singular  = 'todo'
  slug_plural    = 'todos'
  title_singular = 'Cosa da Fare'
  title_plural   = 'Cose da Fare'


  fields = {
    'user': UserModel,
    'entry': ShortTextField(is_title=True, listable=True, duplicateable=True)
  }


generator = CrudDashboard(
      name="Todo Dashboard",
      short_name="Crud",
      roles=[
          AdminRole(), #### Can do Everything by default
          UserRole()   ###  Can't do Anything by default
      ],
      models=[UserModel(), TodolistEntryModel()],
      frontend=FrontendFramework(FrontendFrameworks.VANILLA_JS_AJAX , FontAwesomeIconPack, [FrontendLibraries.CRUD_LIB]),
      backend=BackendFramewoks.RUST_AXUM,
      database=Databases.POSTGRES
)
generator.generate_code()
generator.save('generated_code')
