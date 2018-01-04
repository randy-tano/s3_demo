"""Project directory settings.

Calculates some project directory settings by assuming they are relative this
module's location.

``BASE_DIR``
    The project module's path.

``VAR_ROOT``
    A location to put run-time generated files (such as uploaded files, or the
    collation of static files).

    If running in a virtual environment, this will be ``$VIRTUAL_ENV/var``,
    otherwise it will be ``$BASE_DIR/local``.

``VIRTUALENV_ROOT``
    The root directory of the current virtual environment, or ``''`` if no
    environment is found.
"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

python_bin = os.path.dirname(sys.executable)
_ve_path = os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR)))

# Assume that the presence of 'activate_this.py' in the python bin/
# directory means that we're running in a virtual environment.
if os.path.exists(os.path.join(python_bin, 'activate_this.py')):
    # We're running with a virtualenv python executable.
    VIRTUALENV_ROOT = os.path.dirname(python_bin)
elif _ve_path and os.path.exists(os.path.join(_ve_path, 'bin', 'activate_this.py')):
    # We're running in [virtualenv_root]/src/[project_name].
    VIRTUALENV_ROOT = _ve_path
else:
    VIRTUALENV_ROOT = ''

if VIRTUALENV_ROOT:
    VAR_ROOT = os.path.join(VIRTUALENV_ROOT, 'var')
else:
    # Set the variable root to the local configuration location (which is
    # ignored by the repository).
    VAR_ROOT = os.path.join(BASE_DIR, 'local')

if not os.path.exists(VAR_ROOT):
    os.mkdir(VAR_ROOT)
