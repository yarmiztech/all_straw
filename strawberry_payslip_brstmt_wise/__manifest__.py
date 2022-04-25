# -*- coding: utf-8 -*-
{
    'name': "Strawberry Purchase Type",
    'author':
        'Enzapps',
    'summary': """
This module will help to create Cash and Credit Purchase without Validation.
""",

    'description': """
        This module will help to create Cash and Credit Purchase without Validation.
    """,
    'website': "",
    'category': 'base',
    'version': '14.0',
    'depends': ['base', 'hr_expense', 'stock', 'account', 'boraq_company_branches', 'sale', 'om_hr_payroll','purchase','strawberry_overtime','payslip_payment_journal'],
    "images": [],
    'data': [
        "security/ir.model.access.csv",
        "data/seq.xml",
        'views/branch_payslip.xml',
        'views/purchase.xml'
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
}
