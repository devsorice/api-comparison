from enum import Enum, auto
from typing import List, Dict


##### THIS IS TO DEFINE THE "TYPE OF DATA" WE ARE TREATING
##### THIS WILL BE NEEDED FOR THREE PURPOSES
##### 1 IDENTIFY WHAT TYPE IS BEST IN THE DATABASE FOR THE TECH STACK WE HAVE CHOSEN
##### 2 IDENTIFY WHAT REGEX/PATTERN WE NEED TO VALIDATE THE FIELD - SO INFORMATION FOR VALIDATION
##### 3 IDENTIFY HOW THE USER WILL INTERACT WITH THIS TYPE OF DATA
class Type(Enum):
    PHONE_NUMBER                 = auto()
    LONG_TEXT_TEXTAREA_NEEDED    = auto()
    SHORT_TEXT_INPUT_TYPE_TEXT   = auto()
    ADDRESS                      = auto()
    URL                          = auto()
    DATE                         = auto()
    DATETIME                     = auto()
    TIME                         = auto()
    OBJECT                       = auto()
    ATTACHMENT_UPLOAD_NO_PREVIEW = auto()
    PHOTO_UPLOAD_WITH_PREVIEW    = auto()
    NUMBER_INPUT_TYPE_NUMBER     = auto()
    FLOAT_INPUT_TYPE_NUMBER      = auto()
    INTEGER_INPUT_TYPE_NUMBER    = auto()
    EMAIL                        = auto()
    ARRAY                        = auto()
    PARAGRAPH_TITLE_AND_TEXT     = auto()
    JSON                         = auto()
    HTML                         = auto()
    UUID                         = auto()
    YES_NO_CHECKBOX              = auto()
    ENABLE_DISABLE_TOGGLE        = auto()
    COLOR                        = auto()
    PASSWORD                     = auto()
    ENUM_SINGLE_CHOICE_RADIO     = auto()
    ENUM_SINGLE_CHOICE_SELECT    = auto()
    ENUM_MULTIPLE_CHOICE_SELECT  = auto()
    SLUG                         = auto()
    MONEY_AMOUNT                 = auto()

class Field:
  def __init__(self, tp:Type=Type.SHORT_TEXT_INPUT_TYPE_TEXT, creatable=True, updateable=True, showable=True,listable=False, required=False, is_title=False, searchable=True, duplicateable=True):
      self.tp = tp
      self.creatable     = creatable     ## IF is creatable, it will be shown in the create page,  and it will be accepted by the create method of the backend
      self.updateable    = updateable    ## IF is updateable, it will be shown in the update page, and it will be updateable by the backend
      self.showable      = showable      ## IF is showable, it will be shown in the show page, and it will be returned by the get by id method of the backend
      self.listable      = listable      ## IF is listable, it will be shown in the list page, and  it will be returned by the list method of the backend
      self.required      = required      ## IF is required, the field data must be entered in the create page, and cannot be emptied in the update page, the create method of the backend requires this field to be given
      self.is_title      = is_title      ## IF is title, the value of the field will be shown as title in the show, edit and create page
      self.searchable    = searchable    ## If searchable, it will appear in the searchable fields in the
      self.duplicateable = duplicateable ## if duplicatable, when duplicating the record, this field will be copied in the new record


