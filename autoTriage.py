__author__ = 'cbryce'
__license__ = ''
__date__ = ''
__version__ = ''

"""
autoTriage - Triage Collection Tool
Copyright (C) 2015  LCDI

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import logging
import os
import datetime
import random
from platform import *
from package import *

available_platforms = dict()
available_platforms['winxp'] = {'desc': 'Windows XP', 'obj': windows_xp.WinXP}
available_platforms['win7'] = {'desc': 'Windows 7', 'obj': windows_7.Win7}


class autoTriage():
    """
    Class to start autoTriage
    """
    def __init__(self, drive, output, config):
        """
        Setup
        :param drive: str path to drive to process. Should be single letter with colon!
        :param output: str path to output directory.
        :param config: dict of configuration. See sample config file for options
        :return: None
        """

        if not isinstance(drive, str):
            raise 'Target Drive is invalid type. Should be a string'

        if not isinstance(output, str):
            raise 'Output folder is invalid type. Should be a string'
        elif os.path.exists(output) and not os.path.isdir(output):
            raise 'Output path is not a folder. Should be a directory'

        if not isinstance(config, dict):
            raise 'Target Drive is invalid type. Should be a string'

        self.drive = drive
        self.output = output
        self.config = config
        self.platform = None
        self.log = None
        self.os = None

    def check_directories(self):
        """
        Validate input and create output directories
        :return:
        """

        # Check input
        if not os.path.exists(self.drive):
            raise 'Target drive not found. Please verify your inputs'

        # Create output
        if not os.path.exists(os.path.join(self.output, self.config['case_number'])):
            os.makedirs(os.path.join(self.output, self.config['case_number']))

    def assign_platform(self, p=None):
        """
        :param p: str platform of the target
        :return: None
        """

        if p:
            if p in available_platforms.keys():
                self.platform = available_platforms[p]['obj']
            else:
                raise 'Platform not supported. Verify your command line input'
        else:
            if 'platform' not in self.config.keys():
                raise 'Please provide platform in configuration dictionary'

            if config['platform'] in available_platforms.keys():
                self.platform = available_platforms[self.config['platform']]['obj']
            else:
                raise 'Platform not supported. Verify your command line input'

        if not self.platform:
            raise 'No platform provided. Please validate your input'

        # Init OS
        self.os = self.platform()

    def run(self):
        """
        Run all steps in 1 method
        :return:
        """
        self.pre_collection()
        self.start_collection()
        self.finish_collection()

    def pre_collection(self):
        """
        Run steps needed prior to collection
        :return:
        """
        # Validate input
        self.check_directories()

    def start_collection(self):
        """
        Begin collection
        :return:
        """
        self.os.drive = self.drive
        self.os.find_users()
        if self.config['enable_user_collection'] is True:
            self.os.process_users(self.config)
        pass

    def finish_collection(self):
        """
        Complete collection
        :return:
        """
        gather = tarPackage(os.path.join(self.output, config['case_number']), config['evidence_number'],
                            config['hash_type'])
        gather.package(self.os.paths)
        pass

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--drive', help='Drive to collect data from. ie: D: ', type=str,
                        required=True)
    parser.add_argument('-o', '--output', help='Output Directory to write content to', type=str, required=True)
    parser.add_argument('-p', '--platform', help='Platform to process', type=str, default='list')
    parser.add_argument('-c', '--config', help='Path to config file to use', type=str, default=None)
    parser.add_argument('--debug', help='Enable debugging', action='store_true')
    args = parser.parse_args()

    if args.platform == 'list':
        print 'Platform Name'.rjust(14) + ' | Platform Description'
        print '---------------|--------------------'
        for key in available_platforms:
            print key.rjust(14) + ' | ' + available_platforms[key]['desc']
        quit()

    if args.config:
        import ConfigParser
        parser = ConfigParser.SafeConfigParser()
        parser.read(args.config)

        config = dict()
        config['case_number'] = parser.get('Case Information', 'case_number')
        config['evidence_number'] = parser.get('Case Information', 'evidence_number')
        config['examiner_name'] = parser.get('Case Information', 'examiner_name')

        config['platform'] = parser.get('Script Options', 'platform')
        config['hash_type'] = parser.get('Script Options', 'hash_type')

        config['enable_user_collection'] = parser.getboolean('User Collection', 'enable_user_collection')
        config['collect_all_users_appdata'] = parser.getboolean('User Collection', 'collect_all_users_appdata')
        config['collect_all_users_ntuser'] = parser.getboolean('User Collection', 'collect_all_users_ntuser')
    else:
        config = dict()
        case_id = random.randint(000, 200)
        eid = random.randint(00, 99)
        now = datetime.datetime.today()

        # Generate a case number with today's date and a random case number
        config['case_number'] = 'FI-' + (now.strftime('%Y%M%d')) + '-' + str(case_id)
        config['evidence_number'] = str(case_id) + '-HD-' + str(eid)
        config['examiner_name'] = 'LCDIExaminer'

        if not args.platform:
            raise 'No platform specified. Please add to arguments'
        config['platform'] = args.platform
        config['hash_type'] = 'md5'  # By Default

        # Set default collection parameters to be broad
        config['enable_user_collection'] = True
        config['collect_all_users_appdata'] = True
        config['collect_all_users_ntuser'] = True

    # Start autoTriage
    at = autoTriage(args.drive, args.output, config)

    # Assign a platform
    at.assign_platform()  # Can be read from config['platform'] or passed to method (for library usage)

    # Start application rolling!
    # Can be simplified with at.run() which will run all three
    # To individualize the running of the data
    at.pre_collection()  # Perform preemptive actions
    at.start_collection()  # Start collection
    at.finish_collection()  # Complete collection
