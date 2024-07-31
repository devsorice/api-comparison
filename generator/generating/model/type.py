from enum import Enum, auto
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
