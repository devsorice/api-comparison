from generating.model.type import Type
from generating.model.field import Field


class PrimaryKeyField(Field):
    def __init__(self, tp=Type.INTEGER_INPUT_TYPE_NUMBER, creatable=False, updateable=False, showable=True, listable=True, required=False, is_title=False, searchable=True, duplicateable=False, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class TitleField(Field):
    def __init__(self, tp=Type.SHORT_TEXT_INPUT_TYPE_TEXT, creatable=True, updateable=True, showable=True, listable=True, required=True, is_title=True, searchable=True, duplicateable=True, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class SefurlField(Field):
    def __init__(self, tp=Type.SLUG, creatable=True, updateable=False, showable=True, listable=False, required=True, is_title=False, searchable=True, duplicateable=False, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class PhoneNumberField(Field):
    def __init__(self, tp=Type.PHONE_NUMBER, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=True, duplicateable=False, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class ShortTextField(Field):
    def __init__(self, tp=Type.SHORT_TEXT_INPUT_TYPE_TEXT, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=True, duplicateable=True, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class LongTextField(Field):
    def __init__(self, tp=Type.LONG_TEXT_TEXTAREA_NEEDED, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=True, duplicateable=True, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class AddressField(Field):
    def __init__(self, tp=Type.ADDRESS, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=True, duplicateable=True, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class URLField(Field):
    def __init__(self, tp=Type.URL, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=True, duplicateable=True, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class DateField(Field):
    def __init__(self, tp=Type.DATE, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=True, duplicateable=True, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class DateTimeField(Field):
    def __init__(self, tp=Type.DATETIME, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=True, duplicateable=True, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class TimeField(Field):
    def __init__(self, tp=Type.TIME, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=True, duplicateable=True, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class ObjectField(Field):
    def __init__(self, tp=Type.OBJECT, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=False, duplicateable=True, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class AttachmentUploadNoPreviewField(Field):
    def __init__(self, tp=Type.ATTACHMENT_UPLOAD_NO_PREVIEW, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=False, duplicateable=True, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class PhotoUploadWithPreviewField(Field):
    def __init__(self, tp=Type.PHOTO_UPLOAD_WITH_PREVIEW, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=False, duplicateable=True, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class NumberField(Field):
    def __init__(self, tp=Type.NUMBER_INPUT_TYPE_NUMBER, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=True, duplicateable=True, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class FloatField(Field):
    def __init__(self, tp=Type.FLOAT_INPUT_TYPE_NUMBER, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=True, duplicateable=True, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class IntegerField(Field):
    def __init__(self, tp=Type.INTEGER_INPUT_TYPE_NUMBER, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=True, duplicateable=True, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class EmailField(Field):
    def __init__(self, tp=Type.EMAIL, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=True, duplicateable=True, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class ArrayField(Field):
    def __init__(self, tp=Type.ARRAY, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=False, duplicateable=True, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class ParagraphTitleAndTextField(Field):
    def __init__(self, tp=Type.PARAGRAPH_TITLE_AND_TEXT, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=True, duplicateable=True, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class JsonField(Field):
    def __init__(self, tp=Type.JSON, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=False, duplicateable=True, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class HtmlField(Field):
    def __init__(self, tp=Type.HTML, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=False, duplicateable=True, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class UUIDField(Field):
    def __init__(self, tp=Type.UUID, creatable=False, updateable=False, showable=True, listable=False, required=True, is_title=False, searchable=False, duplicateable=True, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class YesNoCheckboxField(Field):
    def __init__(self, tp=Type.YES_NO_CHECKBOX, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=False, duplicateable=True, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class EnableDisableToggleField(Field):
    def __init__(self, tp=Type.ENABLE_DISABLE_TOGGLE, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=False, duplicateable=True, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class ColorField(Field):
    def __init__(self, tp=Type.COLOR, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=False, duplicateable=True, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class PasswordField(Field):
    def __init__(self, tp=Type.PASSWORD, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=False, duplicateable=True, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class EnumSingleChoiceRadioField(Field):
    def __init__(self, tp=Type.ENUM_SINGLE_CHOICE_RADIO, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=True, duplicateable=True, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class EnumSingleChoiceSelectField(Field):
    def __init__(self, tp=Type.ENUM_SINGLE_CHOICE_SELECT, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=True, duplicateable=True, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class EnumMultipleChoiceSelectField(Field):
    def __init__(self, tp=Type.ENUM_MULTIPLE_CHOICE_SELECT, creatable=True, updateable=True, showable=True, listable=False, required=False, is_title=False, searchable=True, duplicateable=True, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)

class MoneyAmountField(Field):
    def __init__(self, tp=Type.MONEY_AMOUNT, creatable=True, updateable=True, showable=True, listable=False, required=True, is_title=False, searchable=True, duplicateable=True, importance=0,title='', description=''):
        super().__init__(tp=tp, creatable=creatable, updateable=updateable, showable=showable, listable=listable, required=required, is_title=is_title, searchable=searchable, duplicateable=duplicateable, importance=importance, title=title, description=description)
