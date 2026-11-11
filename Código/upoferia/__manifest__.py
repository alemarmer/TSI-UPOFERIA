# -*- coding: utf-8 -*-
{
    'name': "upoferia",

    'summary': "Gestión del modulo de UPOFERIA",

    'description': """Gestion de tesoreria: movimientos, cuotas, presupuestos, cajas, cuentas bancarias, metodos de pago, tickets y productos de barra.""",

    'author': "TSI - UPOFERIA",
    'website': "https://www.upo.es",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/18.0/odoo/addons/base/data/ir_module_category_data.xml
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
        # Tesorería - Carlos
        'views/tesoreria/movimiento_view.xml',
        'views/tesoreria/cuota_view.xml',
        'views/tesoreria/presupuesto_view.xml',
        'views/tesoreria/linea_presupuesto_view.xml',
        'views/tesoreria/tipo_cuota_view.xml',
        'views/tesoreria/bonificacion_view.xml',
        'views/tesoreria/metodo_pago_view.xml',
        'views/tesoreria/caja_view.xml',
        'views/tesoreria/cuenta_bancaria_view.xml',
        'views/tesoreria/categoria_economica_view.xml',
        'views/tesoreria/ticket_view.xml',
        'views/tesoreria/linea_ticket_view.xml',
        'views/tesoreria/producto_view.xml',
        'views/tesoreria/tipo_producto_view.xml',
        'views/tesoreria/tarifa_view.xml',
        # Menús (al final: referencian las acciones)
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'application': True,
}
