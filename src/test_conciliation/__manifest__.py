# -*- coding: utf-8 -*-

{
    'name': 'Test Conciliation',
    'version': '15.0.0.1',
    'sequence': 100,
    'summary': 'Prueba Técnica - Desarrollador Python/Odoo.',
    'category': 'Tools',
    'author': 'Yan Chirino <support@yanchirino.com>',
    'website': 'https://yanchirino.com',
    'license': 'Other proprietary',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_master.xml',
        'views/menus.xml'
    ],
    'images': [],
    'application': True,
    'installable': True,
}
