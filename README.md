Senator Patrick Leahy Center for Digital Investigations Collector
=====

LCDI Collector

Written by Chapin Bryce

# Usage

GUI:
`python lcdic_gui.py`

Command line:
`python lcdic.py E: \output\path --os [OS TYPE]`

# Dependencies

See `requirements.txt`

# Support

## Operating System Collections
- [x] Ubuntu (Tested on 13)
- [x] Windows 7
- [x] Windows XP

## Supported Features
- [x] Grab USB related files
- [x] Create file listing of collected files, the time, and the hash
- [x] Collect files based on file extensions
- [x] Allow the collection of specific users

### Potential Support
- [ ] User Selection
- [ ] Document Collection (See Below)
- [ ] Yara Searching
- [-] Copy out $MFT, $Logfile, $J - Cannot grab while partition is mounted
- [ ] Windows 10
- [ ] Windows 8
- [ ] Windows Vista
- [ ] Windows 98
- [ ] Windows 95
- [ ] OSX 10.9
- [ ] OSX 10.8
- [ ] OSX 10.7
- [ ] OSX 10.6
- [ ] OSX 10.5
- [ ] OpenSUSE
- [ ] Debian
- [ ] OpenBSD
- [ ] CentOS
- [ ] Red Hat

## User Specific Collections
- [x] Documents (docx, xlsx, pdf, pptx, txt, rtf, tiff)
- [x] Images (png, jpg)
- [x] Audio (mp3, m4a, wma)
- [x] Video (m4v, wmv, mov)
- [x] Archives (zip, tar, 7z)
- [x] Executables (exe, bat, sh, pf)

# ToDo List
- [ ] Verification
- [ ] Remote connection
- [ ] Different image sizes and compressions (benchmarks)



