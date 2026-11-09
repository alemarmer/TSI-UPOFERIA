# -*- coding: utf-8 -*-
{
    'name': "upoferia",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/tipo_evento_views.xml',
        'views/evento_views.xml',
        'views/actuacion_views.xml',
        'views/concurso_views.xml',
        'views/reserva_views.xml',
        'views/artista_views.xml',
        'views/caballo_views.xml',
        'views/carruaje_views.xml',
        'views/salida_views.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}

