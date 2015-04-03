__author__ = 'cbryce'

import os
import logging


class CollectorBase(object):
    """
    Base Class for all collectors, allowing them to share the collection methods
    """

    def __init__(self):
        self.targ = ''
        self.dest = ''
        self.case = ''
        self.eid = ''
        self.target_user = ''
        self.extensions = ''
        self.ext_for_users = False
        self.hashtype = ''

    def _hasher(self, data):
        import hashlib

        if self.hashtype == 'sha1':
            h = hashlib.sha1()
        elif self.hashtype == 'sha256':
            h = hashlib.sha256()
        elif self.hashtype == 'sha512':
            h = hashlib.sha512()
        elif self.hashtype == 'md5':
            h = hashlib.md5()
        else:
            quit()

        h.update(data)
        return h.hexdigest()

    def _tarball(self, files):
        """
        Compresses file and returns the file path to the tar file
        """

        import tarfile
        import datetime

        hashlog = open(self.dest + '/hashlist.txt', 'w')

        hashlog.write('Time'.ljust(31) + self.hashtype.upper().ljust(45) + 'File Path\n')
        with tarfile.open(self.dest + '/' + self.eid + '.tar', mode='w', dereference=False) as temp_tar:
            for entry in files:
                if os.path.isdir(entry):
                    for root, dirs, files in os.walk(entry):
                        for f in files:
                            fname = os.path.join(root, f)
                            try:
                                hasher = self._hasher(open(fname, 'rb').read())
                            except IOError, e:
                                hasher = 'Could Not Process'
                            hashlog.write(str(datetime.datetime.now()).ljust(31) + str(hasher).ljust(45)
                                          + fname + '\n')
                            if not os.path.islink(fname):
                                temp_tar.add(fname)
                            else:
                                logging.warning('Link File excluded: ' + fname)
                elif os.path.isfile(entry):
                    try:
                        hasher = self._hasher(open(entry, 'rb').read())
                    except IOError, e:
                        hasher = 'Could Not Process'
                    hashlog.write(str(datetime.datetime.now()).ljust(31) + str(hasher).ljust(45)
                                  + entry + '\n')
                    temp_tar.add(entry)

        hashlog.close()
        temp_tar.close()

        return self.dest + '/' + self.eid + '.tar'
