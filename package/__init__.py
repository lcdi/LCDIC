__author__ = 'cbryce'
__license__ = ''
__date__ = ''
__version__ = ''

import os
import tarfile
import progressbar

class tarPackage(object):

    def __init__(self, dest, eid, hashtype):
        self.dest = dest
        self.eid = eid
        self.hashtype = hashtype

    def package(self, files):
        """
        Iterate through paths to package up
        :param files: list of string paths to directories and files
        :return:
        """

        # TODO try to load files into memory to avoid having to read them twice across the wire

        import datetime
        hashlog = open(self.dest + '/hashlist.txt', 'w')

        pbar = progressbar.ProgressBar(widgets=[progressbar.Bar('+'), ' ', progressbar.Percentage(), ' ',
                                                progressbar.ETA(), ' ', progressbar.SimpleProgress(),
                                                ' locations complete'],
                                       maxval=len(files))
        p = 0

        hashlog.write('Time'.ljust(31) + self.hashtype.upper().ljust(45) + 'File Path\n')
        try:
            with tarfile.open(self.dest + '/' + self.eid + '.tar', mode='w', dereference=False) as temp_tar:
                pbar.start()
                for entry in files:
                    p += 1
                    pbar.update(p)
                    if os.path.isdir(entry):
                        for root, dirs, files in os.walk(entry):
                            for f in files:
                                fname = os.path.join(root, f)
                                try:
                                    hasher = self.hash(open(fname, 'rb').read())
                                except IOError, e:
                                    hasher = 'Could Not Process'
                                hashlog.write(str(datetime.datetime.now()).ljust(31) + str(hasher).ljust(45) + fname + '\n')
                                if not os.path.islink(fname):
                                    temp_tar.add(fname)
                                else:
                                    print 'Link File excluded: ' + fname

                    elif os.path.isfile(entry):
                        try:
                            hasher = self.hash(open(entry, 'rb').read())
                        except IOError, e:
                            hasher = 'Could Not Process'
                        hashlog.write(str(datetime.datetime.now()).ljust(31) + str(hasher).ljust(45)
                                      + entry + '\n')
                        temp_tar.add(entry)
                    hashlog.flush()
                pbar.finish()
            hashlog.close()
            temp_tar.close()
        except IOError, e:
            import datetime

            self.eid = str(datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S'))
            print 'Tar File IO Error; Likely open. Writing to: ' + self.eid
            self.package(files)

        return self.dest + '/' + self.eid + '.tar'

    def hash(self, data):
        """
        Hash data stream
        :param data: stream of data
        :return: hexdigest of data stream
        """
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
