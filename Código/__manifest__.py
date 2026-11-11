# -*- coding: utf-8 -*-
{
    'name': "upoferia",

    'summary': "Gestion del modulo upoferia",

    'description': """Gestion integral de casetas de feria""",

    'author': "UPO",
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
        'views/menus.xml',
        # Tesorería
        'views/movimiento.xml',
        'views/cuota.xml',
        'views/presupuesto.xml',
        'views/linea_presupuesto.xml',
        # Catálogos
        'views/tipo_cuota.xml',
        'views/bonificacion.xml',
        'views/metodo_pago.xml',
        'views/caja.xml',
        'views/cuenta_bancaria.xml',
        'views/categoria_economica.xml',
        # Barra
        'views/ticket.xml',
        'views/linea_ticket.xml',
        'views/producto.xml',
        'views/tipo_producto.xml',
        'views/tarifa.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}

