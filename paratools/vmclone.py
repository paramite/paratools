#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  vmclone.py
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
@click.option(
    '-i', '--image',
    default=None,
    help=(
        'path of new VM image; if None is given, the path will be created '
        'from the same dirname as has template image and from new VM name'
    )
)
@click.argument('template', required=True)
@click.argument('name', required=True)
def vmclone(template, name, image):
    """Clones VM using virt-clone and performs necessary additiona steps.
    Takes name of template VM and name of new VM as arguments.
    """
    if not image:
        rc, out, err = utils.execute(
            (
                'virsh dumpxml {} | '
                'grep -A5 "disk type=\'file\' device=\'disk\'" | '
                'grep "source file"'.format(template)
            ),
            can_fail=False
        )
        if rc:
            click.echo(err)
            exit(1)

        template_image = re.search(
            "\<source\s*file\s*=\s*'(?P<path>.*)'\s*\/\>", out
        ).group('path')
        image = os.path.join(
            os.path.dirname(template_image), '{}.qcow2'.format(name)
        )

    rc, out, err = utils.execute(
        'virt-clone -o {template} -n {name} -f {image}'.format(**locals()),
        can_fail=False
    )
    if rc:
        click.echo(err)
        exit(1)

    # XXX: 1) Hack for bug in virt-clone, which makes new domain XML Invalid
    rc, out, err = utils.execute(
        (
            "virsh dumpxml {name} | "
            "sed 's/domain-{template}/domain-{name}/' > "
            "/var/tmp/paratools-vmclone-{name}.xml".format(**locals())
        ),
        can_fail=False
    )
    if rc:
        click.echo(err)
        exit(1)

    rc, out, err = utils.execute(
        (
            'virsh undefine {name} && '
            'virsh define /var/tmp/paratools-vmclone-{name}.xml && '
            'rm -f /var/tmp/paratools-vmclone-{name}.xml'.format(**locals())
        ),
        can_fail=False
    )
    if rc:
        click.echo(err)
        exit(1)

if __name__ == '__main__':
    vmclone()
