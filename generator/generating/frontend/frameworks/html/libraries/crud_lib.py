from generating.frontend.frameworks.html.elements.sidebar_element import SidebarHtmlElement
from generating.frontend.frameworks.html.libraries.frontend_library import FrontendLibrary
from generating.frontend.frameworks.html.pages.page import HtmlPage


class CrudLib(FrontendLibrary):
  def process_page(self, page:HtmlPage):
    page.add_css('/css/sidebar.css')
    page.add_js('/js/sidebar.js')


  def generate_sidebar(self, elements, **params):
    return SidebarHtmlElement(elements, **params)
