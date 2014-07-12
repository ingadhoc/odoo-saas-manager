from openerp.osv import orm

class product(orm.Model):
    _name = 'product.product'
    _inherit = ['product.product','website.seo.metadata']