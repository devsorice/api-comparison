

from generating.frontend.frameworks.html.elements.html_element import HtmlElement


class SidebarHtmlElement(HtmlElement):
    def __init__(self, elements, **params):
        self.params  = params
        super().__init__(tag='aside', **params)
        self.attr('class', 'page-sidebar')
        self.elements = elements if elements is not None else []

        self.nav_wrap = HtmlElement(tag='nav', _class='left-nav-wrap')
        self.nav_ul   = HtmlElement(tag='ul')

        self.nav_wrap.add_children(self.nav_ul)
        self.add_children(self.nav_wrap)

        self.links_by_href = {
        }
        self.parents_by_href = {
        }
        self.grandparents_by_href = {
        }

    def create_li(self):
        return HtmlElement(tag='li')

    def clone(self):
       return SidebarHtmlElement(self.elements, **self.params)

    def create_sidebar_link(self, title='', href=None, icon=None, tag='a'):
      a = HtmlElement(tag=tag)
      if href is not None:
        a.attr('href', href)
        self.links_by_href[href] = a
      if icon is not None:
          i = HtmlElement(tag='i')
          i.add_class(icon)
          a.add_children(i)
      a.add_children(HtmlElement(tag='span', content=title, __class='title'))
      a.add_children(HtmlElement(tag='span', _class='arrow'))
      return a

    def set_active(self, href=None):
       copy = self.clone()
       copy.setup_sidebar()
       if href:
          if href in copy.links_by_href:
             link:HtmlElement = copy.links_by_href[href]
             link.add_class('active')
          if href in copy.parents_by_href:
             ul:HtmlElement = copy.parents_by_href[href]
             ul.attr('hidden',False)
          if href in copy.grandparents_by_href:
             li:HtmlElement = copy.grandparents_by_href[href]
             li.add_class('open')

       return copy

    def create_sidebar_li(self, element:dict):
        li = HtmlElement(tag='li')

        _link_tag = 'a'
        _open = element.get('open', False)
        _has_children = 'children' in element and element['children']
        _parent_class = 'parent'
        _class_name = ''
        href  = element.get('href', None)
        if _has_children:
          _class_name   = _parent_class
          _link_tag     = 'div'
          href          = None
        if _open:
           _class_name += ' open'
        title = element.get('title', '')

        children = element.get('children', None)
        icon = element.get('icon', None)

        #####TESTO PRINCIPALE
        li.add_class(_class_name)
        a = self.create_sidebar_link(title=title, href=href, icon=icon, tag=_link_tag)
        li.add_children(a)

        if _has_children:
           ul = HtmlElement(tag='ul', _class='nav-sub')
           if not _open:
              ul.attr('hidden',True)
           for child in children:
              title = child.get('title', '')
              href  = child.get('href', None)
              icon = child.get('icon', None)
              subli = HtmlElement(tag='li', _class='sub-section')
              if href:
                 self.parents_by_href[href] = ul
                 self.grandparents_by_href[href] = li
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

    def clone(self):
      return UiKitSidebarElement(self.elements, **self.params)
    def create_li(self):
        return HtmlElement(tag='li', _class='uk-parent')

    def create_sidebar_link(self, title='', href=None, icon=None, tag='a'):
      a = HtmlElement(tag=tag)
      if href is not None:
        a.attr('href', href)
        self.links_by_href[href] = a
      if icon is not None:
          i = HtmlElement(tag='i')
          i.add_class(icon)
          a.add_children(i)
      a.add_children(HtmlElement(tag='span', content=title, __class='title'))
      a.add_children(HtmlElement(tag='span', _class='arrow'))
      return a

    def create_sidebar_li(self, element:dict):
        li = HtmlElement(tag='li')
        _link_tag = 'a'
        _open = element.get('open', False)
        _has_children = 'children' in element and element['children']
        _parent_class = 'uk-parent parent'
        _class_name = ''
        href  = element.get('href', None)

        if _has_children:
          _class_name   = _parent_class
          _link_tag     = 'div'
          href          = None
        if _open:
           _class_name += ' uk-open open'

        title = element.get('title', '')

        children = element.get('children', None)
        icon = element.get('icon', None)

        #####TESTO PRINCIPALE
        li.add_class(_class_name)
        a = self.create_sidebar_link(title=title, href=href, icon=icon, tag=_link_tag)
        li.add_children(a)

        if _has_children:
           ul = HtmlElement(tag='ul', _class='uk-nav-sub nav-sub')
           if not _open:
              ul.attr('hidden',True)
           for child in children:
              title = child.get('title', '')
              href  = child.get('href', None)
              icon = child.get('icon', None)
              subli = HtmlElement(tag='li', _class='sub-section')
              if href:
                 self.parents_by_href[href] = ul
                 self.grandparents_by_href[href] = li
              a = self.create_sidebar_link(title=title,href=href,icon=icon)
              subli.add_children(a)
              ul.add_children(subli)

           li.add_children(ul)
        return li


