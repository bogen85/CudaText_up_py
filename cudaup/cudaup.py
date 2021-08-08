''' cudaup '''
# pylint: disable=E0402

import os
import platform
from pathlib import Path
from .osutil import (
        is_dir, is_exe, exe_src, is_work_dir, checked_shell_script,
        which,
    )
from . import fail, BUILD_TEMP

CUDAUP_PACKETS_IN = 'cudaup.packets'
CUDAUP_REPOS_IN = 'cudaup.repos'

def check_path(fpath, fun, failmsg):
    ''' check path with given function '''
    if not fun(fpath):
        fail(failmsg)

def read_src_sequence(srcdir, filepath):
    ''' read lines from file into sequence '''
    return tuple(Path("%s/%s" % (srcdir, filepath)).read_text().splitlines())

class CudaUp():
    ''' cudaup class '''

    def check_args(self):
        ''' check arguments '''
        if self.args.make:
            check_path(
                self.args.lazdir,
                is_dir,
                "Could not find Lazarus directory (%s)\nUse -l <path> option" %
                self.args.lazdir
            )
            check_path(
                self.lazbuild,
                is_exe,
                "Could not find lazbuild (%s)\nUse -l <path> option" %
                self.lazbuild
            )
        if not is_work_dir(self.args.work_dir):
            fail(
                '"%s" is not a suitable working directory' %
                self.args.work_dir
            )

    def __init__(self, args):
        self.args = args
        self.src = exe_src()

        self.lazbuild = "%s/lazbuild" % (self.args.lazdir)
        self.args.work_dir = os.path.realpath(args.work_dir)
        self.check_args()
        self.packets = read_src_sequence(self.src, CUDAUP_PACKETS_IN)
        self.repos = read_src_sequence(self.src, CUDAUP_REPOS_IN)
        self.git = which('git')
        self.src = "%s/src" % (self.args.work_dir)
        self.run_cmd = checked_shell_script
        self.cmd0 = "%s -q" % (self.lazbuild)
        self.cmd1 = "%s --lazarusdir=%s" % (self.cmd0, self.args.lazdir)


    def check_src_dir(self):
        ''' make src dir '''
        self.run_cmd('mkdir -pv %s' % (self.src))

    def clean(self):
        ''' clean '''
        if not self.args.clean:
            return
        self.run_cmd('rm -rf %s' % (BUILD_TEMP))

    def get(self):
        ''' get '''

        if not self.args.get:
            return

        if not self.git:
            fail('git was not found in the search PATH')

        self.check_src_dir()
        for repo in self.repos:
            checkout = "%s/%s" % (self.src, os.path.basename(repo))
            if not is_work_dir("%s/.git" % (checkout)):
                self.run_cmd("git -C %s clone %s" % (self.src, repo))
            self.run_cmd("git -C %s pull origin master" % (checkout))

    def packs(self):
        ''' packs '''
        if not self.args.packs:
            return

        run_cmd = self.run_cmd

        for packet in self.packets:
            run_cmd('%s %s/%s' % (self.cmd1, self.src, packet))
            run_cmd('%s --add-package %s/%s' % (self.cmd1, self.src, packet))

        run_cmd("%s --build-ide=" % (self.cmd0))

    def make(self):
        ''' make '''
        if not self.args.make:
            return

        cpu = self.args.cpu
        run_cmd = self.run_cmd

        incs = []
        if cpu == 'amd64':
            cpu = 'x86_64'
        if self.args.os != 'linux':
            incs.append('--os=%s' % (self.args.os))
        if self.args.os == 'win32':
            cpu = 'i386'
        if self.args.os == 'win64':
            cpu = 'x86_64'
        if cpu != platform.processor:
            incs.append('--cpu=%s' % cpu)
        if self.args.ws != "":
            incs.append('--ws=%s' % (self.args.ws))
        inc = ' '.join(incs)

        if not self.args.packs:
            for packet in self.packets:
                run_cmd('%s %s %s/%s' % (self.cmd1, inc, self.src, packet))

        ws = self.args.ws if self.args.ws else "gtk2"

        app = "%s/CudaText/app" % (self.src)
        _cudatext = '%s/cudatext' % (app)
        run_cmd('rm -vf %s' % (_cudatext))
        run_cmd('rm -vf %s.exe' % (_cudatext))
        run_cmd('%s %s %s.lpi' % (self.cmd1, inc, _cudatext))

        outdir = "%s/bin/%s-%s-%s" % (self.src, self.args.os, cpu, ws)
        run_cmd('mkdir -pv %s' % (outdir))
        if self.args.os in ('win32', 'win64'):
            run_cmd('cp -v %s.exe %s/cudatext.exe' % (_cudatext, outdir))
        else:
            run_cmd('cp -v %s %s/cudatext' % (_cudatext, outdir))

    def __call__(self):
        self.clean()
        self.get()
        self.packs()
        self.make()
