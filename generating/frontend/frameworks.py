
from enum import Enum, auto
from generating.frontend.icons.icon_pack import IconPack


class FrontendFrameworks(Enum):
    VANILLA_JS_AJAX   = auto()
    REACT             = auto()
    VUE               = auto()
    QWIK              = auto()
    SVELTE            = auto()
    VANILLA_UI_KIT    = auto()
    VANILLA_BOOTSTRAP = auto()

    _icon_packs = {}

    def __add__(self, icon_pack):
        if isinstance(icon_pack, IconPack):
            FrontendFrameworks._icon_packs[self] = icon_pack
        return self

    def getIconPack(self):
        return FrontendFrameworks._icon_packs.get(self, None)
