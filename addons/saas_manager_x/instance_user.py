# -*- coding: utf-8 -*-
##############################################################################
#
#    Saas Manager
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
import openerp
from openerp.tools.translate import _
from openerp import netsvc
from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp

class instance_user(osv.osv):
    """"""
    
    _inherit = 'saas_manager.instance_user'

    _columns = {
        'product_id': fields.related('instance_id', 'product_id', type='many2one',
            relation='product.product', string='Product'),
    }

    _defaults = {
        'active': True,
    }

    def _check_not_admin_login(self, cr, uid, ids, context=None):
        for user_it in self.browse(cr, uid, ids, context=context):
            if user_it.login == 'admin':
                return False
        return True


    _constraints = [
        (_check_not_admin_login, 'Error: It is not possible to create a user with login "admin"', ['login']),
    ]

    _sql_constraints = [
        ('login_unique', 'unique(login, instance_id)', 'Login name must be unique per Instance!'),
    ]    
    
    def unlink(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        instances = self.read(cr, uid, ids, ['remote_id'], context=context)
        unlink_ids = []

        for t in instances:
            if t['remote_id']:
                raise openerp.exceptions.Warning(_('You cannot delete a user that has already been syncronized, yon can deactivate it with the active field'))
            else:
                unlink_ids.append(t['id'])

        osv.osv.unlink(self, cr, uid, unlink_ids, context=context)
        return True
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
