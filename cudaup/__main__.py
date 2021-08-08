''' main '''
# pylint: disable=E0402

import sys
from . import cudaup_options, check_python_version
from .cudaup import CudaUp

def main(name=__name__):
    ''' main entry point '''
    if name != '__main__':
        return

    if sys.argv[1] == '--check-python-version':
        check_python_version()
        return

    sys.argv = sys.argv[1:]
    CudaUp(cudaup_options.args())()

main()
