#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ghrepo.py
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
import sys

from github import Github
from paratools import utils


@click.command()
@click.option('--user', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
@click.argument('org', required=True)
@click.argument('name', required=True)
def ghrepo(org, name, user=None, password=None):
    """Creates new GitHub repository under given organization."""
    Github(user, password).get_organization(org).create_repo(name)
    click.echo(
        'Created repository https://github.com/{}/{}'.format(org, name)
    )


if __name__ == '__main__':
    ghrepo()
