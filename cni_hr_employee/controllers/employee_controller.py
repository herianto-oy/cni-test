from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager

class EmployeePortal(CustomerPortal):
    @http.route(['/my/employee'], type='http', auth='user', website=True)
    def portal_employee(self, redirect=None, **post):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.employee_id.address_id
        employee = request.env.user.employee_id
        values.update({
            'error': {},
            'error_message': [],
        })

        if post and request.httprequest.method == 'POST':
            partner.sudo().write({
                'street': post.get('street', False),
                'street2': post.get('street2', False),
                'city': post.get('city', False),
                'zip': post.get('zipcode', False),
                'state_id': post.get('state_id', False),
                'country_id': post.get('country_id', False)

            })
            employee.sudo().write({
                'name': post.get('name', False),
                'marital': post.get('marital', False)
            })
           
            return request.redirect('/my/home')

        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])
        maritals = request.env['hr.employee']._fields['marital'].selection
        
        values.update({
            'maritals': maritals,
            'partner': partner,
            'employee': employee,
            'countries': countries,
            'states': states,
            'redirect': redirect,
            'page_name': 'employee',
        })

        response = request.render("cni_hr_employee.portal_my_employee", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response