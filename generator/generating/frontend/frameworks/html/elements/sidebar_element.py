

from generating.frontend.frameworks.html.elements.html_element import HtmlElement


class SidebarHtmlElement(HtmlElement):
    def __init__(self, elements, **params):
        super().__init__(tag='aside', **params)
        self.elements = elements if elements is not None else []

        self.nav_wrap = HtmlElement(tag='nav', _class='left-nav-wrap')
        self.nav_ul   = HtmlElement(tag='ul')

        self.nav_wrap.add_children(self.nav_ul)
        self.add_children(self.nav_wrap)

    def create_li(self):
        return HtmlElement(tag='li')

    def create_sidebar_link(self, title='', href=None, icon=None):
      a = HtmlElement(tag='a')
      if href is not None:
        a.attr('href', href)
      if icon is not None:
          i = HtmlElement(tag='i')
          i.add_class(icon)
          a.add_children(i)
      a.add_children(HtmlElement(tag='span', content=title))
      a.add_children(HtmlElement(tag='span', _class='arrow'))
      return a

    def create_sidebar_li(self, element:dict):
        li = HtmlElement(tag='li')

        _open = element.get('open', False)
        _has_children = 'children' in element and element['children']
        _parent_class = 'parent'
        _class_name = ''
        if _has_children:
          _class_name   = _parent_class
        if _open:
           _class_name += ' open'

        title = element.get('title', '')
        href  = element.get('href', None)
        children = element.get('children', None)
        icon = element.get('icon', None)

        #####TESTO PRINCIPALE
        li.add_class(_class_name)
        a = self.create_sidebar_link(title=title, href=href, icon=icon)
        li.add_children(a)

        if _has_children:
           ul = HtmlElement('ul')
           for child in children:
              title = child.get('title', '')
              href  = child.get('href', None)
              icon = child.get('icon', None)
              subli = HtmlElement(tag='li', _class='sub-section')
              a = self.create_sidebar_link(title=title,href=href,icon=icon)
              subli.add_children(a)
              ul.add_children(subli)

           li.add_children(ul)
        return li


    def setup_sidebar(self):
       for element in self.elements:
          li_element = None
          if isinstance(element, HtmlElement):
            li_element = self.create_li()
            li_element.add_children(element)
          elif isinstance(element, dict):
            li_element = self.create_sidebar_li(element)

          if li_element is not None:
              self.nav_ul.add_children(li_element)



class UiKitSidebarElement(SidebarHtmlElement):
    def __init__(self, elements, **params):
        super().__init__(elements, **params)
        self.attr('class', 'uk-light uk-visible@m page-sidebar')
        self.nav_ul.attr('class', 'uk-nav uk-nav-default uk-nav-parent-icon')
        self.nav_ul.attr('data-uk-nav', True)


    def create_li(self):
        return HtmlElement(tag='li', _class='uk-parent')

    def create_sidebar_link(self, title='', href=None, icon=None):
      a = HtmlElement(tag='a')
      if href is not None:
        a.attr('href', href)
      if icon is not None:
          i = HtmlElement(tag='i')
          i.add_class(icon)
          a.add_children(i)
      a.add_children(HtmlElement(tag='span', content=title))
      a.add_children(HtmlElement(tag='span', _class='arrow'))
      return a

    def create_sidebar_li(self, element:dict):
        li = HtmlElement(tag='li')

        _open = element.get('open', False)
        _has_children = 'children' in element and element['children']
        _parent_class = 'uk-parent parent'
        _class_name = ''
        if _has_children:
          _class_name   = _parent_class
        if _open:
           _class_name += ' uk-open'

        title = element.get('title', '')
        href  = element.get('href', None)
        children = element.get('children', None)
        icon = element.get('icon', None)

        #####TESTO PRINCIPALE
        li.add_class(_class_name)
        a = self.create_sidebar_link(title=title, href=href, icon=icon)
        li.add_children(a)

        if _has_children:
           ul = HtmlElement(tag='ul', _class='uk-nav-sub')
           for child in children:
              title = child.get('title', '')
              href  = child.get('href', None)
              icon = child.get('icon', None)
              subli = HtmlElement(tag='li', _class='sub-section')
              a = self.create_sidebar_link(title=title,href=href,icon=icon)
              subli.add_children(a)
              ul.add_children(subli)

           li.add_children(ul)
        return li


