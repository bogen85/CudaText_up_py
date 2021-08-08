''' OS utilities '''
# pylint: disable=E0402

import os
import sys
import subprocess

from . import fail, SYSTEM_SHELL

def exe_src():
    ''' directory of script running us '''
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def is_readable_writeable(fpath):
    ''' is readable and writeable '''
    return os.access(fpath, os.R_OK) and os.access(fpath, os.W_OK)

def is_readable_executeable(fpath):
    ''' is readable and executable '''
    return os.access(fpath, os.X_OK) and os.access(fpath, os.R_OK)

def is_exe(fpath):
    ''' exists and is executable '''
    return os.path.isfile(fpath) and is_readable_executeable(fpath)

def is_dir(fpath):
    ''' exists and is traversable '''
    return os.path.isdir(fpath) and is_readable_executeable(fpath)

def is_work_dir(fpath):
    ''' exists, is traversable, readable, writeable'''
    return is_dir(fpath) and is_readable_writeable(fpath)

def which(program):
    ''' find path of program '''
    fpath, _ = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None

def find_program_dirname(program):
    ''' find path that program resides in '''
    exepath = which(program)
    return os.path.dirname(os.path.realpath(exepath)) if exepath else None

def run_shell_script(script_in):
    ''' run shell scriptlet '''
    prescript = 'set -euo pipefail'
    script = '%s; %s' % (prescript, script_in)
    cmd = subprocess.run([SYSTEM_SHELL, '-c', script], check=False)
    return cmd.returncode

def checked_shell_script(script):
    ''' check run shell scriptlet '''
    status = run_shell_script(script)
    if status != 0:
        fail('%s failed with %d for %s' % (SYSTEM_SHELL, status, script))
