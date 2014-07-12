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
from datetime import datetime, date, timedelta
from openerp import netsvc
from openerp.osv import osv, fields

class instance_period(osv.osv):
    """"""
    
    _inherit = 'saas_manager.instance_period'

    def _get_state(self, cr, uid, ids, name, args, context=None):
        result = {}
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.type == 'free':
                res = 'free'
            elif obj.invoice_line_id.invoice_id:
                if (obj.invoice_line_id.invoice_id.state == 'open') and (datetime.strptime(obj.invoice_line_id.invoice_id.date_due,('%Y-%m-%d')) > datetime.today()):
                    res = 'due'
                res = obj.invoice_line_id.invoice_id.state
            else:
                res = 'uninvoiced'
            result[obj.id] = res
        return result

    _columns = {
        'state': fields.related('invoice_line_id', 'invoice_id', 'state', string='State', type='char', readonly=True,),
        # 'state': fields.function(_get_state, type='selection', selection=[('uninvoiced', 'Uninvoiced'),('due', 'Due'),('draft', 'Draft'),('open', 'Open'),('paid', 'Paid'),('cancelled', 'Cancelled'),('free', 'Free')], string='State'),
        'date_due': fields.related('invoice_line_id','invoice_id', 'date_due', string='Due Date', type='date', readonly=True,),
    }

    _defaults = {
    }


    _constraints = [
    ]




instance_period()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
