from generating.frontend.icons.icon import Icon
from generating.frontend.icons.icon_pack import IconPack


class FeatherIconPack(IconPack):
    @staticmethod
    def translate_icon(icon):
        icon_classes = {
            Icon.HOME: 'feather-icon-home',
            Icon.USER: 'feather-icon-user',
            Icon.SETTINGS: 'feather-icon-settings',
            Icon.NOTIFICATIONS: 'feather-icon-bell',
            Icon.SEARCH: 'feather-icon-search',
            Icon.MAIL: 'feather-icon-mail',
            Icon.CHAT: 'feather-icon-message-circle',
            Icon.HELP: 'feather-icon-help-circle',
            Icon.LOGOUT: 'feather-icon-log-out',
            Icon.DASHBOARD: 'feather-icon-grid',
            Icon.PROFILE: 'feather-icon-user-check',
            Icon.CALENDAR: 'feather-icon-calendar',
            Icon.UPLOAD: 'feather-icon-upload',
            Icon.DOWNLOAD: 'feather-icon-download'
            # Add more mappings as needed
        }
        return icon_classes.get(icon, '')
