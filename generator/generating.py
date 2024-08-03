
from generating.auth.admin import AdminRole
from generating.auth.user import UserRole
from generating.backend.databases import Databases
from generating.backend.frameworks.frameworks import BackendFramewoks
from generating.frontend.frameworks.frameworks import FrontendFramework, FrontendFrameworks
from generating.frontend.icons.fontawesome_icon_pack import FontAwesomeIconPack
from generating.frontend.icons.icon import Icon
from generating.generators.crud_dashboard.crud_dashboard import CrudDashboard
from generating.model.fields import AddressField, ArrayField, AttachmentUploadNoPreviewField, ColorField, DateField, DateTimeField, EmailField, EnableDisableToggleField, EnumMultipleChoiceSelectField, EnumSingleChoiceRadioField, EnumSingleChoiceSelectField, FloatField, HtmlField, IntegerField, JsonField, LongTextField, MoneyAmountField, ObjectField, ParagraphTitleAndTextField, PasswordField, PhoneNumberField, PhotoUploadWithPreviewField, PrimaryKeyField, SefurlField, ShortTextField, TimeField, URLField, UUIDField, YesNoCheckboxField
from generating.model.model import Model
from generating.frontend.frameworks.libraries import FrontendLibraries

class UserModel(Model):
  table          = 'user'
  icon           = Icon.USER
  slug_singular  = 'user'
  slug_plural    = 'users'
  title_singular = 'Utente'
  title_plural   = 'Utenti'


  fields = {
    'id':    PrimaryKeyField(title='ID'   , importance=2),
    'name':  ShortTextField (title='Name' , is_title=True, listable=True, duplicateable=True),
    'email': EmailField     (title='Email', listable=True, importance=1)
  }

class TodolistEntryModel(Model):
  table          = 'todolist'
  icon           = Icon.CHECK
  slug_singular  = 'todo'
  slug_plural    = 'todos'
  title_singular = 'Cosa da Fare'
  title_plural   = 'Cose da Fare'

  foreign_keys = {
      'user': UserModel
  }


  fields = {
    'entry': ShortTextField(is_title=True, listable=True, duplicateable=True)
  }

class ExampleModel(Model):
    table = 'examples'
    icon = 'example_icon'
    slug_singular = 'example'
    slug_plural = 'examples'
    title_singular = 'Example'
    title_plural = 'Examples'

    fields = {
        'id': PrimaryKeyField(title='ID', importance=2),
        'name': ShortTextField(title='Name', is_title=True, listable=True, duplicateable=True),
        'email': EmailField(title='Email', listable=True, importance=1),
        'age': IntegerField(title='Age', required=True, listable=True),
        'height': FloatField(title='Height', listable=True),
        'description': LongTextField(title='Description', required=False),
        'address': AddressField(title='Address', listable=True),
        'website': URLField(title='Website'),
        'birthdate': DateField(title='Birthdate', required=True),
        'last_login': DateTimeField(title='Last Login', required=False),
        'preferred_time': TimeField(title='Preferred Time', required=False),
        'settings': ObjectField(title='Settings', required=False),
        'profile_picture': PhotoUploadWithPreviewField(title='Profile Picture'),
        'resume': AttachmentUploadNoPreviewField(title='Resume', required=True),
        'phone_number': PhoneNumberField(title='Phone Number', required=True),
        'slug': SefurlField(title='Slug', required=True),
        'tags': ArrayField(title='Tags', required=False),
        'bio': ParagraphTitleAndTextField(title='Bio', required=False),
        'metadata': JsonField(title='Metadata', required=False),
        'content': HtmlField(title='Content', required=False),
        'uuid': UUIDField(title='UUID', required=True),
        'is_active': YesNoCheckboxField(title='Is Active'),
        'is_verified': EnableDisableToggleField(title='Is Verified'),
        'favorite_color': ColorField(title='Favorite Color'),
        'password': PasswordField(title='Password', required=True),
        'role': EnumSingleChoiceRadioField(title='Role', required=True),
        'status': EnumSingleChoiceSelectField(title='Status', required=True),
        'permissions': EnumMultipleChoiceSelectField(title='Permissions', required=False),
        'salary': MoneyAmountField(title='Salary', required=True),
    }



generator = CrudDashboard(
      name="Todo Dashboard",
      short_name="Crud",
      roles=[
          AdminRole(), #### Can do Everything by default
          UserRole()   ###  Can't do Anything by default
      ],
      models=[UserModel(), TodolistEntryModel(), ExampleModel()],
      frontend=FrontendFramework(FrontendFrameworks.VANILLA_JS_AJAX , FontAwesomeIconPack, [FrontendLibraries.DATA_TABLE, FrontendLibraries.CRUD_LIB]),
      backend=BackendFramewoks.RUST_AXUM,
      database=Databases.POSTGRES
)
generator.generate_code()
generator.save('generated_code')
