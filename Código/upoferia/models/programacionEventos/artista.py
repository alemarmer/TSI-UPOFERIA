class Artista(models.Model):
    _name = 'feria.artista'
    _description = 'Artista'

    sDni= fields.Char(string="Nombre del evento", size=60, required=True)
    fCache_base = fields.Float(string='Caché base')
    sMontaje = fields.Char(string='Montaje')
    sIluminacion = fields.Char(string='Iluminación')
    fPotencia_kw = fields.Float(string='Potencia (kW)')
    sSonido = fields.Char(string='Sonido')
    sEspacio = fields.Char(string='Espacio')