# -*- coding: utf-8 -*-
{
    'name': "upoferia",

    'summary': "Gestión del modulo de UPOFERIA",

    'description': """
Long description of module's purpose
    """,

    'author': "TSI - UPOFERIA",
    'website': "https://www.upo.es",

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
        'views/socios/persona_view.xml',
        'views/socios/socio_view.xml',
        'views/socios/beneficiario_view.xml',
        'views/socios/tipo_socio_view.xml',
        'views/socios/consentimiento_biometrico_view.xml',
        'views/socios/invitacion_acceso_view.xml',
        'views/control_accesos/punto_acceso_view.xml',
        'views/control_accesos/control_aforo_view.xml',
        'views/control_accesos/incidencia_puerta_view.xml',
        'views/control_accesos/registro_accesos_view.xml',
        'views/turnos/fichaje_view.xml',
        'views/menu.xml',
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
        #'demo/demo.xml',
    ],
    'application': True,
}

