from generating.frontend.locales.languages import Language
from generating.frontend.settings.charset import Charset
from generator.generating.frontend.frameworks.html.elements.favicon import Favicon
from generator.generating.frontend.frameworks.html.elements.html_element import HtmlElement


class HtmlPage:
    ### ISPIRAZIONE DA
    ### https://github.com/devsorice/redazione/blob/master/admin/ui/templates/app.tpl
    ### TO EXPAND
    def __init__(self, title:str='',
                       language:Language=Language.ENGLISH,
                       charset:Charset=Charset.UTF_8,
                       h1:str|None=None,
                       main_content:HtmlElement|None=None,
                       favicon:Favicon|None=None


                ):

        self.title = title
        self.h1    = title
        if h1 is None:
            self.h1 = title

        self.main_content = main_content


        self.html_element = HtmlElement(tag='html', attributes={
            'lang':language.value
        })

        ####HEAD#############################
        self.favicon = favicon
        if self.favicon is None:
            favicon = Favicon()

        self.head_element = HtmlElement(tag='head')
        self.head_element.add_children(
            HtmlElement(tag='meta', attributes={
                'charset':charset.value
            })
        )
        self.head_element.add_children(
            HtmlElement(tag='meta', attributes={
                'charset':charset.value
            })
        )
        self.head_element.add_children(
            HtmlElement(tag='meta', attributes={
                'content':'width=device-width, initial-scale=1.0'
            })
        )
        self.head_element.add_children(
            HtmlElement(tag='title', content=title)
        )
        self.favicon = favicon
        if self.favicon is None:
            favicon = Favicon()

        for favicon_tag in self.favicon.get_elements():
          self.head_element.add_children(favicon_tag)

        self.html_element.add_children(self.head_element)
        #############################################


        ####BODY#############################
        self.body_element   = HtmlElement(tag='body')
        self.header_element = HtmlElement(tag='header')
        self.main_element   = HtmlElement(tag='main')
        self.title_element  = HtmlElement(tag='h1', content=self.h1)
        self.main_element.add_children(self.title_element)
        if main_content:
            self.main_element.add_children(main_content)
        self.footer_element = HtmlElement(tag='footer')

        self.body_element.add_children(self.header_element)
        self.body_element.add_children(self.main_element)
        self.body_element.add_children(self.footer_element)
        self.html_element.add_children(self.body_element)
        #########################################




    def build(self):
        html =  '<!DOCTYPE html>'
        html = html+self.html_element.get_html()
        return html

