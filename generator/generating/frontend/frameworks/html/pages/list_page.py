

from typing import List
from generating.frontend.frameworks.html.pages.page import HtmlPage
from generating.frontend.frameworks.html.elements.favicon import Favicon
from generating.frontend.frameworks.html.elements.html_element import HtmlElement
from generating.frontend.frameworks.html.elements.table import Table
from generating.frontend.locales.languages import Language
from generating.frontend.settings.charset import Charset
from generating.model.model import Model
from generating.model.field import Field

class ListPage(HtmlPage):
  def __init__(self, model:Model, title: str = '', description: str = '', language: Language = Language.ENGLISH, charset: Charset = Charset.UTF_8, h1: str | None = None, main_content: HtmlElement | None = None, favicon: Favicon | None = None, css: List[str] | None = None, hide_header: bool = False, hide_footer: bool = False):
    super().__init__(title, description, language, charset, h1, main_content, favicon, css, hide_header, hide_footer)
    self.model = model

    self.table_container = HtmlElement(tag='div', _class='custom-table')

    table_header = []
    tmp_headers = []
    for field_id in model.fields:
      field = model.fields[field_id]
      if isinstance(field, Field):
        if field.listable:
          tmp_headers.append(
            {'title':field.title, 'importance':field.importance}
          )

    # Sorting the list of dictionaries by the 'importance' key in descending order
    sorted_data = sorted(tmp_headers, key=lambda x: x['importance'], reverse=True)
    table_header = [item['title'] for item in sorted_data]

    table_body  = []
    table = Table(th=table_header, td=table_body, _class='table')

    self.table_container.add_children(table)
    self.main_element.add_children(self.table_container)
