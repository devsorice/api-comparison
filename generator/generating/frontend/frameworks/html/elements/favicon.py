import json
from typing import List
from generator.generating.frontend.frameworks.html.elements.html_element import HtmlElement
from generator.generating.frontend.frameworks.html.elements.utils import meta
from generator.generating.generators.file import GeneratedFile

##https://next.realfavicongenerator.net/
class Favicon:
  def __init__(
      self,
      app_short_name:str|None      = None,
      app_long_name:str|None       = None,
      favicon_48x48:str|None       = '/favicon-48x48.png',
      favicon_svg:str|None         = '/favicon.svg',
      favicon_ico:str|None         = '/favicon.ico',
      favicon_apple_touch:str|None = '/apple-touch-icon.png',
      theme_color:str|None         = '#fdfdfd"',
      background_color:str|None    = '#c5d3e3',
      favicon_192x192:str|None     = '/web-app-manifest-192x192.png',
      favicon_512x512:str|None     = '/web-app-manifest-512x512.png',
  ):
    self.elements:List[HtmlElement] = []
    self.files:List[GeneratedFile]  = []

    self.app_short_name  = app_short_name
    self.app_long_name   = app_long_name


    self.webmanifest = {}
    if self.app_long_name:
       self.webmanifest['name'] = self.app_long_name
    elif self.app_short_name:
       self.webmanifest['name'] = self.app_short_name

    if self.app_short_name:
       self.webmanifest['short_name'] = self.app_short_name

    self.webmanifest['display'] = 'standalone'
    self.webmanifest['icons'] = []





    if theme_color is not None:
       self.elements.append(meta('theme-color', theme_color))
       self.webmanifest['theme_color'] = theme_color

    if background_color is not None:
       self.webmanifest['background_color'] = background_color

    if favicon_48x48 is not None:
       self.elements.append(HtmlElement(tag='link', attributes={
                'rel':'icon',
                'type':'image/png',
                'href':favicon_48x48,
                'sizes':'48x48'
            }))

    if favicon_svg is not None:
       self.elements.append(HtmlElement(tag='link', attributes={
                'rel':'icon',
                'type':'image/svg+xml',
                'href':favicon_svg,
                'sizes':'48x48'
            }))
    if favicon_ico is not None:
       self.elements.append(HtmlElement(tag='link', attributes={
                'rel':'shortcut icon',
                'href':favicon_ico
            }))
    if favicon_apple_touch is not None:
        self.elements.append(HtmlElement(tag='link', attributes={
                'rel':'apple-touch-icon',
                'href':favicon_apple_touch,
                'sizes':'180x180'
            }))

    if self.app_short_name:
       self.elements.append(meta('apple-mobile-web-app-title', self.app_short_name))


    if favicon_192x192 is not None:
        self.webmanifest['icons'].append({
          'src': favicon_192x192,
          'sizes': '192x192',
          'type': 'image/png',
          'purpose': 'maskable'
          })

    if favicon_512x512 is not None:
       self.webmanifest['icons'].append({
          'src': favicon_512x512,
          'sizes': '512x512',
          'type': 'image/png',
          'purpose': 'maskable'
          })

    self.elements.append(HtmlElement(tag='link', attributes={
              'rel':'manifest',
              'href':'/site.webmanifest'
          }))
    self.files.add('site.webmanifest', self.generate_webmanifest)

  def get_elements(self):
     return self.elements
  def get_files(self):
     return self.files

  def generate_webmanifest(self):
    return json.dumps(self.webmanifest)
