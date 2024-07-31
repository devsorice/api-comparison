from generator.generating.frontend.frameworks.html.elements.sidebar_element import UiKitSidebarElement
from generator.generating.frontend.frameworks.html.libraries.frontend_library import FrontendLibrary
from generator.generating.frontend.frameworks.html.pages.page import HtmlPage


class Uikit(FrontendLibrary):

  def process_page(self, page:HtmlPage):
    ###DOVREI CARICARE SOLO QUELLO CHE MI SERVE E NON DA UN PROGETTO ESTERNO
    page.add_css('https://cdn.jsdelivr.net/npm/uikit@3.21.8/dist/css/uikit.min.css')
    page.add_css('https://use.fontawesome.com/releases/v5.6.1/css/all.css')


  def generate_sidebar(elements, **params):
    return UiKitSidebarElement(elements, **params)
