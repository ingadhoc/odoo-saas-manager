# import time
# from lxml import etree
# import openerp.addons.decimal_precision as dp
# import openerp.exceptions

# from openerp import netsvc
# from openerp import pooler
import openerplib
import openerp
import re
from openerp.tools.translate import _
from openerp.osv import fields, osv, orm
import openerp.addons.decimal_precision as dp
import xmlrpclib
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare

# from openerp.tools.translate import _


class instance(osv.osv):
    """"""
    
    matcher = re.compile(r'[^a-z0-9_]')

    _inherit = 'saas_manager.instance'

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'This name is already assigned. You must choose another one.'),
    ]

    def _special_match(self, strg):
        return not bool(self.matcher.search(strg))
    
    def _check_special_character_in_name(self, cr, uid, ids, context=None):
        for instance_it in self.browse(cr, uid, ids, context=context):
            if not self._special_match(instance_it.name):
                return False
        return True

    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        res = {}
        date_order = time.strftime(DEFAULT_SERVER_DATE_FORMAT)    
        for record in self.browse(cr, uid, ids, context=context):
            res[record.id] = {}
            val = 0.0
            cur = record.partner_id.property_product_pricelist.currency_id
            
            # Users
            amount_users = 0.0
            additional_user_price = 0.0
            additional_users = 0
            active_users = len(record.instance_user_ids)
            included_users_qty = record.product_id.included_users_qty
            if active_users > record.product_id.included_users_qty:
                additional_users = active_users - record.product_id.included_users_qty
            if record.product_id.additional_user_product_id:
                additional_user_price = self.pool.get('product.pricelist').price_get(cr, uid, [record.pricelist_id.id],
                        record.product_id.additional_user_product_id.id, 1.0, record.partner_id.id, {
                            'uom': record.product_id.additional_user_product_id.uom_id.id,
                            'date': date_order,
                            })[record.pricelist_id.id] 
                amount_users = additional_user_price * additional_users
            res[record.id]['included_users_qty'] = included_users_qty
            res[record.id]['additional_user_price'] = cur_obj.round(cr, uid, cur, additional_user_price)
            res[record.id]['amount_users'] = cur_obj.round(cr, uid, cur, amount_users)
            res[record.id]['additional_users'] = additional_users

            # Additionals
            additional_ammount = 0.0
            for additional in record.instance_additional_ids:
                additional_ammount += additional.additional_price
            res[record.id]['additional_ammount'] = cur_obj.round(cr, uid, cur, additional_ammount) 
            
            # Product
            product_price = self.pool.get('product.pricelist').price_get(cr, uid, [record.pricelist_id.id],
                    record.product_id.id, 1.0, record.partner_id.id, {
                        'uom': record.product_id.uom_id.id,
                        'date': date_order,
                        })[record.pricelist_id.id]
            res[record.id]['product_price'] = cur_obj.round(cr, uid, cur, product_price)
            
            # Subtotal
            subtotal = product_price + amount_users + additional_ammount
            res[record.id]['subtotal'] = cur_obj.round(cr, uid, cur, subtotal)

            amount_tax = subtotal * (1 - (record.discount or 0.0) / 100.0)
            taxes = tax_obj.compute_all(cr, uid, record.tax_id, amount_tax, 1, record.product_id, record.partner_id)
            for c in taxes['taxes']:
                val += c.get('amount', 0.0)
            res[record.id]['amount_untaxed'] = cur_obj.round(cr, uid, cur, amount_tax)
            res[record.id]['amount_tax'] = cur_obj.round(cr, uid, cur, val)
            res[record.id]['amount_total'] = cur_obj.round(cr, uid, cur, taxes['total_included']) 
        return res        

    _constraints = [
        (_check_special_character_in_name, 'Error: Instances name cannot contain spaces or special characters',
            ['name']),
    ]

    def get_full_name(self, cr, uid, ids, field_name, arg, context=None):
        return dict(self.name_get(cr, uid, ids, context=context)) 

    _columns = {
            'image': fields.related('partner_id', 'image', string="Image", type='binary', store=True),
            'url': fields.function(get_full_name, type="char", string='URL'),
        # TODO. Could be good to add states restricion "readonly=True, states={'draft': [('readonly', False)]}"" to all this fields
            'product_price': fields.function(_amount_all, string='Product Price', digits_compute= dp.get_precision('Product Price'), multi='sums'),            
            'amount_users': fields.function(_amount_all, string='Users Subtotal', digits_compute= dp.get_precision('Account'), multi='sums'),
            'additional_users': fields.function(_amount_all, type='integer', string='Additional Users', digits_compute= dp.get_precision('Account'), multi='sums'),
            'included_users_qty': fields.function(_amount_all, type='integer', string='Included Users', digits_compute= dp.get_precision('Account'), multi='sums'),
            'additional_user_price': fields.function(_amount_all, string='Additional User Price', digits_compute= dp.get_precision('Account'), multi='sums'),
            'additional_ammount': fields.function(_amount_all, string='Additionals', digits_compute= dp.get_precision('Account'), multi='sums'),
            'subtotal': fields.function(_amount_all, string='Subtotal', digits_compute= dp.get_precision('Account'), multi='sums'),
            'amount_untaxed': fields.function(_amount_all, string='Untaxed Amount', digits_compute= dp.get_precision('Account'), multi='sums'),
            'amount_tax': fields.function(_amount_all, string='Taxes', digits_compute= dp.get_precision('Account'), multi='sums'),
            'amount_total': fields.function(_amount_all, string='Total', digits_compute= dp.get_precision('Account'), multi='sums'),
            'discount': fields.float('Discount (%)', digits_compute= dp.get_precision('Discount'),),
            'tax_id': fields.many2many('account.tax', 'instance_tax_rel', 'instance_id', 'tax_id', 'Taxes',),  
            'pricelist_id': fields.related('partner_id', 'property_product_pricelist', type='many2one', relation='product.pricelist', string='Pricelist'),
            'fiscal_position': fields.related('partner_id', 'property_account_position', type='many2one', relation='account.fiscal.position', string='Fiscal Position'),                      
            'currency_id': fields.related('pricelist_id', 'currency_id', type="many2one", relation="res.currency", string="Currency", readonly=True),
            }

    def name_get(self, cr, uid, ids, context=None):
        """Overrides orm name_get method"""
        if not isinstance(ids, list):
            ids = [ids]
        res = []
        if not ids:
            return res
        reads = self.read(cr, uid, ids, ['name'], context)
        param = self.get_parameters (cr, uid, ids)

        for record in reads:
            base_url = param[record['id']]['base_url']
            if record['name'] and base_url:
                name = record['name'] + '.' + base_url 
                res.append((record['id'], name))
            else:
                res.append((record['id'], ''))
        return res      

    def onchange_partner(self, cr, uid, ids, partner_id):
        v = {}
        

        if pricelist:
            val['pricelist_id'] = pricelist
        
        if partner_id:
            pricelist = part.property_product_pricelist and part.property_product_pricelist.id or False
            fiscal_position = part.property_account_position and part.property_account_position.id or False
            
            partner_obj = self.pool.get('res.partner')
            partner = partner_obj.browse(cr, uid, partner_id)
            
            if not partner:
                return {'value': v}
            
            if isinstance(partner, list):
                partner = partner[0]
            v['image'] = partner.image
            v['pricelist_id'] = pricelist
            v['fiscal_position'] = fiscal_position
        else:
            v['image'] = False       
        return {'value': v}

    def action_open(self, cr, uid, ids, *args):
        for instance in self.browse(cr, uid, ids):
            if instance.db_created:
                # TODO
                print 'reactivate users'
            else:
                ret = self.create_database(cr, uid, [instance.id])
                self.update_users(cr, uid, [instance.id])
        return True

    def product_id_change(self, cr, uid, ids, pricelist, product_id, partner_id=False, update_tax=True, fiscal_position=False, context=None):
        if not  partner_id:
            raise osv.except_osv(_('No Owner Defined!'), _('Before choosing a product,\n select an owner.'))
        context = context or {}
        warning = {}
        # product_uom_obj = self.pool.get('product.uom')
        # partner_obj = self.pool.get('res.partner')
        product_obj = self.pool.get('product.product')
        context = {'partner_id': partner_id}
        result = {}
        domain = {}

        if product_id:
            product_obj = product_obj.browse(cr, uid, product_id, context=context)

            fpos = fiscal_position and self.pool.get('account.fiscal.position').browse(cr, uid, fiscal_position) or False
            if update_tax: #The quantity only have changed
                result['tax_id'] = self.pool.get('account.fiscal.position').map_tax(cr, uid, fpos, product_obj.taxes_id)
            date_order = time.strftime(DEFAULT_SERVER_DATE_FORMAT)        
            result['product_free_periods'] = product_obj.free_periods
        else:
            # result['price_unit'] = False
            result['tax_id'] = False
            result['product_free_periods'] = False

        return {'value': result, 'domain': domain, 'warning': warning}


    def update_users(self, cr, uid, ids, *args):
        param = self.get_parameters (cr, uid, ids)
        for inst in self.browse(cr, uid, ids):
            connection = self.connect_to_openerp(cr, uid, inst.id, param)
            remote_user_model = connection.get_model("res.users")
            remote_group_model = connection.get_model("res.groups")
            for user in inst.instance_user_ids:
                remote_ids = remote_user_model.search([("login", "=", user.login)])
                vals = self._prepare_user(cr, uid, user)
                if not user.remote_id:
                    if not remote_ids:
                        user_id = remote_user_model.create(vals)
                        self.pool.get('saas_manager.instance_user').write(cr, uid, [user.id], {'remote_id': user_id})
                    else:                    
                        print 'Debo poner une excepection porque ya habria un usuario con ese nombre'
                else:
                    if not remote_ids or remote_ids[0] == user.remote_id:                        
                        remote_user_model.write([user.remote_id],vals)
                    else:
                        print 'Debo poner une excepection porque ya habria un usuario con ese nombre'
        return True

    def _prepare_user(self, cr, uid, user, groups=False, context=None):
        """Prepare the dict of values to create the new user
        """
        if context is None:
            context = {}
        user_vals = {
            'name': user.name,
            'login': user.login,
            'email': user.email,
            'active': user.active,
            'phone': user.phone or '',
            'mobile': user.mobile or '',
            # 'groups_id': [(6, 0, groups)],
        }
        return user_vals
                
    def connect_to_openerp(self, cr, uid, inst_id, parameters, context=None):
        param = parameters
        base_url = param[inst_id]['base_url']
        server_port = int(param[inst_id]['server_port'])
        admin_name = param[inst_id]['admin_name']
        admin_pass = param[inst_id]['admin_pass']
        database = param[inst_id]['database']
        #domain = database + '.' + param[inst_id]['base_url']
        domain = base_url
        connection = openerplib.get_connection(hostname=domain, database=database, \
            login=admin_name, password=admin_pass, port=server_port)
        return connection

    def get_parameters(self, cr, uid, ids):
        inst_parameters = {}
        for instance in self.browse(cr, uid, ids):
            inst_parameters[instance.id] = {
                'base_url': instance.product_id.base_url,
                'server_port': instance.product_id.server_port,
                'server_super_admin_pwd': instance.product_id.server_super_admin_pwd,
                'admin_name': instance.admin_name or instance.product_id.admin_name,
                'admin_pass': instance.admin_pass or instance.product_id.admin_pass,
                'template_db_name': instance.product_id.template_db_name,
                'database': instance.name or '',
            }
        return inst_parameters

    def create_database(self, cr, uid, ids):
        param = self.get_parameters(cr, uid, ids)
        for inst in self.browse(cr, uid, ids):
            if inst.db_created:
                continue

            if not param[inst.id] or not param[inst.id]['base_url']:
                raise openerp.exceptions.Warning(_('Unable to create database, not base URL defined.'))
            
            rpc_db_url = 'http://%s:%d/xmlrpc/db' % (param[inst.id]['base_url'], int(param[inst.id]['server_port']))
            template_db_name = param[inst.id]['template_db_name']
            server_super_admin_pwd = param[inst.id]['server_super_admin_pwd']
            new_db_name = inst.name
            
            if not template_db_name:
                raise openerp.exceptions.Warning(_('No template Database specified.'))
            if not server_super_admin_pwd:
                raise openerp.exceptions.Warning(_('No super admin password provided.'))
            if not new_db_name:
                raise openerp.exceptions.Warning(_('No new Database name specified.'))

            sock = xmlrpclib.ServerProxy(rpc_db_url)
            try:
                sock.duplicate_database(server_super_admin_pwd, template_db_name, new_db_name)
            except:
                # TODO Esto me daba error asi que lo tuve que comentar, no se para que estaba
                # print "Unexpected error: ", sys.exc_info()[0]
                raise openerp.exceptions.Warning(_('Unable to create Database.'))

            connection = self.connect_to_openerp(cr, uid, inst.id, param)
            sub_domain = inst.name + '.' + param[inst.id]['base_url']
            new_url = 'http://%s:%d/' % (sub_domain, int(param[inst.id]['server_port']))
            connection.get_model('ir.config_parameter').set_param('web.base.url', sub_domain)
            self.write(cr, uid, inst.id, {'db_created': True})
        return True

    def unlink(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        instances = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []

        for t in instances:
            if t['state'] in ['open', 'close']:
                raise openerp.exceptions.Warning(_('You cannot delete an instance that is on Open or Close State.'))
            else:
                unlink_ids.append(t['id'])

        osv.osv.unlink(self, cr, uid, unlink_ids, context=context)
        return True

    def button_dummy(self, cr, uid, ids, context=None):
        return True