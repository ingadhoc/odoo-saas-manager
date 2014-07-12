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

class instance_period(osv.osv):
    """"""
    
    _name = 'saas_manager.instance_period'
    _description = 'instance_period'

    _columns = {
        'date_from': fields.date(string='date_from'),
        'date_to': fields.date(string='date_to'),
        'description': fields.char(string='description'),
        'invoice_line_id': fields.many2one('account.invoice.line', string='invoice_line_id'),
        'type': fields.selection([(u'free', 'free'), (u'normal', 'normal')], string='type'),
        'residual': fields.float(string='residual'),
        'amount_total': fields.float(string='amount_total'),
        'date_due': fields.date(string='date_due'),
        'state': fields.char(string='state'),
        'instance_id': fields.many2one('saas_manager.instance', string='instance_id', ondelete='cascade', required=True), 
    }

    _defaults = {
    }


    _constraints = [
    ]




instance_period()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
