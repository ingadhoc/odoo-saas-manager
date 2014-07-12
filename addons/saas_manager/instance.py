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

class instance(osv.osv):
    """"""
    
    _name = 'saas_manager.instance'
    _description = 'instance'

    _states_ = [
        # State machine: instance
        ('draft','Draft'),
        ('required','Required'),
        ('open','Open'),
        ('pending','Pending'),
        ('close','Close'),
        ('cancelled','Cancelled'),
    ]
    _columns = {
        'name': fields.char(string='Name', readonly=True, required=True, size=32, states={'draft': [('readonly', False)]}),
        'admin_name': fields.char(string='Admin Name', readonly=True),
        'admin_pass': fields.char(string='Admin Pwd', readonly=True),
        'db_created': fields.boolean(string='DB Created'),
        'start_date': fields.date(string='start_date', readonly=True),
        'next_period_start_date': fields.date(string='next_period_start_date', readonly=True),
        'product_free_periods': fields.integer(string='product_free_periods'),
        'state': fields.selection(_states_, "State"),
        'partner_id': fields.many2one('res.partner', string='Partner', readonly=True, required=True, states={'draft': [('readonly', False)]}), 
        'instance_user_ids': fields.one2many('saas_manager.instance_user', 'instance_id', string='Users', required=True), 
        'product_id': fields.many2one('product.product', string='Product', readonly=True, states={'draft': [('readonly', False)]}, context={'default_saas_subtype':'product','default_type':'saas'}, domain=[('type','=','saas'),('saas_subtype','=','product')], required=True), 
        'instance_additional_ids': fields.one2many('saas_manager.instance_additional', 'instance_id', string='Additionals'), 
        'instance_period_ids': fields.one2many('saas_manager.instance_period', 'instance_id', string='instance_period_ids'), 
    }

    _defaults = {
        'state': 'draft',
    }


    _constraints = [
    ]


    def action_wfk_set_draft(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state':'draft'})
        wf_service = netsvc.LocalService("workflow")
        for obj_id in ids:
            wf_service.trg_delete(uid, 'saas_manager.instance', obj_id, cr)
            wf_service.trg_create(uid, 'saas_manager.instance', obj_id, cr)
        return True



instance()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
