# Copyright (C) 2011, Valentin Lorentz
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import sys

from PyQt4 import QtGui

def data_file_path(filename):
    """Return the path to the data file."""
    suffix = os.path.join('share', 'wididitclient', filename)
    path = os.path.join(sys.prefix, suffix)
    if os.path.isfile(path):
        return path

    path = os.path.join(sys.prefix, 'local', suffix)
    if os.path.isfile(path):
        return path

    return filename

def get_qicon(filename='ui/whale.svg'):
    """Return a QIcon instance.
    """
    return QtGui.QIcon(data_file_path(filename))
