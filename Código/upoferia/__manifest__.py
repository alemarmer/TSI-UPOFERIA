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
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/menu.xml',
        'views/gamificacion/mision_view.xml',
        'views/gamificacion/mision_descubrimiento_view.xml',
        'views/gamificacion/mision_evento_view.xml',
        'views/gamificacion/mision_sociales_view.xml',
        'views/gamificacion/racha_view.xml',
        'views/gamificacion/recompensas_view.xml',
        'views/gamificacion/registros_view.xml',
        'views/gamificacion/temporadas_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,    
    
}

