##THIS IS TO CREATE HTML
from typing import List
import re


class HtmlElement:
    fields = ['tag', 'attributes', 'content', 'closing', 'before', 'after', 'description', 'icon', 'title']
    default_values = {'closing': 'default', 'attributes': {}, 'content': '', 'before': '', 'after': '', 'description': '', 'icon': '', 'title': '', 'class': ''}

    def __init__(self, **params):
        if params is None:
            params = {}
        self.__dict__.update(HtmlElement.default_values)
        self.__dict__.update(params)

    def attr(self, key, value):
        if not hasattr(self, 'attributes'):
            self.attributes = {}
        self.attributes[key] = str(value)

    def attr_get(self, key):
        if not hasattr(self, 'attributes') or key not in self.attributes:
            return ''
        return self.attributes[key]

    def render(self):
        self.add_class(self.get_class())
        self.attributes['class'] = self.trim(self.attributes['class'])

    def trim(self, text):
        text = text.strip()
        text = text.replace('  ', ' ')
        return text

    def add_class(self, class_name):
        prefix = ''
        if self.attr_get('class'):
            prefix = self.attr_get('class') + ' '
        self.attributes['class'] = prefix + class_name

    def get_class(self):
        # Placeholder for potential subclass logic
        return ''

    def get_tag_opening(self):
        tag_open = '<'
        if hasattr(self, 'tag'):
            tag_open += self.tag
        if hasattr(self, 'attributes') and isinstance(self.attributes, dict):
            for key, item in self.attributes.items():
                escaped_item = re.sub(r'[^a-zA-Z0-9]', lambda x: f'&#{ord(x.group())};', item)
                tag_open += f' {key}="{escaped_item}"'
        if hasattr(self, 'closing') and self.closing == 'self':
            tag_open += '/'
        tag_open += '>'
        return tag_open

    def get_tag_closing(self):
        if hasattr(self, 'closing') and self.closing == 'default' and hasattr(self, 'tag'):
            return f'</{self.tag}>'
        return ''

    def get_html(self):
        self.render()
        content = self.get_content()

        string = ''
        if hasattr(self, 'before'):
            string += self.before

        string += self.get_tag_opening()
        string += self.trim(content)
        string += self.get_tag_closing()

        if hasattr(self, 'after'):
            string += self.after

        return string

    def add_children(self, el):
        if not hasattr(self, 'content'):
            self.content = []
        elif isinstance(self.content, str) or isinstance(self.content, HtmlElement):
            self.content = [self.content]
        elif not isinstance(self.content, list):
            self.content = []

        if isinstance(el, str) or isinstance(el, HtmlElement):
            self.content.append(el)


    def get_content(self):
        if hasattr(self, 'content'):
            if isinstance(self.content, str):
                return self.trim(self.content)
            elif isinstance(self.content, HtmlElement):
                return self.content.get_html()
            elif isinstance(self.content, list):
                return ''.join([elem.get_html() for elem in self.content])
        return ''
