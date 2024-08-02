from generating.frontend.frameworks.html.elements.sidebar_element import UiKitSidebarElement
from generating.frontend.frameworks.html.libraries.frontend_library import FrontendLibrary
from generating.frontend.frameworks.html.pages.page import HtmlPage
from generating.frontend.frameworks.html.pages.list_page import ListPage


class DataTable(FrontendLibrary):

  def process_page(self, page:HtmlPage):
    ###DOVREI CARICARE SOLO QUELLO CHE MI SERVE E NON DA UN PROGETTO ESTERNO
    if(isinstance(page, ListPage)):
      page.add_css('https://cdn.datatables.net/v/dt/dt-2.1.3/datatables.min.css')
      page.add_js('https://cdn.datatables.net/v/dt/dt-2.1.3/datatables.min.js')

  def generate_sidebar(self, elements, **params):
    return UiKitSidebarElement(elements, **params)
