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

__all__ = ['acquire', 'release', 'save', 'get', 'set']

import os
import json
from threading import Lock

from wididitclient.utils import log

def get_fd(mode='w+'):
    global _path
    open(_path, 'a') # Create the file
    return open(_path, mode)

def save():
    global _conf
    with get_fd() as file:
        json.dump(_conf, file, sort_keys=True, indent=4)

_path = os.path.expanduser('~/.config/wididit-client.json')
if not os.path.isfile(_path):
    log.info('Creating new configuration file.')
    with get_fd() as file:
        file.write('{}')

try:
    with get_fd('r') as file:
        _conf = json.load(file)
except Exception as e:
    log.error('Configuration could not be parsed. Creating backup and '
            'creating new file.')
    os.rename(_path, _path + '.bak')
    with get_fd() as file:
        file.write('{}')
    _conf = {}

_lock = Lock()

def acquire(blocking=False):
    global _lock
    _lock.acquire(blocking)

def release():
    global _lock
    _lock.release()
    save()

def get(path, default='', node=None):
    global _conf
    if node is None:
        node = _conf
    if path == []:
        return node
    name = path[0]
    if name not in node:
        if len(path) == 1:
            node[name] = default
            save()
        else:
            node[name] = {}
    return get(path[1:], default, node[name])

def set(path, value, node=None):
    global _conf
    if node is None:
        node = _conf
    name = path[0]
    path = path[1:]
    if path == []:
        node[name] = value
        save()
        return
    if name not in node:
        if path == []:
            node[name] = default
        else:
            node[name] = create_node(path[0])
    set(path, value, node[name])
