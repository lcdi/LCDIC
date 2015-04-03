__author__ = 'cbryce'

import re


def cc():
    if not easygui.ccbox('Would you like to continue?'):
        quit()


if __name__ == '__main__':
    import easygui
    import lcdic

    # Get case information
    msg = 'Enter Case Information'
    title = 'Case Data'
    fieldnames = ['Case Number', 'Evidence ID', 'Examiner Name']
    fieldvalues = []
    fieldvalues = easygui.multenterbox(msg, title, fieldnames, fieldvalues)

    if not fieldvalues:
        cc()
    else:
        while 1:
            if fieldvalues == None:
                break

            errmsg = ''
            for i in fieldvalues:
                if i.strip() == "":
                    errmsg = '"%s" is a required field.' % fieldnames[i]

            case_pattern = '(FI|DR|RD)-[0-9]{8}-[0-9]{1,4}'
            if not re.search(case_pattern, fieldvalues[0]):
                errmsg = 'Case Name is not the correct format'

            evidnce_pattern = '[0-9]{1,4}-(HD|FM|SD|MD|PC|LT|EX|OM|EB|TC|RA|EA)-[0-9]{1,3}'
            if not re.search(evidnce_pattern, fieldvalues[1]):
                errmsg = 'Evidence ID is not in the correct format'

            if errmsg == '':
                break
            else:
                fieldvalues = easygui.multenterbox(errmsg, msg, fieldnames, fieldvalues)
    if not fieldvalues:
        cc()

    # Get mount point
    targ = easygui.diropenbox('Target Drive Selection', 'Select Evidence Mount Point', '')

    if not targ:
        cc()
    else:
        while 1:
            if targ:
                break
            else:
                targ = easygui.diropenbox('Target Drive Selection', 'Select Evidence Mount Point', '')

    # Get output directory
    dest = easygui.diropenbox('Output Location Selection', 'Select Output Directory', '')

    if not dest:
        cc()
    else:
        while 1:
            if dest:
                break
            else:
                dest = easygui.diropenbox('Output Location Selection', 'Select Output Directory', '')

    # Select OS_Type
    choices = ['WinXP', 'Win7', 'Ubu13']
    os_type = easygui.buttonbox('Evidence OS Selection', 'Select the Evidence Operating System', choices)

    if not fieldvalues:
        cc()
    else:
        while 1:
            if os_type:
                break
            else:
                os_type = easygui.buttonbox('Evidence OS Selection', 'Select the Evidence Operating System', choices)

    lcdic.main(dest, targ, os_type.lower(), fieldvalues[0], fieldvalues[1], fieldvalues[2])
