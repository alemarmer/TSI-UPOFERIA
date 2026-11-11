# -*- coding: utf-8 -*-
{
    'name': "upoferia",

    'summary': "Gestión del modulo de UPOFERIA",

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
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/caseta_view.xml',
        'views/zona_caseta_view.xml',
        'views/mesa_view.xml',
        'views/mobiliario_caseta_view.xml',
        'views/elemento_seguridad_view.xml',
        'views/licencia_view.xml',
        'views/llave_view.xml',
        'views/copia_llave_view.xml',
        'views/inspector_view.xml',
        'views/inspeccion_view.xml',
        'views/inspeccion_inspector_view.xml',
        'views/punto_control_view.xml',
        'views/incidencia_view.xml',
        'views/mantenimiento_view.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

