from typing import List
from generating.frontend.frameworks.html.elements.html_element import HtmlElement


class Table(HtmlElement):
  def __init__(self, th:List[str|HtmlElement]=[], td:List[List[str|HtmlElement]]=[], **params):
    super().__init__(tag='table', **params)

    self.header = HtmlElement(tag='thead')
    self.header_row = None

    if len(th)>0:
      self.header_row = HtmlElement(tag='tr')
      for field in th:
        cell = HtmlElement(tag='th')
        cell.add_children(field)
        self.header_row.add_children(cell)
      self.header.add_children(self.header_row)

    self.body   = HtmlElement(tag='tbody')

    if len(td)>0:
      for record in td:
        row = HtmlElement(tag='tr')
        for field in record:
          cell = HtmlElement(tag='td')
          cell.add_children(field)
          row.add_children(cell)
        self.body.add_children(row)

    self.add_children(self.header)
    self.add_children(self.body)
