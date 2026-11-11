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
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        # Montaje
        'views/cuadrilla_views.xml',
        'views/plan_montaje_views.xml',
        'views/fase_montaje_views.xml',
        'views/tarea_montaje_views.xml',
        'views/transporte_views.xml',
        # Material y préstamos
        'views/categoria_material_views.xml',
        'views/material_views.xml',
        'views/uso_material_views.xml',
        'views/prestamo_views.xml',
        'views/prestamo_linea_views.xml',
        # Menús (al final: referencian las acciones)
        'views/menu_montaje_material.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}

