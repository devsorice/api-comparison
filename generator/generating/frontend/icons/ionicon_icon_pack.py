from generating.frontend.icons.icon import Icon
from generating.frontend.icons.icon_pack import IconPack


class IoniconPack(IconPack):
    @staticmethod
    def translate_icon(icon, style:str=''):
        icon_classes = {
            Icon.HOME: 'ion-md-home',
            Icon.USER: 'ion-md-person',
            Icon.SETTINGS: 'ion-md-settings',
            Icon.NOTIFICATIONS: 'ion-md-notifications',
            Icon.SEARCH: 'ion-md-search',
            Icon.MAIL: 'ion-md-mail',
            Icon.CHAT: 'ion-md-chatboxes',
            Icon.HELP: 'ion-md-help-circle',
            Icon.LOGOUT: 'ion-md-log-out',
            Icon.DASHBOARD: 'ion-md-speedometer',
            Icon.PROFILE: 'ion-md-contact',
            Icon.CALENDAR: 'ion-md-calendar',
            Icon.UPLOAD: 'ion-md-cloud-upload',
            Icon.DOWNLOAD: 'ion-md-cloud-download'
            # Add more mappings as needed
        }
        return icon_classes.get(icon, '')
