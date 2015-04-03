Senator Patrick Leahy Center for Digital Investigations Collector
=====

LCDI Collector

Written by Chapin Bryce

# Usage

## GUI:
`python lcdic_gui.py`

- Follow the GUi steps to begin using the tool!

## Command line:
`python lcdic.py E: \output\path --os [OS TYPE]`

- Where `E:` is the mounted drive to collect from 
  - Can be mounted with F-response (not tested)
  - Can be mounted with FTK Imager
  - Can be a local directory of a non-system partition
- Where `\output\path` is the path to the output
  - Can be a full or relative path
- Where `--os` is the OS to collect
  - To get a list of supported OS's, run `--os list`

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
- [x] User Selection
- [x] Document Collection (See Below)

## User Specific Collections
- [x] Examiner Specified Extensions in Config.ini
- [x] Documents (docx, xlsx, pdf, pptx, txt, rtf, tiff)
- [x] Images (png, jpg)
- [x] Audio (mp3, m4a, wma)
- [x] Video (m4v, wmv, mov)
- [x] Archives (zip, tar, 7z)
- [x] Executables (exe, bat, sh, pf)

### Potential Support
- [ ] Tar Compression
- [ ] Yara Searching
- [ ] Copy out $MFT, $Logfile, $J - Cannot grab while partition is mounted
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

# ToDo List
- [ ] Verification & Validation
- [ ] Remote connection
- [ ] Different image sizes and compressions (benchmarks)



