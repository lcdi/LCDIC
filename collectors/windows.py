__author__ = 'cbryce'
__version__ = 0.00

import os
import logging

from .base import CollectorBase


class WinXP(CollectorBase):
    """
    Collector Class for the
    """

    def __init__(self):
        super(WinXP, self).__init__()

        self.name = 'Windows XP Collector'
        self.description = 'Collection of artifacts found in Windows XP'

        self.user_path = '\\Documents and Settings\\'
        self.registry_config = '\\WINDOWS\\system32\\config\\'

        self.app_data_location = '\\Application Data'
        self.users = []

    def setup(self):
        self.user_path = self.targ + self.user_path
        self.registry_config = self.targ + self.registry_config
        self.users = []

    def collector(self):
        """
        Run collection
        :return:
        """
        logging.info('Collection of Users and their AppData started')
        app = self.collect_appdata().values()
        logging.info('Collection of Users and their AppData completed')

        logging.info("Collection of registry and NTUSER.DATs started")
        reg = self.collect_registry().values()
        logging.info("Collection of registry and NTUSER.DATs completed")

        logging.info("Collection of File System artifacts started")
        self.collect_fs_data()  # Nothing to extract
        logging.info("Collection of File System artifacts completed")

        logging.info("Collection of USB artifacts started")
        usb = self.collect_usb().values()
        logging.info("Collection of USB artifacts completed")

        if self.target_user and self.extensions:
            logging.info("Collection of User Document artifacts started")
            for user in self.users:
                if user in self.target_user:
                    # collect all data from this user
                    docs = self.collect_docs()
                else:
                    docs = []
            logging.info("Collection of User Document artifacts completed")

        # Append data to paths
        paths = []
        for i in app:
            paths.append(i)
        for i in reg:
            paths.append(i)
        for i in usb:
            paths.append(i)
        for i in docs:
            paths.append(i)

        return paths

    def collect_appdata(self):
        """
        Browse all accounts and collect appdata
        :return: list of dictionary of users and the appdata paths
        """
        # Collect all user names
        # TODO: Allow specification of specific user name(s)
        user_dict = {}

        for user in os.listdir(self.user_path):
            if os.path.isdir(self.user_path + user):
                user_dict[user] = self.user_path + user + self.app_data_location
        self.users = user_dict.keys()

        return user_dict

    def collect_registry(self):
        """
        Browse all accounts and collect NTUSER
        :return: list of dictionary of users and the appdata paths
        """

        # Collect for System32/Config
        reg_hives = ['sam', 'software', 'system', 'security']
        reg_dict = dict()
        for entry in os.listdir(self.registry_config):
            if os.path.isfile(self.registry_config + entry):
                for hive in reg_hives:
                    if entry.lower() == hive:
                        reg_dict[hive] = self.registry_config + entry

        for user in self.users:
            if os.path.isfile(self.user_path + user + '\\NTUSER.DAT'):
                reg_dict[user] = self.user_path + user + '\\NTUSER.DAT'

        return reg_dict

    def collect_mem(self):
        pass

    def collect_fs_data(self):
        """
        Collect data from file system for parsing
        :return: dictionary of paths to file system data
        """
        # TODO Add in ability to zip extracted files
        import subprocess

        fsdata = dict()

        if not os.path.exists(os.path.join(os.path.abspath(self.dest), 'filesystem_artifacts')):
            os.makedirs(os.path.join(os.path.abspath(self.dest), 'filesystem_artifacts'))

        fsdata['MFT'] = self.targ + '0'
        fsdata['LogFile'] = self.targ + '2'
        # fsdata['USN'] = self.targ + '\\$Extend\\$UsnJrnl' ## Not in WinXP

        from lcdic import base

        for key in fsdata.keys():
            try:
                cmd = base+'\\libs\\RawCopy\\RawCopy64.exe ' + fsdata[key] + ' ' + os.path.join(os.path.abspath(self.dest), 'filesystem_artifacts') + ' -AllAttr'
                subprocess.call(cmd, shell=True)
            except Exception, e:
                logging.warning('Could not extract $MFT using 64bit tool...Trying 32bit...')
                try:
                    cmd = base+'\\libs\\RawCopy\\RawCopy.exe ' + fsdata[key] + ' ' + os.path.join(os.path.abspath(self.dest), 'filesystem_artifacts') + ' -AllAttr'
                    subprocess.call(cmd, shell=True)
                except Exception, e:
                    logging.error('Could not Extract ' + key + '!')

        return None

    def collect_usb(self):
        """
        Collects the data needed for USB information
        :return: dictionary of usb logs
        """

        usb_logs = dict()
        usb_logs['setupapi'] = self.targ + '/Windows/setupapi.log'
        return usb_logs

    def complete_collection(self, paths):
        self._tarball(paths)

    def collect_docs(self):

        self.doc_array = list()

        # Collect data from specified users
        if self.extensions and self.ext_for_users:
            for user in self.target_user:
                for root, dirs, files in os.walk(self.user_path + user):
                    for entry in files:
                        if os.path.splitext(entry)[-1].strip('.') in self.extensions:
                            self.doc_array.append(os.path.join(root + '/' + entry))

        # Collect data from all users
        elif self.extensions and not self.ext_for_users:
            for user in self.users:
                for root, dirs, files in os.walk(self.user_path + user):
                    for entry in files:
                        if os.path.splitext(entry)[-1].strip('.') in self.extensions:
                            self.doc_array.append(os.path.join(root + '/' + entry))

        return self.doc_array


