from generating.frontend.frameworks.html.elements.sidebar_element import UiKitSidebarElement
from generating.frontend.frameworks.html.libraries.frontend_library import FrontendLibrary
from generating.frontend.frameworks.html.pages.page import HtmlPage


class Uikit(FrontendLibrary):

  def process_page(self, page:HtmlPage):
    ###DOVREI CARICARE SOLO QUELLO CHE MI SERVE E NON DA UN PROGETTO ESTERNO
    page.add_css('https://cdn.jsdelivr.net/npm/uikit@3.21.8/dist/css/uikit.min.css')

  def generate_sidebar(self, elements, **params):
    return UiKitSidebarElement(elements, **params)
