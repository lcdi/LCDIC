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
        :param drive: str path to drive to process. Should be single letter!
        :param output: str path to output directory.
        :param config: dict of configuration. See sample config file for options
        :return: None
        """
        self.drive = drive
        self.output = output
        self.config = config

        if not os.path.exists(self.output):
            os.makedirs(self.output)

    def start_collection(self):
        pass

    def init_logger(self, debug=False):
        """
        Set up logger
        :param d: bool to enable debugging (aka print logging to screen) and increase log level
        :return: None
        """

        if debug:
            level = logging.DEBUG
        else:
            level = logging.WARNING
        logging.basicConfig(level=level, filename=os.path.join(self.output, 'run.log'),
                            format='%(asctime)s | %(levelname)s | %(message)s', filemode='w')

        # Add ability to read log in STDOUT
        if debug:
            console = logging.StreamHandler()
            console.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
            console.setFormatter(formatter)
            logging.getLogger('').addHandler(console)

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--drive', help='Drive to collect data from. Must be letter only', type=str,
                        required=True)
    parser.add_argument('-o', '--output', help='Output Directory to write content to', type=str, required=True)
    parser.add_argument('-p', '--platform', help='Platform to process', type=str, default='list')
    parser.add_argument('-c', '--config', help='Path to config file to use', type=str, default=None)
    parser.add_argument('--debug', help='Enable debuggin', action='store_true')
    args = parser.parse_args()

    if args.platform == 'list':
        print 'Platform Name'.rjust(14) + ' | Platform Description'
        print '---------------|--------------------'
        for key in available_platforms:
            print key.rjust(14) + ' | ' + available_platforms[key]['desc']

    if args.config:
        pass  # TODO add config parser
    else:
        config = dict()
        case_id = random.randint(000, 200)
        eid = random.randint(00, 99)
        now = datetime.datetime.today()

        # Generate a case number with today's date and a random case number
        config['case_number'] = 'FI-' + (now.strftime('%Y%M%d')) + '-' + str(case_id)
        config['evidence_number'] = str(case_id) + '-HD-' + str(eid)
        config['examiner_name'] = 'LCDIExaminer'

        # Set default collection parameters to be broad
        config['enable_user_collection'] = True
        config['collect_all_users_appdata'] = True
        config['collect_all_users_ntuser'] = True

    # Start autoTriage
    main = autoTriage(args.drive, args.output, config)
    main.init_logger(args.debug)
