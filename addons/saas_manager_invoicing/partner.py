# -*- coding: utf-8 -*-
##############################################################################
#
#    Nautical
#    Copyright (C) 2013 Sistemas ADHOC
#    No email
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


import re
from openerp import netsvc
from openerp.osv import osv, fields
from datetime import datetime, date, timedelta
from openerp.tools.translate import _
from dateutil.relativedelta import relativedelta
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare

class partner(osv.osv):
    """"""
    
    _inherit = 'res.partner'

    _columns = {
    }

    _sql_constraints = [
    ]    


    def process_active_partner_invoices(self, cr, uid, ids=None, open_invoices=False, context=None):
        if context is None:
            context = {}
        if ids is None:
            ids = self.search(cr, uid, [], context=context)
        res = None
        context['date_invoice'] = time.strftime(DEFAULT_SERVER_DATE_FORMAT) 
        active_partner_ids = self.get_active_partner_ids(cr, uid, ids, context)
        return self.create_invoices(cr, uid, active_partner_ids, open_invoices, context)

    def get_active_partner_ids(self, cr, uid, ids, context=None):        
        active_partner_ids = []
        for record in self.browse(cr, uid, ids, context):
            for instance in record.instance_ids:
                if instance.state in ['open']:
                    active_partner_ids.append(record.id)
                    # We make this break because this partner is active, we go to the next partner
                    break
        return active_partner_ids

    def create_invoices(self, cr, uid, ids, open_invoices=False, context=None):
        """ create invoices for the active saas instances """

        wf_service = netsvc.LocalService("workflow")
        inv_obj = self.pool.get('account.invoice')
        inv_ids = []
        for partner in self.browse(cr, uid, ids, context=context):
            inv_values = self._prepare_invoice(cr, uid, partner, context=context)
            if inv_values:
                inv_values['comment'] =  _('SaaS Service Period ') + time.strftime('%m-%y')
                inv_values['origin'] = inv_values['reference'] = _('SaaS Serv. ') + time.strftime('%m-%y')
                inv_id = inv_obj.create(cr, uid, inv_values, context=context)
                inv_ids.append(inv_id)
                for instance in partner.instance_ids:
                    if instance.state in ['open']:
                        inv_lines_vals = self._prepare_invoice_line_instance(cr, uid, instance, inv_id, context=context)
                        print inv_lines_vals
                        if inv_lines_vals:
                            self.pool.get('account.invoice.line').create(cr, uid, inv_lines_vals, context=context)
                inv_obj.button_reset_taxes(cr, uid, [inv_id], context=context)
                if open_invoices:
                    wf_service.trg_validate(uid, 'account.invoice', inv_id, 'invoice_open', cr)                            
        return inv_ids

    def _prepare_invoice_line_instance(self, cr, uid, instance, inv_id, context=None):
        if context is None:
            context = {}

        result = []

        inv_line_values = {
            'name': instance.product_id.name + '. DB: ' + (instance.name or '') + _('. Period ') + time.strftime('%m-%y'),
            # 'origin': sale.name,
            # 'account_id': res['account_id'],
            'price_unit': instance.subtotal,
            'instance_id': instance.id,
            'quantity': 1.0,
            'discount': instance.discount or False,
            # 'uos_id': instance.product_uom.id or False,
            'product_id': instance.product_id.id or False,
            'invoice_id': inv_id,
            'invoice_line_tax_id': [(6, 0, [x.id for x in instance.tax_id])],
            # 'invoice_line_tax_id': [(6, 0, [x.id for x in line.tax_id])],
            # 'account_analytic_id': line.order_id.project_id and line.order_id.project_id.id or False,
            # 'invoice_line_tax_id': res.get('invoice_line_tax_id'),
            # 'account_analytic_id': sale.project_id.id or False,
        }
        return inv_line_values
