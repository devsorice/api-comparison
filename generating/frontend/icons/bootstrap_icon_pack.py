from generating.frontend.icons.icon import Icon
from generating.frontend.icons.icon_pack import IconPack


class BootstrapIconPack(IconPack):
    @staticmethod
    def translate_icon(icon):
        icon_classes = {
            Icon.HOME: 'bi-house',
            Icon.USER: 'bi-person',
            Icon.SETTINGS: 'bi-gear',
            Icon.NOTIFICATIONS: 'bi-bell',
            Icon.SEARCH: 'bi-search',
            Icon.MAIL: 'bi-envelope',
            Icon.CHAT: 'bi-chat',
            Icon.HELP: 'bi-question-circle',
            Icon.LOGOUT: 'bi-box-arrow-right',
            Icon.DASHBOARD: 'bi-speedometer2',
            Icon.PROFILE: 'bi-person-badge',
            Icon.CALENDAR: 'bi-calendar',
            Icon.UPLOAD: 'bi-cloud-upload',
            Icon.DOWNLOAD: 'bi-cloud-download'
            # Add more mappings as needed
        }
        return icon_classes.get(icon, '')
