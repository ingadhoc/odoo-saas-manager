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

class product(osv.osv):
    """"""
    
    _name = 'product.product'
    _inherits = {  }
    _inherit = [ 'product.product' ]

    _columns = {
        'saas_product': fields.boolean(string='SaaS Product'),
        'base_url': fields.char(string='Base URL'),
        'server_url': fields.char(string='Server URL'),
        'server_port': fields.char(string='Server Port'),
        'server_super_admin_pwd': fields.char(string='Super Admin Pwd'),
        'admin_name': fields.char(string='Admin Name'),
        'admin_pass': fields.char(string='Admin Pwd'),
        'template_db_name': fields.char(string='Template DB name'),
        'free_periods': fields.integer(string='Free Periods'),
        'free_periods_uom_id': fields.many2one('product.uom', string='UOM'),
        'included_users_qty': fields.integer(string='included_users_qty'),
        'additional_user_price': fields.float(string='additional_user_price'),
        'additional_user_product_id': fields.many2one('product.product', string='additional_user_product_id', context={'default_type':'saas','default_saas_subtype':'extra_user'}, domain=[('type','=','saas'),('saas_subtype','=','extra_user')]),
        'saas_subtype': fields.selection([(u'product', 'product'), (u'extra_user', 'extra_user'), (u'additional', 'additional')], string='saas_subtype'),
        'instance_id': fields.one2many('saas_manager.instance', 'product_id', string='&lt;no label&gt;'), 
        'product_module_ids': fields.one2many('saas_manager.product_module', 'product_id', string='product_module_ids'), 
        'additional_product_ids': fields.one2many('product.product', 'saas_product_id', string='additional_product_ids', context={'default_type':'saas','default_saas_subtype':'additional'}, domain=[('type','=','saas'),('saas_subtype','=','additional')]), 
        'saas_product_id': fields.many2one('product.product', string='saas_product_id'), 
    }

    _defaults = {
    }


    _constraints = [
    ]




product()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
