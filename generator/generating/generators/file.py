import os
from typing import Callable




class GeneratedFile:
  def __init__(self, path:str, read_function:Callable):
    self.path = path
    self.read_function = read_function

  def get_path(self):
    return self.path

  def get_read_function(self):
    return self.read_function

  def save(self, basePath=''):
    file_path = basePath+'/'+self.path
    content=self.read_function()
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as file:
      # Write the string to the file
      file.write(content)


class StringFile(GeneratedFile):
  def __init__(self, path:str, str_data:str):
    super().__init__(path, self.read)
    self.path = path
    self.str_data = str_data

  def read(self):
    return self.str_data

class ReadFile(GeneratedFile):
  def __init__(self, path:str, from_path:str):
    super().__init__(path, self.read)
    self.path = path
    self.from_path = from_path

  def read(self):
    with open(self.from_path, 'r') as file:
          content = file.read()
          return content
