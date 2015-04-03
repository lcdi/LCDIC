__author__ = 'cbryce'
__version__ = 0.00

import progressbar
import os
import yara


class YaraSearch():
    def __init__(self, custom_rule, target):
        self.custom_rule = custom_rule
        self.target = target

    def run(self):

        if os.path.isfile(self.custom_rule):
            rules = yara.compile(self.custom_rule)
        elif isinstance(self.custom_rule, str):
            rules = yara.compile(source=self.custom_rule)

        matches = []

        count = 0
        for root, dirs, files in os.walk(self.target):
            for entry in files:
                count += 1


        pbar = progressbar.ProgressBar(widgets=[progressbar.Bar('+'), ' ', progressbar.Percentage(), ' | ',
                                                progressbar.ETA(), ' | ', progressbar.SimpleProgress()],
                                       maxval=count).start()

        p = 0
        for root, dirs, files in os.walk(self.target+'\\'):
            for entry in files:
                p += 1
                pbar.update(p)
                e = os.path.join(root, entry)
                try:
                    m = rules.match(e)
                    if len(m) > 1:
                        pass
                    if m:
                        matches.append({'match': m, 'file': e})
                except Exception, err:
                    pass
        pbar.finish()
        return matches

if __name__ == '__main__':
    # To Run Tests
    YaraSearch('../config/yara.rules', 'F:')