from generating.frontend.frameworks.html.html_element import HtmlElement


class SidebarHtmlElement(HtmlElement):
    def __init__(self, elements=None, **params):
        super().__init__(tag='ul', **params)
        self.elements = elements if elements is not None else []

    def get_sidebar_html(self):
        items_html = ''
        for element in self.elements:
            if isinstance(element, HtmlElement):
                li_element = HtmlElement(tag='li', content=element.get_html())
                items_html += li_element.get_html()
            elif isinstance(element, dict):
                content_elements = []
                if 'icon' in element:
                    icon_element = HtmlElement(tag='i', attributes={'class': element['icon']})
                    content_elements.append(icon_element)
                if 'title' in element:
                    title_element = HtmlElement(tag='span', content=element['title'])
                    content_elements.append(title_element)

                content_html = ''.join([elem.get_html() for elem in content_elements])
                link_element = HtmlElement(tag='a', attributes={'href': element['link']}, content=content_html)
                li_element = HtmlElement(tag='li', content=link_element.get_html())
                items_html += li_element.get_html()
        return items_html

    def get_content(self):
        return self.get_sidebar_html()
