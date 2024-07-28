from enum import Enum, auto
from generating.model.model import Model


class PermissionType(Enum):
    CREATE     = auto()
    READ       = auto()
    UPDATE     = auto()
    DELETE     = auto()
    SUPER      = auto()


class Permission:
    ##tp: TYPE OF PERMISSION
    ##onModel: IF NONE, THE PERMISSION IS APPLIED ON ALL MODELS
    ##onField:  IF NONE, THE PERMISSION IS APPLIED ON ALL FIELDS
    def __init__(self,
                      tp:PermissionType,
                      onModel:Model=None,
                      onField:str=None
                ):
      self.tp       = tp
      self.onModel  = onModel
      self.onField  = onField
