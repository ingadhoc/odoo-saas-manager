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

class product_module(osv.osv):
    """"""
    
    _name = 'saas_manager.product_module'
    _description = 'product_module'

    _columns = {
        'name': fields.char(string='name', required=True),
        'product_id': fields.many2one('product.product', string='product_id', ondelete='cascade', required=True), 
    }

    _defaults = {
    }


    _constraints = [
    ]




product_module()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
