__author__ = 'Chapin Bryce'
__version__ = 0.00

import os
import datetime
import logging

#
# Main function. Callable by other scripts
#

base = os.path.dirname(os.path.realpath(__file__))


def main(outpath, targ, rule, os_type, config):
    start = datetime.datetime.now()

    if not os.path.exists(outpath):
        os.makedirs(outpath)

    logging.basicConfig(filename=outpath + '/lcdic.log',
                        level=logging.DEBUG,
                        format='%(asctime)s | %(levelname)s | %(message)s')

    case = config['case_number']
    eid = config['eid']
    examiner = config['name']
    targeted_user = config['target_users']
    d = config['d']
    extensions = config['extensions']
    ext_for_users = config['ext_for_users']

    # Enable STDOUT Printing for debug
    if d:
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

    logging.info('Start of collection')
    logging.info('Case Number: ' + case)
    logging.info('Evidence Number: ' + eid)
    logging.info('Examiner Name: ' + examiner)
    logging.info('Evidence: ' + targ)
    logging.info('Output directory: ' + outpath)
    logging.info('Configuration File: ' + config['config_path'])
    logging.info('Yara Rule: ' + rule)

    from collectors import windows
    from collectors import debian
    from collectors import search

    coll = None

    # Create Object
    if os_type == 'winxp':
        coll = windows.WinXP()
        logging.info('Collection of Windows XP Initialized')
    elif os_type == 'win7':
        coll = windows.Win7()
        logging.info('Collection of Windows 7 Initialized')
    elif os_type == 'ubu13':
        coll = debian.Ubuntu13()
        logging.info('Collection of Ubuntu 13 Initialized')
    else:
        raise UserWarning('Invalid OS Selected')

    # Initialize Class Items based on input
    coll.targ = targ
    coll.case = case
    coll.eid = eid
    coll.dest = outpath
    coll.hashtype = config['hashtype']
    if targeted_user:
        coll.target_user = targeted_user
    if extensions:
        coll.extensions = extensions
        coll.ext_for_users = ext_for_users
    coll.setup()

    # Call methods
    paths_to_process = coll.collector()

    # Add in Yara
    if rule:
        logging.info('Yara Searching Started')
        ysearch = search.YaraSearch(rule, targ)
        rules = ysearch.run()
        logging.info('Yara Searching Completed')
        for r in rules:
            paths_to_process.append(r['file'])

    logging.info("Creation of TarBall and Hashing started")
    coll.complete_collection(paths_to_process)
    logging.info("Creation of TarBall and Hashing completed")
    end = datetime.datetime.now()
    logging.info('Run time: ' + str(end - start))
    logging.info("LCDI Collector Completed")

#
# End of Main Function
#

#
# Start parsing for __main__ script
#


def _argparse():
    """
    Parse Args & return object
    :return:
    """
    import argparse

    parser = argparse.ArgumentParser(description='LCDI Collector, a script to automate targeted collections. '
                                                 'See config.ini to set optional information and configurations',
                                     version=__version__, epilog='Created by ' + __author__)

    parser.add_argument('targ', metavar='C:', help="Path to the root of the targeted volume")
    parser.add_argument('dest', metavar='/path/to/output', help="Path to the root of the output directory, "
                                                                "will create if it does not exist")
    parser.add_argument('os', metavar='list', help='Select OS. type `list` for list of supports OS\'s')
    parser.add_argument('-c', '--config', help='Path to custom config file. Default is config/config.ini',
                        default=base+'/config/config.ini')
    parser.add_argument('-r', '--rule', help='Yara Search Term (single string keyword) or Path to custom Yara rules '
                                             'file. Sample located in config/yara.rules', default='')
    return parser.parse_args()


def _config_parser(config):
    """
    Read configuration file into dictionary
    :param config: string path to configuration file
    :return: config dictionary
    """
    from ConfigParser import SafeConfigParser

    parser = SafeConfigParser()
    parser.read(config)
    parser_dict = dict()
    parser_dict['config_path'] = config
    parser_dict['case_number'] = parser.get('Options', 'case_number')
    parser_dict['eid'] = parser.get('Options', 'eid')
    parser_dict['name'] = parser.get('Options', 'name')
    parser_dict['extensions'] = parser.get('Options', 'extensions').split(',')
    parser_dict['target_users'] = parser.get('Options', 'target_users').split(',')
    parser_dict['d'] = parser.getboolean('Options', 'd')
    parser_dict['ext_for_users'] = parser.getboolean('Options', 'ext_for_users')
    parser_dict['hashtype'] = parser.get('Options', 'hashtype')

    return parser_dict

#
# Start Main Program
#

if __name__ == '__main__':
    args = _argparse()

    if args.config:
        config = _config_parser(args.config)
    else:
        raise 'Config File not found. Please specify or replace the deafult'

    # init vars
    os_type = ''
    coll = None
    outpath = ''

    # Convert OS to Process
    # TODO Have a method to auto-determine OS of evidence
    supported_os = {'win7': 'Windows 7', 'winxp': 'Windows XP', 'ubu13': 'Ubuntu 13'}
    if args.os.lower() in supported_os.keys():
        os_type = args.os.lower()
    elif args.os.lower() == 'list':
        print 'OS Name'.ljust(20) + 'Name to supply'
        for os in supported_os.keys():
            print supported_os[os].ljust(20) + os
        quit()
    else:
        print('Invalid Arguments: Select from list below')
        print 'OS Name'.ljust(20) + 'Name to supply'
        for os in supported_os.keys():
            print supported_os[os].ljust(20) + os
        quit()

    outpath = os.path.join(args.dest, config['case_number'])

    main(outpath, args.targ, args.rule, os_type, config)





