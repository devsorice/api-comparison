from generating.frontend.frameworks.html.elements.html_element import HtmlElement


def meta(name='', content=''):
  return HtmlElement(tag='meta', attributes={
                'name':name,
                'content':content
            })

