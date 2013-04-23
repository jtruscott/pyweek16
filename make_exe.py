from distutils.core import setup
import os
import py2exe


#hack which fixes the pygame mixer and pygame font
origIsSystemDLL = py2exe.build_exe.isSystemDLL # save the orginal before we edit it
def isSystemDLL(pathname):
    # checks if the freetype and ogg dll files are being included
    if os.path.basename(pathname).lower() in ("libfreetype-6.dll", "libogg-0.dll","sdl_ttf.dll"): # "sdl_ttf.dll" added by arit.
            return 0
    return origIsSystemDLL(pathname) # return the orginal function
py2exe.build_exe.isSystemDLL = isSystemDLL # override the default function with this one

setup(windows=['run_game.py'],
    options = {
    'py2exe': {
        'bundle_files': 1,
        'compressed': True,
        'ascii': True,
        'excludes': [
            '_ssl',
            'pyreadline', 'doctest', 'locale',
            'pdb', 'pickle', 'calendar', 'inspect'],
        }
    },
    zipfile=None
)
