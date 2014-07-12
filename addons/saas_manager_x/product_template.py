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

class template(osv.osv):
    """"""
    
    _inherit = 'product.template'

    _columns = {
        'type': fields.selection([('product','Stockable Product'),('consu', 'Consumable'),('service','Service'),('saas', 'SaaS')], 'Product Type', required=True, help="Consumable: Will not imply stock management for this product. \nStockable product: Will imply stock management for this product.. \nSaaS product: For SaaS Products."),
    }

    _defaults = {
    }


    _constraints = [
    ]




template()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
