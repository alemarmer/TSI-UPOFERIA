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
        'views/views.xml',
        'views/templates.xml',
        # Personal (RRHH y Turnos) - Juanjo
        'views/RRHH/empleado_views.xml',
        'views/RRHH/disponibilidad_views.xml',
        'views/RRHH/certificacion_views.xml',
        'views/RRHH/ausencia_views.xml',
        'views/RRHH/contrato_laboral_views.xml',
        'views/RRHH/despido_views.xml',
        'views/RRHH/entrega_uniforme_views.xml',
        'views/RRHH/taquilla_views.xml',
        'views/RRHH/asignacion_taquilla_views.xml',
        'views/RRHH/curso_formacion_views.xml',
        'views/RRHH/formacion_empleado_views.xml',
        'views/RRHH/turno_views.xml',
        'views/RRHH/menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

