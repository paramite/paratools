#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  vmprep.py
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

import click
import os
import re

from paratools import utils


@click.command()
@click.argument('regex')
@click.option(
    '-i', '--images',
    default='/var/lib/libvirt/images',
    help='path where to look for VM images'
)
@click.option(
    '-d', '--domain',
    default='internal',
    help='default domain for VMs'
)
@click.option(
    '-s', '--steps',
    default=(
        'customize,logfiles,net-hostname,net-hwaddr,puppet-data-log,'
        'udev-persistent-net'
    ),
    help='virt-sysprep steps to perform with VM image'
)
def vmprep(regex, images, domain, steps):
    """Prrepares libvirt VMs for usage.="""
    for img in os.listdir(os.path.abspath(images)):
        if not re.search(regex, img):
            continue
        click.echo('Preparing {0}'.format(img))
        hostname = img.split('.', 1)[0]
        rc, out, err = utils.execute(
            'virt-sysprep '
                '--hostname "{hostname}.{domain}" '
                '--enable "{steps}" '
                '-a {images}/{img}',
            can_fail=False
        )
        if rc:
            click.echo(err)
            exit(1)

if __name__ == '__main__':
    vmprep()
