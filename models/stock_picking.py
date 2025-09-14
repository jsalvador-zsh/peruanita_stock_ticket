from odoo import models, fields, api
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    def btn_ticket(self):
        return {
            'name': 'Imprimir Ticket',
            'tag': 'picking_ticket',
            'type': 'ir.actions.client',
            'params': {
                'ticket_id': self.id,
                'model_id': 'stock.picking'
            }
        }
    
    @api.model
    def ticket_data(self, ticket_id):
        picking = self.browse(ticket_id)
        if picking:
            # Formatear fecha correctamente
            picking_date = ''
            if picking.scheduled_date:
                picking_date = picking.scheduled_date.strftime('%d/%m/%Y %H:%M')
            elif picking.date:
                picking_date = picking.date.strftime('%d/%m/%Y %H:%M')
            
            # Manejar información de la empresa de forma segura
            company = {}
            if picking.company_id:
                company = {
                    'name': picking.company_id.name or '',
                    'street': picking.company_id.street or '',
                    'vat': picking.company_id.vat or '',
                    'phone': picking.company_id.phone or '',
                    'logo': '/web/image?model=res.company&id={}&field=logo'.format(picking.company_id.id) if picking.company_id.id else ''
                }
            
            # Determinar el título del documento según el tipo de operación
            picking_type_code = picking.picking_type_id.code if picking.picking_type_id else ''
            if picking_type_code == 'outgoing':
                document_title = 'CONTROL DE DESPACHO'
            elif picking_type_code == 'incoming':
                document_title = 'GUÍA INTERNA DE RECEPCIÓN'
            else:
                document_title = 'TRANSFERENCIA DE INVENTARIO'
            
            # Manejar información del partner de forma segura
            partner_name = ''
            partner_vat = ''
            if picking.partner_id:
                partner_name = picking.partner_id.name or ''
                partner_vat = picking.partner_id.vat or ''
            
            data = {
                'name': picking.name or '',
                'picking_date': picking_date,
                'partner_id': partner_name or '',
                # Control de ingreso
                'referral_guide': picking.referral_guide or '',
                'vat': partner_vat,
                # Control de despacho
                'transport_company': picking.transport_company_id.name or '',
                'vehicle_plate': picking.vehicle_plate or '',
                'declaration_sworn': 'SI' if getattr(picking, 'declaration_sworn', False) else 'NO',
                'certificate_microbiological': 'SI' if getattr(picking, 'certificate_microbiological', False) else 'NO',
                'shipping_guide': 'SI' if getattr(picking, 'shipping_guide', False) else 'NO',

                'state': dict(self._fields['state'].selection).get(picking.state) if hasattr(self, '_fields') else '',
                'picking_type': picking.picking_type_id.name if picking.picking_type_id else '',
                'picking_type_code': picking_type_code,
                'document_title': document_title,
                'origin': picking.origin or '',
                'location_from': picking.location_id.complete_name if picking.location_id else '',
                'location_to': picking.location_dest_id.complete_name if picking.location_dest_id else '',
                'user_id': picking.user_id.name if picking.user_id else '',
                'company': company,
                'lines': []
            }
            
            # Procesar líneas de movimiento
            for line in picking.move_ids_without_package:
                line_data = {
                    'product_code': line.product_id.default_code or '',
                    'product_name': line.product_id.display_name or '',
                    'quantity': line.product_uom_qty or 0,
                    'uom_name': line.product_uom.name if line.product_uom else '',
                    'lot_name': line.move_line_ids.lot_id.name if line.move_line_ids and line.move_line_ids.lot_id else ''
                }
                data['lines'].append(line_data)
            
            return data
        return {}