# -*- coding: utf-8 -*-

import re, hashlib, base64, io
from PIL import Image, ImageOps
from odoo import models, fields, api


class Persona(models.Model):
    _name = 'upoferia.socios.persona'
    _description = 'Persona'
    _rec_name = 'dni'
    
    dni = fields.Char(string="DNI", size=9, required=True)
    nombre = fields.Char("Nombre")
    telefono = fields.Char("Teléfono", size=9)
    codigo_persona = fields.Char("Código Persona", compute='_compute_codigo_persona', store=True, readonly=True)
    qr_nombre = fields.Char("Nombre QR", readonly=True)
    qr_imagen = fields.Binary("Código QR", attachment=True, readonly=True, store=False, compute='_compute_qr_imagen')
    email = fields.Char("Correo")
    direccion_calle = fields.Char("Calle")
    direccion_ciudad = fields.Char("Ciudad")
    direccion_cp = fields.Char("Código Postal")
    invitaciones_recibidas_ids = fields.One2many('upoferia.socios.invitacion_acceso', 'persona_id', string="Invitaciones recibidas")
    consentimiento_biometrico_ids = fields.One2many('upoferia.socios.consentimiento_biometrico', 'persona_id', string="Consentimientos biométricos")
    registro_accesos_ids = fields.One2many('upoferia.control_accesos.registro_accesos', 'persona_id', string='Registros de accesos')
    
    @api.depends('dni')
    def _compute_codigo_persona(self):
        for persona in self:
            if persona.dni:
                persona.codigo_persona = hashlib.md5(persona.dni.encode()).hexdigest()[:12]
            else:
                persona.codigo_persona = False

    @api.depends('codigo_persona')
    def _compute_qr_imagen(self):
        for persona in self:
            if not persona.codigo_persona:
                persona.qr_imagen = False
                persona.qr_nombre = False
                continue

            png = self.env['ir.actions.report'].barcode('QR', persona.codigo_persona, width=300, height=300)

            # Si no ponemos fondo y borde da fallo al escanear
            qr = Image.open(io.BytesIO(png)).convert('RGBA')
            lienzo = Image.new('RGB', qr.size, 'white')
            lienzo.paste(qr, mask=qr.split()[3])
            lienzo = ImageOps.expand(lienzo, border=40, fill='white')
            buffer = io.BytesIO()
            lienzo.save(buffer, format='PNG')
            persona.qr_imagen = base64.b64encode(buffer.getvalue())
            persona.qr_nombre = f"qr_{persona.codigo_persona}.png"

    @api.constrains('dni')
    def _check_dni(self):
        LETRAS_DNI = "TRWAGMYFPDXBNJZSQVHLCKE"
        if not re.match(r"^\d{8}[A-Z]$", self.dni):
            raise models.ValidationError('El DNI debe tener 8 números y una letra.')
        elif LETRAS_DNI[int(self.dni[:8]) % 23] != self.dni[8]:
            raise models.ValidationError("La letra del DNI no es válida.")
            
    @api.constrains('telefono')
    def _check_telefono(self):
        if not self.telefono.isdigit():
            raise models.ValidationError('El teléfono solo debe contener números.')
            
    @api.constrains('email')
    def _check_email(self):
        if self.email and not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", self.email):
            raise models.ValidationError('El correo no es válido.')
            
    _sql_constraints = [('dni_unique', 'UNIQUE(dni)', 'Ya existe un registro con este DNI.'),('codigo_persona_unique', 'UNIQUE(ccodigo_persona)', 'Ya existe un registro con este Código Persona.')]