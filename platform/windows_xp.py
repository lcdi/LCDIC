__author__ = 'cbryce'
__license__ = ''
__date__ = ''
__version__ = ''

from platform.windows_base import Base

class WinXP():
    def __init__(self):
        pass

class Factory():
    def platform_name(self):
        return 'winxp'
    def platform_description(self):
        return 'Process Windows XP'
    def platform_class(self):
        return WinXP