from typing import List
from generating.generators.file import GeneratedFile


class App:
  def __init__(self, name:str, short_name:str|None=None):
    self.name = name
    if not short_name:
        self.short_name = name
    else:
        self.short_name = short_name
    self.files:List[GeneratedFile] = []


  def add_file(self, file:GeneratedFile):
          self.files.append(file)
