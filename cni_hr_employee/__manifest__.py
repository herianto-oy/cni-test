# -*- coding: utf-8 -*-
{
    'name': "Odoo 13 CNI Employee",
    'summary': 'Employee For Odoo 13 Community Edition',
    'description': '',
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Generic Modules/Human Resources',
    'version': '0.1',
    'depends': ['base', 'website', 'hr', 'om_hr_payroll'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/payslip_template.xml',
        'views/employee_templates.xml',
    ],
}
