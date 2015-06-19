#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  token.py
#
#  Copyright 2015 Martin Magr <martin.magr@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import base64
import click
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import hashlib
import hmac
import os
import struct


CONF_PATH = '~/.config/paratools/tkn.conf'
CNT_PATH = '~/.config/paratools/.tkn_counter'

@click.command()
def tkn():
    """Prints IP address of libvirt VM. If name of VM is not given as argument
    prints information of all running VMs
    """
    config = configparser.SafeConfigParser()
    if not config.read(os.path.expanduser(CONF_PATH)):
        raise ValueError('Failed to parse config file {}.'.format(path))

    secret = config.get('token', 'secret')
    with open(os.path.expanduser(CNT_PATH)) as cntf:
        counter = int(cntf.read().strip())
    with open(os.path.expanduser(CNT_PATH), 'w') as cntf:
        counter += 1
        cntf.write(str(counter))

    try:
        key = base64.b32decode(secret, True)
    except TypeError:
        secret += "=" * ((8 - len(secret) % 8) % 8)
        key = base64.b32decode(secret, True)
    msg = struct.pack(">Q", counter)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = ord(h[19]) & 15
    token = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    token = str(token)
    if len(token) < 6:
        token = '0' * (6 - len(token)) + token
    click.echo(token)

if __name__ == '__main__':
    tkn()
