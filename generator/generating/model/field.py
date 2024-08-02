from generating.model.type import Type

class Field:
  def __init__(self, tp:Type=Type.SHORT_TEXT_INPUT_TYPE_TEXT, creatable=True, updateable=True, showable=True,listable=False, required=False, is_title=False, searchable=True, duplicateable=True, importance=0, title='', description=''):
      self.tp = tp
      self.creatable     = creatable     ## IF is creatable, it will be shown in the create page,  and it will be accepted by the create method of the backend
      self.updateable    = updateable    ## IF is updateable, it will be shown in the update page, and it will be updateable by the backend
      self.showable      = showable      ## IF is showable, it will be shown in the show page, and it will be returned by the get by id method of the backend
      self.listable      = listable      ## IF is listable, it will be shown in the list page, and  it will be returned by the list method of the backend
      self.required      = required      ## IF is required, the field data must be entered in the create page, and cannot be emptied in the update page, the create method of the backend requires this field to be given
      self.is_title      = is_title      ## IF is title, the value of the field will be shown as title in the show, edit and create page
      self.searchable    = searchable    ## If searchable, it will appear in the searchable fields in the
      self.duplicateable = duplicateable ## if duplicatable, when duplicating the record, this field will be copied in the new record
      self.importance    = importance    ## This will determine order of fields on pages
      self.title         = title         ## This will be the name of the field shown to the user
      self.description   = description   ## This description will be shown to the user to explain what this field is for
