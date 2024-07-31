from typing import List
from generating.generators.file import GeneratedFile


class App:
  def __init__(self, name):
    self.name = name
    self.files:List[GeneratedFile] = []


  def add_file(self, file:GeneratedFile):
          self.files.append(file)
