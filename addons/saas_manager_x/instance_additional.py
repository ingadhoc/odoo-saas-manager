# -*- coding: utf-8 -*-
##############################################################################
#
#    Saas Manager
#    Copyright (C) 2014 Sistemas ADHOC
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
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare

class instance_additional(osv.osv):
    """"""
    
    _inherit = 'saas_manager.instance_additional'

    def _get_aditional_price(self, cr, uid, ids, name, args, context=None):
        cur_obj = self.pool.get('res.currency')
        result = {}
        date_order = time.strftime(DEFAULT_SERVER_DATE_FORMAT)   
        for record in self.browse(cr, uid, ids, context=context):
            result[record.id] = {}            
            additional_price = self.pool.get('product.pricelist').price_get(cr, uid, [record.instance_id.pricelist_id.id],
                    record.additional_product_id.id, 1.0, record.instance_id.partner_id.id, {
                        'uom': record.additional_product_id.uom_id.id,
                        'date': date_order,
                        })[record.instance_id.pricelist_id.id]
            
            cur = record.instance_id.pricelist_id.currency_id
            result[record.id]['additional_price'] = cur_obj.round(cr, uid, cur, additional_price)
        return result

    _columns = {
        'additional_price': fields.function(_get_aditional_price, type='float', string='Price', readonly=True, multi='additional'),
    }



instance_additional()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
