from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager

class PayrollPortal(CustomerPortal):
    def _prepare_home_portal_values(self):
        values = super(PayrollPortal, self)._prepare_home_portal_values()
        values['payslip_count'] = request.env['hr.payslip'].search_count([('employee_id.user_id', '=', request.env.user.id)])
        return values

    @http.route(['/my/payslip', '/my/payslip/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_hr_payslip(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_portal_layout_values()

        searchbar_sortings = {
            'date': {'label': 'Newest', 'order': 'create_date desc, id desc'},
            'name': {'label': 'Name', 'order': 'number asc, id asc'},
        }

         # default sort by value
        if not sortby:
            sortby = 'date'
        domain = [('employee_id.user_id', '=', request.env.user.id)]
       
        request.env['hr.payslip']
        # count for pager
        payslip_count = request.env['hr.payslip'].search_count(domain)
       
        # make pager
        pager = portal_pager(
            url="/my/payslip",
            url_args={'date_begin': date_begin, 'date_end': date_end},
            total=payslip_count,
            page=page,
            step=self._items_per_page
        )
  
        # search the purchase orders to display, according to the pager data
        payslip_ids = request.env['hr.payslip'].search(
            domain,
            order=searchbar_sortings[sortby]['order'],
            limit=self._items_per_page,
            offset=pager['offset']
        )

        values.update({
            'payslip_ids': payslip_ids,
            'page_name': 'payslip',
            'pager': pager,
            'default_url': '/my/payslip',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })

        return request.render("cni_hr_employee.portal_my_payslips", values)

    @http.route(['/my/payslip/<int:order_id>'], type='http', auth="public", website=True)
    def portal_payroll_download(self, order_id, report_type=None, access_token=None, message=False, download=False, **kw):
        try:
            payslip_sudo = self._document_check_access('hr.payslip', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('pdf'):
            return self._show_report(model=payslip_sudo, report_type=report_type, report_ref='om_hr_payroll.action_report_payslip', download=download)
