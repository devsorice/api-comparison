class IconPack:
    def translate_icon(self, icon, style:str=''):
        raise NotImplementedError("This method should be overridden by subclasses")

    def load(self, page):
        raise NotImplementedError("This method should be overridden by subclasses")
