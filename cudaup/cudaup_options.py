''' Cudaup Options '''
# pylint: disable=E0402

import os
import platform

from .osutil import find_program_dirname
from . import ArgumentParser, BUILD_TEMP

def args():
    ''' parse command line arguments '''
    return ArgumentParser(
        "Download CudaText sources (all packages) and compile them."
        )(
            '-g', '--get',
            action='store_true',
            help='download packages'
        )(
            '-p', '--packs',
            action='store_true',
            help='install packages to Lazarus'
        )(
            '-m', '--make',
            action='store_true',
            help='compile CudaText'
        )(
            '-l', '--lazdir',
            metavar="directory",
            default=find_program_dirname('lazbuild'),
            help="set Lazarus directory"
        )(
            '-o', '--os',
            default=platform.system().lower(),
            help='set target OS (win32/win64/linux/freebsd/darwin/solaris'
        )(
            '-c', '--cpu',
            metavar='arch',
            default=platform.processor(),
            help='set target CPU (i386/x86_64/arm)'
        )(
            '-w', '--ws', '--widget-set',
            metavar='widgetset',
            default='',
            help="override WidgetSet (gtk2/gtk3/qt/qt5/cocoa)"
        )(
            '--clean', action='store_true',
            help='delete temp Free Pascal folders (%s)' % BUILD_TEMP,
        )(
            '-wd', '--work-dir', '--working-directory',
            metavar='work_dir',
            default=os.getcwd(),
            help=(
                "working directory to download to and build in. "
                "default is current directory."
            )
        )()
