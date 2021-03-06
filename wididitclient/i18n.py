#!/usr/bin/env python

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
import gettext

from wididitclient.utils import log

if 'unittest' in sys.modules:
    _ = lambda x:x
else:
    try:
        log.debug('Trying default gettext path.')
        _trans = gettext.translation('wididitclient')
        _ = _trans.ugettext
        log.debug('Using default gettext path.')
    except:
        try:
            path = os.path.join(sys.prefix, 'local', 'share', 'locale')
            log.debug('Trying forced local path for gettext: %s' % path)
            _trans = gettext.translation('wididitclient', localedir=path)
            _ = _trans.ugettext
            log.debug('Using forced local path for gettext.')
        except:
            def _(string, *args, **kwargs):
                return string
            log.debug('Using gettext fallback.')

