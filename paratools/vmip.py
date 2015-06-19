#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  vmip.py
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
@click.argument('name', required=False)
def vmip(name):
    """Prints IP address of libvirt VM. If name of VM is not given as argument
    prints information of all running VMs
    """
    rc, out, err = utils.execute(
        'virsh list --state-running --name',
        can_fail=False
    )
    if rc:
        click.echo(err)
        exit(1)

    for vm in out.split('\n'):
        vm = vm.strip()
        if not vm:
            continue
        if name and name != vm:
            continue
        # get VM MAC address
        rc, out, err = utils.execute(
            'virsh dumpxml {} | grep "mac address="'.format(vm),
            can_fail=False
        )
        if rc:
            click.echo(err)
            exit(1)
        mac = re.search(
            '<mac address=\'(?P<mac>[\w:]+)\'\/>', out
        ).group('mac')
        # find IP address for MAC address
        rc, out, err = utils.execute('arp -n', can_fail=False)
        if rc:
            click.echo(err)
            exit(1)
        for record in out.split('\n'):
            record = record.strip()
            if not record:
                continue
            record = record.split()
            if mac == record[2]:
                if not name:
                    click.echo('{} '.format(vm), nl=False)
                click.echo(record[0])
                break

if __name__ == '__main__':
    vmip()
