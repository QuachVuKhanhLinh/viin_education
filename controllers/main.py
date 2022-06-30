import odoo
# import logging
# _logger = logging.getLogger(__name__)

class MyLinhAPI(odoo.http.Controller):
    @odoo.http.route('/linh', auth='public')
    def linh_handler(self):
        print(self)
        return "Welcome to 'linh' API!"