# -*- coding: utf-8 -*-
{
    'name': "upoferia",

    'summary': "Gestión del modulo de UPOFERIA",

    'description': """Gestion de transacciones con proveedores, categorias de proveedor, marcas, patrocinios, exhibiciones, espacios publicitarios, servicios y tecnicos.""",

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
        'demo/upoferia.tipo_transaccion.csv', # Los tipos de transaccion (PED, ALB, FAC, ABO, CON) se cargan siempre porque los necesita el modulo.
        'views/RRHH/menus.xml',
        'views/tipo_evento_views.xml',
        'views/evento_views.xml',
        'views/actuacion_views.xml',
        'views/concurso_views.xml',
        'views/reserva_views.xml',
        'views/artista_views.xml',
        'views/caballo_views.xml',
        'views/carruaje_views.xml',
        'views/salida_views.xml',
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
        #'demo/demo.xml',
    ],
    'application': True,
}
