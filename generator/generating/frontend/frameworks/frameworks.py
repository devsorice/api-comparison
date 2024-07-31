
from enum import Enum, auto
from generating.frontend.icons.icon_pack import IconPack
from generator.generating.frontend.frameworks.libraries import FrontendLibraries


class FrontendFrameworks(Enum):
    VANILLA_JS_AJAX   = auto()
    REACT             = auto()
    VUE               = auto()
    QWIK              = auto()
    SVELTE            = auto()
    VANILLA_UI_KIT    = auto()
    VANILLA_BOOTSTRAP = auto()

    _icon_packs = {}
    _libraries  = {}

    def __add__(self, el):
        if isinstance(el, IconPack):
            FrontendFrameworks._icon_packs[self] = el
        if isinstance(el, FrontendLibraries):
            FrontendFrameworks._libraries[self] = FrontendFrameworks._libraries.get(self, [])
            FrontendFrameworks._libraries[self].append(el)
        return self

    def getIconPack(self):
        return FrontendFrameworks._icon_packs.get(self, None)

    def getLibraries(self):
        return FrontendFrameworks._libraries.get(self, None)
