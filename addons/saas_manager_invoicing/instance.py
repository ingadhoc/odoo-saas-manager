import time
# from lxml import etree
# import openerp.addons.decimal_precision as dp
# import openerp.exceptions

# from openerp import pooler
from openerp import netsvc
import openerplib
import openerp
import re
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from openerp.tools.translate import _
from openerp.osv import fields, osv, orm
import openerp.addons.decimal_precision as dp
import xmlrpclib
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare

# from openerp.tools.translate import _


class instance(osv.osv):
    """"""

    _inherit = 'saas_manager.instance'

    def _get_has_due(self, cr, uid, ids, name, args, context=None):
        result = {}
        instance_period_obj = self.pool.get('saas_manager.instance_period')
        for obj in self.browse(cr, uid, ids, context=context):
            res = False
            domain = []
            domain.append(('instance_id','=',obj.id))
            domain.append(('type','=','normal'))
            domain.append(('invoice_line_id.invoice_id.state','=','open'))
            domain.append(('date_due','<',datetime.today()))
            dued_instance_period_ids = instance_period_obj.search(cr, uid, domain, context=context)
            print 'dued_instance_period_ids ',dued_instance_period_ids
            if dued_instance_period_ids:
                res = True
            result[obj.id] = res
        return result

    _columns = {
            'has_due': fields.function(_get_has_due, type='boolean', string='Has Due?',),
            # 'account_invoice_line_ids': fields.one2many('account.invoice.line', 'instance_id', string='Account Invoice Lines', readonly=True), 
            }

    def create_period(self, cr, uid, ids, context=None):
        period_obj = self.pool.get('saas_manager.instance_period')
        for instance in self.browse(cr, uid, ids, context=context):
            additionals = ''
            for additional in instance.instance_additional_ids:
                additionals += additional.additional_product_id.name + ', '
                date_from = instance.next_period_start_date
                if not date_from:
                    date_from = datetime.today().strftime('%Y-%m-%d')
                # TODO use unit of mesure so we can use years or others
                date_to = (datetime.strptime(date_from,('%Y-%m-%d')) + relativedelta(months=1)).strftime('%Y-%m-%d')

                # Normal or free?
                assigned_free_periods = period_obj.search(cr, uid, [('type','=','free'),('instance_id','=',instance.id)], context=context)
                period_type = 'normal'
                if instance.product_free_periods > len(assigned_free_periods):
                    period_type = 'free'

                description = _('SaaS Product: ') + instance.product_id.name
                description += '. DB: ' + (instance.name or '')
                description += _('. Period ') + date_from + ' - ' + date_to
                description += _('. Additional Users: ') + str(instance.additional_users)
                if additionals != '':
                    description += _('. Additionals: ') + additionals

                # Invoice Line 
                invoice_line_id = False
                if period_type == 'normal':
                    invoice_ids = self.create_invoices(cr, uid, [instance.id], context=context)
                    print 'invoice_ids', invoice_ids
                    if invoice_ids:
                        invoice_id = invoice_ids[0]
                    else:
                        # TODO poner raise error
                        print 'raise error'
                    inv_lines_vals = {
                        'name': description,
                        'origin': _('SaaS: ') + instance.name,
                        'product_id': instance.product_id.id or False,
                        'price_unit': instance.subtotal,
                        'discount': instance.discount or False,
                        'quantity': 1.0,
                        'invoice_id': invoice_id,
                        'invoice_line_tax_id': [(6, 0, [x.id for x in instance.tax_id])],
                    }
                    invoice_line_id = self.pool.get('account.invoice.line').create(cr, uid, inv_lines_vals, context=context)                    
                
                period_vals = {
                    'instance_id': instance.id,
                    'date_from': date_from, 
                    'date_to': date_to, 
                    'description': description,
                    'type': period_type,
                    'invoice_line_id': invoice_line_id, 
                }

                period_id = period_obj.create(cr, uid, period_vals, context=context)

    def create_invoices(self, cr, uid, ids, open_invoices=False, context=None):
        """ create invoices for the active saas instances """

        wf_service = netsvc.LocalService("workflow")
        inv_obj = self.pool.get('account.invoice')
        inv_ids = []
        for instance in self.browse(cr, uid, ids, context=context):
            inv_values = self.pool.get('res.partner')._prepare_invoice(cr, uid, instance.partner_id, context=context)
            if inv_values:
                inv_values['comment'] =  _('SaaS Service Period ') + time.strftime('%m-%y')
                inv_values['origin'] = inv_values['reference'] = _('SaaS Serv. ') + time.strftime('%m-%y')
                inv_id = inv_obj.create(cr, uid, inv_values, context=context)
                inv_ids.append(inv_id)
                inv_obj.button_reset_taxes(cr, uid, [inv_id], context=context)
                if open_invoices:
                    wf_service.trg_validate(uid, 'account.invoice', inv_id, 'invoice_open', cr)                            
        return inv_ids              

