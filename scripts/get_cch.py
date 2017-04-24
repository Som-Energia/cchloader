# -*- coding: utf-8 -*-

# Script to load all configured and enabled providers on PowerERP

import click
import os
from erppeek import Client
from urlparse import urlparse

@click.command()
@click.option('-s', '--server', default='http://localhost',
                help='Dirección del servidor')
@click.option('-p', '--port', default=8069, help='Puerto servidor ERP',
                type=click.INT)
@click.option('-d', '--db', help='Nombre de la base de datos')
@click.option('-u', '--user', default='admin', help='Usuario del servidor')
@click.option('-w', '--password', default='admin', help='Contraseña usuario')

def config_connection(**kwargs):
    config = {
        'erp':
            {
                'uri': '{}:{}'.format(kwargs['server'], kwargs['port']),
                'db': kwargs['db'],
                'user': kwargs['user'],
                'password': kwargs['password']
            }
    }

    u = urlparse(config['erp']['uri'])
    config['erp']['uri'] = '{protocol}://{url}'.format(**{'protocol': u.scheme, 'url': u.hostname})
    config['erp']['port'] = u.port
    c = Client(config['erp']['uri']+ ':' + str(config['erp']['port']),
             config['erp']['db'],
             config['erp']['user'],
             config['erp']['password'])
    get_cch(c)


def get_cch(c):
    providers = c.TgComerProvider.read([],[])
    for provider in providers:
         print "Loading {} CCH curves".format(provider['name'])
         c.TgComerReader.reader([provider['id']])

if __name__ == "__main__":
   config_connection(auto_envvar_prefix='PEEK')

