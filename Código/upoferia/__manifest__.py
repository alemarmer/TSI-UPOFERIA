# -*- coding: utf-8 -*-
{
    'name': "upoferia",

    'summary': """Gestion de la feria: compras, proveedores y patrocinios""",

    'description': """Gestion de transacciones con proveedores, categorias de proveedor, marcas, patrocinios, exhibiciones, espacios publicitarios, servicios y tecnicos.""",

    'author': "TSI - UPO",
    'website': "https://www.upo.es",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/18.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/tipo_transaccion_view.xml',
        'views/transaccion_view.xml',
        'views/linea_transaccion_view.xml',
        'views/categoria_proveedor_view.xml',
        'views/proveedor_view.xml',
        'views/marca_view.xml',
        'views/patrocinio_view.xml',
        'views/exhibicion_marca_view.xml',
        'views/espacio_publicitario_view.xml',
        'views/servicio_view.xml',
        'views/servicio_proveedor_view.xml',
        'views/tecnico_view.xml',
        'views/menu.xml',
        'demo/upoferia.tipo_transaccion.csv', # Los tipos de transaccion (PED, ALB, FAC, ABO, CON) se cargan siempre porque los necesita el modulo.
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'application': True,
}
