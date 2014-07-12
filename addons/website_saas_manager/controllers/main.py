# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-Today OpenERP SA (<http://www.openerp.com>).
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

from openerp import exceptions
from openerp import netsvc
from openerp import SUPERUSER_ID
from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp.osv import osv
from openerp.tools.translate import _

class ProductForm(object):
    mandatory_fields = ["instance_name"]
    
    def mandatory_fields(self):
        return self.mandatory_fields

    def optional_fields(self):
        return []

    def all_fields(self):
        return self.mandatory_fields() + self.optional_fields()

    def empty(self):
        return dict.fromkeys(self.all_fields(), '')

class Website(osv.Model):
    _inherit = "website"

    def preprocess_request(self, cr, uid, ids, request, context=None):
        product_obj = request.registry['product.product']
        product_ids = product_obj.search(cr, request.uid, [], context=request.context)

        request.context.update({
            'product_ids': product_obj.browse(cr, request.uid, product_ids, context=request.context)
        })

        return super(Website, self).preprocess_request(cr, uid, ids, request, context=None)


class website_saas_manager(http.Controller):

    @http.route(['/saas_products/'], type='http', auth="public", website=True, multilang=True)
    def saas_products(self, **post):
        cr, uid, context = request.cr, request.uid, request.context
        product_obj = request.registry['product.product']
        product_ids = product_obj.search(cr, request.uid, [('type','=','saas')], context=request.context)

        render_values = {
            'product_ids': product_obj.browse(cr, request.uid, product_ids, context=request.context)
        }

        return request.website.render("website_saas_manager.saas_products", render_values)

    @http.route(['/saas_product/<model("product.product"):product>/'], type='http', auth="public", website=True, multilang=True)
    def saas_product(self, product, error_message=None, instance_name=None, **post):
        cr, uid, context = request.cr, request.uid, request.context
        
        orm_instance = request.registry['saas_manager.instance']

        product_form = ProductForm()
        values = {
            'form_values': product_form.empty(),
            'error': {},
        }
        form_values = values['form_values']
        form_values.update(post)
        error = values['error']

        for field_name in product_form.mandatory_fields:
            if not form_values[field_name]:
                error[field_name] = 'Domain cannot be empty'

        if error:
            return request.website.render("website_sale.checkout", values)
        
        if instance_name and len(instance_name) == 0:
            error_message = 'Domain cannot be empty'
            return request.redirect("/saas_product/%s/?error_message=%s" % (product.id, error_message))

        
        if instance_obj.search(cr, uid, [], context=context):
            error_message = 'Domain cannot be empty'
            return request.redirect("/saas_product/%s/?error_message=%s" % (product.id, error_message))

        render_values = {
            'product': product,
        }
        
        if instance_name:
            render_values['instance_name'] = instance_name
        if error_message:
            render_values['error_message'] = error_message

        return request.website.render("website_saas_manager.saas_product", render_values)

    @http.route(['/saas_product/<model("product.template"):product>/register/'], type='http', auth="public", website=True, multilang=True)
    def register(self, product, instance_name, **post):
        cr, uid, context = request.cr, request.uid, request.context

        if not instance_name:
            error_message = 'Domain cannot be empty'
            return request.redirect("/saas_product/%s/?error_message=%s" % (product.id, error_message))

        instance_obj = request.registry['saas_manager.instance']
        if instance_obj.search(cr, uid, [], context=context):
            error_message = 'Domain cannot be empty'
            return request.redirect("/saas_product/%s/?error_message=%s" % (product.id, error_message))            
        
        user_obj = request.registry['res.users']
        user = user_obj.browse(cr, uid, uid, context=context)
        show_login = True
        if user.active:
            show_login = False

        render_values = {
            'product': product,
            'instance_name': instance_name,
            'user': user,
            'show_login': show_login,
        }
        return request.website.render("website_saas_manager.signup", render_values)

    @http.route(['/saas_product/<model("product.template"):product>/create/'], type='http', auth="public", website=True, multilang=True)
    def create(self, product, instance_name, login=None, name=None, password=None, confirm_password=None, **post):
        if not instance_name:
            error_message = 'Domain cannot be empty'
            return request.redirect("/saas_product/%s?error_message=%s" % (product.id, error_message))

        cr, uid, context = request.cr, request.uid, request.context

        user_obj = request.registry['res.users']
        user = user_obj.browse(cr, uid, uid, context=context)
        
        if not user.active:
            if not login or not name or not password or not confirm_password:
                error_message = _('You must provide all password.')
                return request.redirect("/saas_product/%s/register/?error_message=%s" % (product.id, error_message))
            
            model, group_portal_id = request.registry['ir.model.data'].get_object_reference(cr, 1, 'base', 'group_portal')
            user_vals = {
                'name': name,
                'login': login,
                'password': password,
                'groups_id': [(6, 0, [group_portal_id])],
            }
            user_obj.create(cr, 1, user_vals, context=context)

            #instance_user_obj = request.registry['saas_manager.instance_user']
            #instance_user_vals = {
            #    'name': name,
            #    'login': login,
            #}
            #instance_user_obj.create(cr, 1, instance_user_vals, context=context)

        return self.create_saas_instance(cr, uid, product, instance_name, user, context=context)

    def create_saas_instance(self, cr, uid, product, instance_name, user, context=None):
        instance_vals = {
            'name': instance_name,
            'partner_id': user.partner_id.id,
            'product_id': product.id,
        }
        instance_obj = request.registry['saas_manager.instance']
        instance_id = instance_obj.create(cr, 1, instance_vals, context=context)

        wf_service = netsvc.LocalService("workflow")
        #wf_service.trg_validate(1, 'saas_manager.instance', instance_id, 'sgn_require', cr)
        #wf_service.trg_validate(1, 'saas_manager.instance', instance_id, 'sgn_open', cr)
        
        instance = instance_obj.browse(cr, 1, instance_id, context=context)
        return request.redirect("http://%s" % instance.url)

