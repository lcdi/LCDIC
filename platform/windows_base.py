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
        self.drive = None
        self.user_dir_base = ''
        self.appdata_location = ''
        self.system_users = ''
        self.users = []
        self.paths = []

    def find_users(self):
        """
        Iterates through self.user_dir_base to find all users
        :return:
        """
        for user in os.listdir(os.path.join(self.drive, self.user_dir_base)):
            if user not in self.system_users and os.path.isdir(os.path.join(self.drive, self.user_dir_base, user)):
                self.users.append(user)

    def collect_appdata_paths(self, specific=None):
        """
        Collect paths to appdata for discovered users
        :return: list of paths
        """
        if not specific:
            path = []
            for user in self.users:
                appdata = os.path.join(self.drive, self.user_dir_base, user)
                path.append(appdata + self.appdata_location)
            return path

    def collect_ntuser_paths(self, specific=None):
        """
        Collect paths to ntuser for discovered users
        :return: list of paths
        """
        if not specific:
            path = []
            for user in self.users:
                path.append(os.path.join(self.drive, self.user_dir_base, user, 'NTUSER.DAT'))  # TODO validate same case for WinXP!
            return path

    def process_users(self, config):
        """

        :return:
        """
        tmpList = []
        if config['collect_all_users_appdata'] is True:
            a = self.collect_appdata_paths()

        if config['collect_all_users_ntuser'] is True:
            b = self.collect_ntuser_paths()

        for data in a:
                self.paths.append(data)
        for data in b:
                self.paths.append(data)