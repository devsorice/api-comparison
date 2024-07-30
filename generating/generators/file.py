import os
from typing import Callable


class GeneratedFile:
  def __init__(self, path:str, read_function:Callable):
    self.path = path
    self.read_function = read_function

  def save(self, basePath=''):
    file_path = basePath+'/'+self.path
    content=self.read_function()
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as file:
      # Write the string to the file
      file.write(content)
