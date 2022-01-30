#!/bin/sh

set -euo pipefail

_PY_VERS0="
python3.11 python3.10 python3.10 python3.9 python3.8 python3.7
python3.6 python3.5
"
_PY_VERS1="
python39 python38 python37 python36 python35
"
_PY_VERS="$_PY_VERS0 $_PY_VERS1 python3 python
"

PY_VERS=${PYTHON:-$_PY_VERS}

PYTHON=${PYTHON:-__undefined__}

DISABLE_ROOT_CHECK=${DISABLE_ROOT_CHECK:-no}

error () {
    echo > /dev/stderr $@
}

find_python() {
    for py in $PY_VERS; do
        if which 2>/dev/null 1>/dev/null $py; then
            PYTHON=$py
            return
        fi
    done
    echo no python found in ["$PY_VERS"]
    exit 1
}

invalid_python_version () {
    error
    exe=$PYTHON
    $exe > /dev/stderr --version
    error
    error "'$exe' does not satisfy python version requirements."
    error "Recommended python executables:"
    error " $_PY_VERS0"
    error "Also accepted python executables:"
    error " $_PY_VERS1"
    exit 1
}

root_check() {
    if [ "$USER" == root ]; then
        error 'Please do not run builds as root'
        error 'Use fakeroot if building an archive'
        exit 1
    fi
}

main() {
    [ "$DISABLE_ROOT_CHECK" == 'yes' ] || root_check
    find_python
    export PYTHONPATH=$(dirname "$0")
    $PYTHON -m cudaup --check-python-version || invalid_python_version
    exec $PYTHON -m cudaup "$0" "$@"
}

main "$@"
