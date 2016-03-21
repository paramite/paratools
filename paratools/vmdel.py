#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  vmdel.py
#
#  Copyright 2016 Martin Magr <martin.magr@gmail.com>
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

import click
import os
import re

from paratools import utils


@click.command()
@click.argument('name', required=False)
def vmdel(name):
    """Removes VM (both domain and image)."""
    rc, out, err = utils.execute(
        (
            'virsh dumpxml {} | '
            'grep -A5 "disk type=\'file\' device=\'disk\'" | '
            'grep "source file"'.format(name)
        ),
        can_fail=False
    )
    if rc:
        click.echo(err)
        exit(1)

    image = re.search(
        "\<source\s*file\s*=\s*'(?P<path>.*)'\s*\/\>", out
    ).group('path')

    rc, out, err = utils.execute(
        'virsh destroy {}'.format(name), can_fail=False
    )
    if rc and not re.search('domain is not running', err):
        click.echo(err)
        exit(1)

    rc, out, err = utils.execute(
        'virsh undefine {}'.format(name), can_fail=False
    )
    if rc:
        click.echo(err)
        exit(1)

    rc, out, err = utils.execute(
        'rm -f {}'.format(image), can_fail=False
    )
    if rc:
        click.echo(err)
        exit(1)

if __name__ == '__main__':
    vmdel()
