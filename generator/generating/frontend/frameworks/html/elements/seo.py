import json
from typing import List
from generating.frontend.frameworks.html.elements.html_element import HtmlElement
from generating.frontend.frameworks.html.elements.utils import meta
from generating.generators.file import GeneratedFile

##https://next.realfavicongenerator.net/
class Seo:
  def __init__(
      self
  ):
    self.elements:List[HtmlElement] = []
    self.files:List[GeneratedFile]  = []

  def get_elements(self):
     return self.elements
  def get_files(self):
     return self.files
