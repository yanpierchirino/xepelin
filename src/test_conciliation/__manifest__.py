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
    'images': [],
    'depends': ['base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/cron.xml',
        'wizards/testdata_import.xml',
        'views/res_master.xml',
        'views/res_complement.xml',
        'views/res_reconciled.xml',
        'views/menus.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'test_conciliation/static/src/js/listview.js'
        ],
        'web.assets_qweb': [
            'test_conciliation/static/src/xml/templates.xml'
        ]
    },
    'application': True,
    'installable': True,
}
