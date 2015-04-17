__author__ = 'cbryce'
__license__ = ''
__date__ = ''
__version__ = ''

from platform.windows_base import Base


class Win7(Base):
    def __init__(self):
        """

        :return:
        """
        super(Win7, self).__init__()

        self.user_dir_base = r'\Users'
        self.appdata_location = r'\AppData'
        self.system_users = ['All Users', 'Default', 'Default User', 'Public']


class Factory():
    def platform_name(self):
        return 'win7'

    def platform_description(self):
        return 'Process Windows 7'

    def platform_class(self):
        return Win7