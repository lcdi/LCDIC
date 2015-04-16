__author__ = 'cbryce'
__license__ = ''
__date__ = ''
__version__ = ''

import os


class Base(object):
    """
    Base class for Windows Collections
    """
    def __init__(self):
        self.user_dir_base = ''
        self.appdata_location = ''
        self.system_users = ''
        self.users = []

    def find_users(self):
        """
        Iterates through self.user_dir_base to find all users
        :return:
        """
        for x, user, y in os.walk(self.user_dir_base):
            self.users.append(user)

    def collect_ntuser_paths(self):
        """
        Collect paths to appdata for discovered users
        :return: list of paths
        """
        path = []
        for user in self.users:
            path.append(os.path.join(self.user_dir_base, user, self.appdata_location))
        return path