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


{   'active': False,
    'author': u'Sistemas ADHOC',
    'category': u'base.module_category_knowledge_management',
    'demo_xml': [],
    'depends': [u'mail', u'product', u'account', u'contacts'],
    'description': u'Saas Manager',
    'init_xml': [],
    'installable': True,
    'license': 'AGPL-3',
    'name': u'Saas Manager',
    'test': [],
    'update_xml': [   u'security/saas_manager_group.xml',
                      u'view/instance_additional_view.xml',
                      u'view/product_view.xml',
                      u'view/instance_user_view.xml',
                      u'view/instance_view.xml',
                      u'view/instance_period_view.xml',
                      u'view/product_module_view.xml',
                      u'view/partner_view.xml',
                      u'view/saas_manager_menuitem.xml',
                      u'data/instance_additional_properties.xml',
                      u'data/product_properties.xml',
                      u'data/instance_user_properties.xml',
                      u'data/instance_properties.xml',
                      u'data/instance_period_properties.xml',
                      u'data/product_module_properties.xml',
                      u'data/partner_properties.xml',
                      u'data/instance_additional_track.xml',
                      u'data/product_track.xml',
                      u'data/instance_user_track.xml',
                      u'data/instance_track.xml',
                      u'data/instance_period_track.xml',
                      u'data/product_module_track.xml',
                      u'data/partner_track.xml',
                      u'workflow/instance_workflow.xml',
                      'security/ir.model.access.csv'],
    'version': u'1.1',
    'website': ''}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
