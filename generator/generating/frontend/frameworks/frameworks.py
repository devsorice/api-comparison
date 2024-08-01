
from enum import Enum, auto
from typing import List
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


class FrontendFramework:
    def __init__(self, framework:FrontendFrameworks, icon_pack:IconPack=None, libraries:List[FrontendLibraries]=[]):
        self.framework = framework
        self.icon_pack = icon_pack
        self.libraries = libraries

    def get_icon_pack(self):
        return self.icon_pack

    def get_libraries(self):
        return self.libraries


    def get_frontend(self):
        return self.framework
