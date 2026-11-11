# -*- coding: utf-8 -*-
# from odoo import http


# class Upoferia(http.Controller):
#     @http.route('/upoferia/upoferia', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/upoferia/upoferia/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('upoferia.listing', {
#             'root': '/upoferia/upoferia',
#             'objects': http.request.env['upoferia.upoferia'].search([]),
#         })

#     @http.route('/upoferia/upoferia/objects/<model("upoferia.upoferia"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('upoferia.object', {
#             'object': obj
#         })