class PrimaryKeyField(Field):
    def __init__(self, tp=Type.INTEGER_INPUT_TYPE_NUMBER, creatable=False, updateable=False, showable=True, listable=True, required=False, is_title=False, searchable=True, duplicateable=False):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class TitleField(Field):
    def __init__(self, tp=Type.SHORT_TEXT_INPUT_TYPE_TEXT, creatable=True, updateable=True, showable=True, listable=True, required=True, is_title=True, searchable=True, duplicateable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class SefurlField(Field):
    def __init__(self, tp=Type.SLUG, creatable=True, updateable=False, showable=True, listable=False, required=True, is_title=False, searchable=True, duplicateable=False):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class PhoneNumberField(Field):
    def __init__(self, tp=Type.PHONE_NUMBER, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=True, duplicateable=False):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class ShortTextField(Field):
    def __init__(self, tp=Type.SHORT_TEXT_INPUT_TYPE_TEXT, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=True, duplicateable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class LongTextField(Field):
    def __init__(self, tp=Type.LONG_TEXT_TEXTAREA_NEEDED, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=True, duplicateable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class AddressField(Field):
    def __init__(self, tp=Type.ADDRESS, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=True, duplicateable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class URLField(Field):
    def __init__(self, tp=Type.URL, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=True, duplicateable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class DateField(Field):
    def __init__(self, tp=Type.DATE, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=True, duplicateable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class DateTimeField(Field):
    def __init__(self, tp=Type.DATETIME, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=True, duplicateable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class TimeField(Field):
    def __init__(self, tp=Type.TIME, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=True, duplicateable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class ObjectField(Field):
    def __init__(self, tp=Type.OBJECT, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=False, duplicateable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class AttachmentUploadNoPreviewField(Field):
    def __init__(self, tp=Type.ATTACHMENT_UPLOAD_NO_PREVIEW, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=False, duplicateable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class PhotoUploadWithPreviewField(Field):
    def __init__(self, tp=Type.PHOTO_UPLOAD_WITH_PREVIEW, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=False, duplicateable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class NumberField(Field):
    def __init__(self, tp=Type.NUMBER_INPUT_TYPE_NUMBER, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=True, duplicateable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class FloatField(Field):
    def __init__(self, tp=Type.FLOAT_INPUT_TYPE_NUMBER, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=True, duplicateable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class IntegerField(Field):
    def __init__(self, tp=Type.INTEGER_INPUT_TYPE_NUMBER, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=True, duplicateable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class EmailField(Field):
    def __init__(self, tp=Type.EMAIL, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=True, duplicateable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class ArrayField(Field):
    def __init__(self, tp=Type.ARRAY, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=False, duplicateable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class ParagraphTitleAndTextField(Field):
    def __init__(self, tp=Type.PARAGRAPH_TITLE_AND_TEXT, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=True, duplicateable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class JsonField(Field):
    def __init__(self, tp=Type.JSON, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=False, duplicateable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class HtmlField(Field):
    def __init__(self, tp=Type.HTML, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=False, duplicateable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class UUIDField(Field):
    def __init__(self, tp=Type.UUID, creatable=False, updateable=False, showable=True, listable=False, required=True, is_title=False, searchable=False, duplicateable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class YesNoCheckboxField(Field):
    def __init__(self, tp=Type.YES_NO_CHECKBOX, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=False, duplicateable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class EnableDisableToggleField(Field):
    def __init__(self, tp=Type.ENABLE_DISABLE_TOGGLE, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=False, duplicateable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class ColorField(Field):
    def __init__(self, tp=Type.COLOR, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=False, duplicateable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class PasswordField(Field):
    def __init__(self, tp=Type.PASSWORD, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=False, duplicateable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class EnumSingleChoiceRadioField(Field):
    def __init__(self, tp=Type.ENUM_SINGLE_CHOICE_RADIO, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=True, duplicateable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class EnumSingleChoiceSelectField(Field):
    def __init__(self, tp=Type.ENUM_SINGLE_CHOICE_SELECT, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=True, duplicateable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class EnumMultipleChoiceSelectField(Field):
    def __init__(self, tp=Type.ENUM_MULTIPLE_CHOICE_SELECT, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=True, duplicateable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)

class MoneyAmountField(Field):
    def __init__(self, tp=Type.MONEY_AMOUNT, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=True, duplicateable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable)


class Databases(Enum):
    MONGODB   = auto()
    POSTGRES  = auto()

class FrontendFrameworks(Enum):
    VANILLA_JS_AJAX = auto()

class BackendFramewoks(Enum):
    RUST_AXUM  = auto()


class Model:
    pass

class Generator:
    def generate(self, models:List[Model]=[]):
        pass

class FrontendGenerator(Generator):
    pass



# class ListPage(Page):
# class ShowPage(Page):
# class CreatePage(Page):
# class UpdatePage(Page):
# class DashboardPage(Page):
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
    def generate_dashboard_page(self):
        pass

class BackendGenerator(Generator):
    pass

class DatabaseGenerator(Generator):
    pass




####THIS CLASS WILL GENERATE
#####FRONTEND REPOSITORY
#####BACKEND  REPOSITORY  + SWAGGER DOCUMENTATION
#####SQL MIGRATION OR MONGO MIGRATIONS
class CrudDahboardVanillaJSGenerator(CrudDashboardFrontendGenerator):
    def generate(self, models:List[Model]=[]):
        pass




class CrudDashboard:
      def __init__(self):
        self.backend_generators:  Dict[BackendFramewoks, BackendGenerator]    = {}
        self.frontend_generators: Dict[FrontendFrameworks, FrontendGenerator] = {}
        self.database_generators: Dict[Databases, DatabaseGenerator] = {}
        self.frontend_generators[FrontendFrameworks.VANILLA_JS_AJAX]   = CrudDahboardVanillaJSGenerator()

      def generate_code(self, models:List[Model], frontend:FrontendFrameworks=None, backend:BackendFramewoks=None, database:Databases=None):
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


# class ListPage(Page):
# class ShowPage(Page):
# class CreatePage(Page):
# class UpdatePage(Page):
# class DashboardPage(Page):

# class HtmlComponent:
#   def __init__(self, html, css, js):
#      self.html = html
#      self.css  = css
#      self.js   = js

#   def generate(self):
#      return f"
#           <style>

#      "


# class Page(Html):

####Example
class UserModel(Model):
  fields = {
    'id': PrimaryKeyField(),
    'name': ShortTextField(is_title=True, listable=True, duplicateable=True),
    'email': EmailField(listable=True)
  }

CrudDashboard()
CrudDashboard.generate_code(models=[UserModel()],
                           frontend=FrontendFrameworks.VANILLA_JS_AJAX,
                           backend=BackendFramewoks.RUST_AXUM,
                           database=Databases.POSTGRES)
