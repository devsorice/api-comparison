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
  def __init__(self, tp:Type=Type.SHORT_TEXT_INPUT_TYPE_TEXT, creatable=True, updateable=True, showable=True,listable=False, required=False, is_title=False, searchable=True):
      self.tp = tp
      self.creatable    = creatable    ## IF is creatable, it will be shown in the create page,  and it will be accepted by the create method of the backend
      self.updateable   = updateable   ## IF is updateable, it will be shown in the update page, and it will be updateable by the backend
      self.showable     = showable     ## IF is showable, it will be shown in the show page, and it will be returned by the get by id method of the backend
      self.listable     = listable     ## IF is listable, it will be shown in the list page, and  it will be returned by the list method of the backend
      self.required     = required     ## IF is required, the field data must be entered in the create page, and cannot be emptied in the update page, the create method of the backend requires this field to be given
      self.is_title     = is_title     ## IF is title, the value of the field will be shown as title in the show, edit and create page
      self.searchable   = searchable   ## If searchable, it will appear in the searchable fields in the


class PrimaryKeyField(Field):
    def __init__(self, tp=Type.INTEGER_INPUT_TYPE_NUMBER, creatable=False, updateable=False, showable=True, listable=True, required=False, is_title=False, searchable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class TitleField(Field):
    def __init__(self, tp=Type.SHORT_TEXT_INPUT_TYPE_TEXT, creatable=True, updateable=True, showable=True, listable=True, required=True, is_title=True, searchable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class SefurlField(Field):
    def __init__(self, tp=Type.SLUG, creatable=True, updateable=False, showable=True, listable=False, required=True, is_title=False, searchable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class PhoneNumberField(Field):
    def __init__(self, tp=Type.PHONE_NUMBER, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class ShortTextField(Field):
    def __init__(self, tp=Type.SHORT_TEXT_INPUT_TYPE_TEXT, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class LongTextField(Field):
    def __init__(self, tp=Type.LONG_TEXT_TEXTAREA_NEEDED, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class AddressField(Field):
    def __init__(self, tp=Type.ADDRESS, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class URLField(Field):
    def __init__(self, tp=Type.URL, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class DateField(Field):
    def __init__(self, tp=Type.DATE, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class DateTimeField(Field):
    def __init__(self, tp=Type.DATETIME, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class TimeField(Field):
    def __init__(self, tp=Type.TIME, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class ObjectField(Field):
    def __init__(self, tp=Type.OBJECT, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=False):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class AttachmentUploadNoPreviewField(Field):
    def __init__(self, tp=Type.ATTACHMENT_UPLOAD_NO_PREVIEW, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=False):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class PhotoUploadWithPreviewField(Field):
    def __init__(self, tp=Type.PHOTO_UPLOAD_WITH_PREVIEW, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=False):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class NumberField(Field):
    def __init__(self, tp=Type.NUMBER_INPUT_TYPE_NUMBER, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class FloatField(Field):
    def __init__(self, tp=Type.FLOAT_INPUT_TYPE_NUMBER, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class IntegerField(Field):
    def __init__(self, tp=Type.INTEGER_INPUT_TYPE_NUMBER, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class EmailField(Field):
    def __init__(self, tp=Type.EMAIL, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class ArrayField(Field):
    def __init__(self, tp=Type.ARRAY, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=False):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class ParagraphTitleAndTextField(Field):
    def __init__(self, tp=Type.PARAGRAPH_TITLE_AND_TEXT, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class JsonField(Field):
    def __init__(self, tp=Type.JSON, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=False):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class HtmlField(Field):
    def __init__(self, tp=Type.HTML, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=False):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class UUIDField(Field):
    def __init__(self, tp=Type.UUID, creatable=False, updateable=False, showable=True, listable=False, required=True, is_title=False, searchable=False):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class YesNoCheckboxField(Field):
    def __init__(self, tp=Type.YES_NO_CHECKBOX, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=False):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class EnableDisableToggleField(Field):
    def __init__(self, tp=Type.ENABLE_DISABLE_TOGGLE, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=False):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class ColorField(Field):
    def __init__(self, tp=Type.COLOR, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=False):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class PasswordField(Field):
    def __init__(self, tp=Type.PASSWORD, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=False):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class EnumSingleChoiceRadioField(Field):
    def __init__(self, tp=Type.ENUM_SINGLE_CHOICE_RADIO, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class EnumSingleChoiceSelectField(Field):
    def __init__(self, tp=Type.ENUM_SINGLE_CHOICE_SELECT, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class EnumMultipleChoiceSelectField(Field):
    def __init__(self, tp=Type.ENUM_MULTIPLE_CHOICE_SELECT, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)

class MoneyAmountField(Field):
    def __init__(self, tp=Type.MONEY_AMOUNT, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=True):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable)


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
    pass

class FrontendGenerator(Generator):
    pass

class BackendGenerator(Generator):
    pass

class DatabaseGenerator(Generator):
    pass




####THIS CLASS WILL GENERATE
#####FRONTEND REPOSITORY
#####BACKEND  REPOSITORY  + SWAGGER DOCUMENTATION
#####SQL MIGRATION OR MONGO MIGRATIONS
class CrudDahboardVanillaJSGenerator(Generator):
    def generate(self, models:List[Model]=[]):
        pass




class CrudDashboard:
     def __init__(self):
        self.backend_generators:  Dict[BackendFramewoks, BackendGenerator]    = {}
        self.frontend_generators: Dict[FrontendFrameworks, FrontendGenerator] = {}
        self.database_generators: Dict[Databases, DatabaseGenerator] = {}
        self.frontend_generators[FrontendFrameworks.VANILLA_JS_AJAX]   = CrudDahboardVanillaJSGenerator()


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
    'name': ShortTextField(is_title=True, listable=True),
    'email': EmailField(listable=True)
  }

CrudDashboard()
CrudDashboard.generateCode(models=[UserModel()],
                           frontend=FrontendFrameworks.VANILLA_JS_AJAX,
                           backend=BackendFramewoks.RUST_AXUM,
                           database=Databases.POSTGRES)
