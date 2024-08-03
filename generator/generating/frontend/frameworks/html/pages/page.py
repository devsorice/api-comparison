from typing import List
from generating.frontend.locales.languages import Language
from generating.frontend.settings.charset import Charset
from generating.frontend.frameworks.html.elements.favicon import Favicon
from generating.frontend.frameworks.html.elements.html_element import HtmlElement
from datetime import datetime
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

class Page:
    def __init__(self, title:str='',
                       language:Language=Language.ENGLISH,
                       charset:Charset=Charset.UTF_8,
                       h1:str|None=None,
                       main_content:HtmlElement|None=None,
                       favicon:Favicon|None=None,
                       css:List[str]|None=None,
                       hide_header:bool=False,
                       hide_footer:bool=False
                ):
        pass

class HtmlPage(Page):
    def __init__(self, title:str='',
                       description:str='',
                       language:Language=Language.ENGLISH,
                       charset:Charset=Charset.UTF_8,
                       h1:str|None=None,
                       main_content:HtmlElement|None=None,
                       favicon:Favicon|None=None,
                       css:List[str]|None=None,
                       hide_header:bool=False,
                       hide_footer:bool=False
                ):

        self.title = title
        self.h1    = title
        if h1 is None:
            self.h1 = title
        self.description = description

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
                'name':'viewport',
                'content':'width=device-width, initial-scale=1.0'
            })
        )
        self.head_element.add_children(
            HtmlElement(tag='title', content=title)
        )
        self.head_element.add_children(
            HtmlElement(tag='meta', attributes={
                'name':'description',
                'content':description
            })
        )
        self.favicon = favicon
        if self.favicon is None:
            favicon = Favicon()

        for favicon_tag in self.favicon.get_elements():
          self.head_element.add_children(favicon_tag)


        if isinstance(css, list):
            for css_path in css:
                self.add_css(css_path)

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

        if not hide_header:
          self.body_element.add_children(self.header_element)
        self.body_element.add_children(self.main_element)
        if not hide_footer:
          self.body_element.add_children(self.footer_element)
        self.html_element.add_children(self.body_element)
        #########################################



    def add_css(self, path):
        path_with_version = self.add_version_query_string(path)
        self.head_element.add_children(HtmlElement(tag='link', attributes={
            'rel': 'stylesheet',
            'href': path_with_version
        }))

    def add_js(self, path):
        path_with_version = self.add_version_query_string(path)
        self.body_element.add_children(HtmlElement(tag='script', attributes={
            'src': path_with_version
        }))

    def add_version_query_string(self, path):
        url_parts = list(urlparse(path))
        query = parse_qs(url_parts[4])
        if not query:
            version = datetime.now().strftime('%Y%m%d%H%M%S')
            query['v'] = version
            url_parts[4] = urlencode(query, doseq=True)
        return urlunparse(url_parts)

    def build(self):
        html =  '<!DOCTYPE html>'
        html = html+self.html_element.get_html()
        return html

