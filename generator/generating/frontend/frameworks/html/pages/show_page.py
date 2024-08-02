from typing import List
from generating.frontend.frameworks.html.pages.page import HtmlPage
from generating.frontend.frameworks.html.elements.favicon import Favicon
from generating.frontend.frameworks.html.elements.html_element import HtmlElement
from generating.frontend.locales.languages import Language
from generating.frontend.settings.charset import Charset
from generating.model.model import Model



class ShowPage(HtmlPage):
  def __init__(self, model:Model, title: str = '', description: str = '', language: Language = Language.ENGLISH, charset: Charset = Charset.UTF_8, h1: str | None = None, main_content: HtmlElement | None = None, favicon: Favicon | None = None, css: List[str] | None = None, hide_header: bool = False, hide_footer: bool = False):
    super().__init__(title, description, language, charset, h1, main_content, favicon, css, hide_header, hide_footer)
    self.model = model
