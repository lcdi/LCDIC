__author__ = 'cbryce'

import os

from .base import CollectorBase


class Ubuntu13(CollectorBase):
    """
    Collect data from Ubuntu 13
    """

    def __init__(self):
        super(Ubuntu13, self).__init__()

        self.name = 'Ubuntu 13 Collector'
        self.description = 'Collection of artifacts found in Ubuntu 13'

        self.user_path = '/home/'
        self.app_data_location = '/.local'
        self.users = []

        self.etc = '/etc/'
        self.var_log = '/var/log/'

    def setup(self):

        self.user_path = self.targ + self.user_path
        self.users = []

        self.etc = self.targ + '/etc/'
        self.var_log = self.targ + '/var/log/'

    def collector(self):
        user = self.collect_user_data().values()
        config = self.collect_config_data()

        paths = []
        for i in user:
            paths.append(i)
        for i in config:
            paths.append(i)

        return paths

    def collect_user_data(self):
        """
        Browse all accounts and collect .local
        :return: list of dictionary of users and the .local paths
        """
        # Collect all user names
        # TODO: Allow specification of specific user name(s)
        user_dict = {}

        for user in os.listdir(self.user_path):
            if os.path.isdir(self.user_path + user):
                user_dict[user] = self.user_path + user + self.app_data_location
        self.users = user_dict.keys()

        return user_dict

    def collect_config_data(self):
        return [self.etc, self.var_log]

    def complete_collection(self, paths):
        self._tarball(paths)