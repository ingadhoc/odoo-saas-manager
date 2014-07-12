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


{   'active': False,
    'author': u'Sistemas ADHOC',
    'category': u'base.module_category_knowledge_management',
    'demo_xml': [],
    'depends': ['saas_manager_invoicing', 
                # 'web_nocreatedb', 
                'disable_openerp_online', 
                'cron_run_manually', 
                'web_saas_cust',
                'crm',
                'sale',
                'account_accountant',
                'website_saas_manager',
                ],
    'description': u"""
SaaS Manager
============ 
Requires:
--------- 
* Requiere instalar sudo oerpenv pip install openerp-client-lib
* lp:~sistemas-adhoc/openerp-l10n-ar-localization/7.0 --> l10n_ar_states 
* lp:server-env-tools/7.0 --> disable_openerp_online, cron_run_manually
* lp:web-addons/7.0 --> web_nocreatedb,

Important notes:
----------------
If reports do not contain headers, install the static version of wkhtmltopdf from https://code.google.com/p/wkhtmltopdf/.

Aditional Required configs on production
----------------------------------------
On settings/general activate password recovery
Install spanish language
Mod defaul language to es_AR
Set default timezone to 'America/Argentina/Buenos_Aires'

""",
    'init_xml': [],
    'installable': True,
    'license': 'AGPL-3',
    'name': u'Saas Manager Project',
    'test': [
            ],
    'update_xml': [   
                  ],
    'version': u'1.1',
    'website': ''}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
