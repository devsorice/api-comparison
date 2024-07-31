
from enum import Enum, auto
from generating.frontend.icons.icon_pack import IconPack
from generating.frontend.frameworks.libraries import FrontendLibraries


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
            FrontendFrameworks._icon_packs.value[self] = el
        if isinstance(el, FrontendLibraries):
            FrontendFrameworks._libraries.value[self] = FrontendFrameworks._libraries.value.get(self, [])
            FrontendFrameworks._libraries.value[self].append(el)
        return self

    def getIconPack(self):
        return FrontendFrameworks._icon_packs.value.get(self, None)

    def getLibraries(self):
        return FrontendFrameworks._libraries.value.get(self, None)
