from generating.frontend.icons.icon import Icon
from generating.frontend.icons.icon_pack import IconPack


class UIKitIconPack(IconPack):
    @staticmethod
    def translate_icon(icon):
        icon_classes = {
            Icon.HOME: 'uk-icon-home',
            Icon.USER: 'uk-icon-user',
            Icon.SETTINGS: 'uk-icon-cog',
            Icon.NOTIFICATIONS: 'uk-icon-bell',
            Icon.SEARCH: 'uk-icon-search',
            Icon.MAIL: 'uk-icon-envelope',
            Icon.CHAT: 'uk-icon-comments',
            Icon.HELP: 'uk-icon-question-circle',
            Icon.LOGOUT: 'uk-icon-sign-out',
            Icon.DASHBOARD: 'uk-icon-dashboard',
            Icon.PROFILE: 'uk-icon-id-badge',
            Icon.CALENDAR: 'uk-icon-calendar',
            Icon.UPLOAD: 'uk-icon-upload',
            Icon.DOWNLOAD: 'uk-icon-download'
            # Add more mappings as needed
        }
        return icon_classes.get(icon, '')