class Win7(CollectorBase):
    """
    Collector Class for the
    """

    def __init__(self):
        super(Win7, self).__init__()

        self.name = 'Windows 7 Collector'
        self.description = 'Collection of artifacts found in Windows 7'

        self.user_path = '\\Users\\'
        self.registry_config = '\\WINDOWS\\system32\\config\\'

        self.app_data_location = '\\AppData'
        self.users = []

    def setup(self):
        self.user_path = self.targ + self.user_path
        self.registry_config = self.targ + self.registry_config
        self.users = []

    def collector(self):
        logging.info('Collection of Users and their AppData started')
        app = self.collect_appdata().values()
        logging.info('Collection of Users and their AppData completed')
        logging.info("Collection of registry and NTUSER.DATs started")
        reg = self.collect_registry().values()
        logging.info("Collection of registry and NTUSER.DATs completed")

        logging.info("Collection of File System artifacts started")
        # fs = self.collect_fs_data()
        fs = []
        logging.info("Collection of File System artifacts completed")

        logging.info("Collection of USB artifacts started")
        usb = self.collect_usb().values()
        logging.info("Collection of USB artifacts completed")

        if self.extensions:
            logging.info("Collection of file extensions artifacts started")
            if self.ext_for_users and self.target_user:
                for user in self.users:
                    if user in self.target_user:
                        # collect all data from this user
                        docs = self.collect_docs()
            else:
                # Collect files matching extension on any location of system
                docs = self.collect_docs()
            logging.info("Collection of file extensions artifacts completed")

        paths = []
        for i in app:
            paths.append(i)
        for i in reg:
            paths.append(i)
        for i in usb:
            paths.append(i)
        for i in docs:
            paths.append(i)
        for i in fs:
            paths.append(i)

        return paths

    def collect_appdata(self):
        """
        Browse all accounts and collect appdata
        :return: list of dictionary of users and the appdata paths
        """
        # Collect all user names
        # TODO: Allow specification of specific user name(s)
        user_dict = {}
        for user in os.listdir(self.user_path):
            if os.path.isdir(self.user_path + user):
                user_dict[user] = self.user_path + user + self.app_data_location
        self.users = user_dict.keys()

        return user_dict

    def collect_registry(self):
        """
        Browse all accounts and collect NTUSER
        :return: list of dictionary of users and the appdata paths
        """

        # Collect for System32/Config
        reg_hives = ['sam', 'software', 'system', 'security']
        reg_dict = dict()
        for entry in os.listdir(self.registry_config):
            if os.path.isfile(self.registry_config + entry):
                for hive in reg_hives:
                    if entry.lower() == hive:
                        reg_dict[hive] = self.registry_config + entry

        for user in self.users:
            if os.path.isfile(self.user_path + user + '\\NTUSER.DAT'):
                reg_dict[user] = self.user_path + user + '\\NTUSER.DAT'

        return reg_dict

    def collect_mem(self):
        pass

    def collect_usb(self):
        """
        Collects the data needed for USB information
        :return: dictionary of usb logs
        """

        usb_logs = dict()
        usb_logs['setupapiapp'] = self.targ + '/Windows/inf/setupapi.app.log'
        usb_logs['setupapidev'] = self.targ + '/Windows/inf/setupapi.dev.log'

        return usb_logs

    def collect_fs_data(self):
        """
        Collect data from file system for parsing
        :return: dictionary of paths to file system data
        """
        # TODO Add in ability to zip extracted files
        import subprocess

        fsdata = dict()

        if not os.path.exists(os.path.join(os.path.abspath(self.dest), 'filesystem_artifacts')):
            os.makedirs(os.path.join(os.path.abspath(self.dest), 'filesystem_artifacts'))

        fsdata['MFT'] = self.targ + '0'
        fsdata['LogFile'] = self.targ + '2'

        from lcdic import base  # import base variable, not base module!
        from libs import pyads

        j = pyads.ADS(self.targ + '\\$Extend\\$UsnJrnl:$J')
        if len(j.getStreams()):  # if a stream is detected, copy it out. reads entire journal into RAM, may cause issues
            j.extractStream('', outfile=os.path.join(os.path.abspath(self.dest), 'filesystem_artifacts', 'USN_$J'))
            logging.info('Completed USN Journal Extraction')

        for key in fsdata.keys():
            try:
                cmd = base+'\\libs\\RawCopy\\RawCopy64.exe ' + fsdata[key] + ' ' + os.path.join(os.path.abspath(self.dest), 'filesystem_artifacts') + ' -AllAttr'
                subprocess.check_output(cmd, shell=True)
            except Exception, e:
                logging.warning('Could not extract $MFT using 64bit tool...Trying 32bit...')
                try:
                    cmd = base+'\\libs\\RawCopy\\RawCopy.exe ' + fsdata[key] + ' ' + os.path.join(os.path.abspath(self.dest), 'filesystem_artifacts') + ' -AllAttr'
                    subprocess.check_output(cmd, shell=True)
                except Exception, e:
                    logging.error('Could not Extract ' + key + '!')
            logging.info('Completed ' + key + ' Extraction')




        return {'path': os.path.join(os.path.abspath(self.dest), 'filesystem_artifacts')}

    def collect_docs(self):
        self.doc_array = list()

        # Collect data from specified users
        if self.extensions and self.ext_for_users:
            for user in self.target_user:
                for root, dirs, files in os.walk(self.user_path + user):
                    for entry in files:
                        if os.path.splitext(entry)[-1].strip('.') in self.extensions:
                            self.doc_array.append(os.path.join(root + '/' + entry))

        # Collect data from all users
        elif self.extensions and not self.ext_for_users:
            for user in self.users:
                for root, dirs, files in os.walk(self.user_path + user):
                    for entry in files:
                        if os.path.splitext(entry)[-1].strip('.') in self.extensions:
                            self.doc_array.append(os.path.join(root + '/' + entry))

        return self.doc_array

    def complete_collection(self, paths):
        self._tarball(paths)
