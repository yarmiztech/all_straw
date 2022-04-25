# -*- coding: utf-8 -*-
{
    'name': "Strawberry Overtime",
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
    'depends': ['base', 'hr_expense', 'stock', 'account','hr_contract','boraq_company_branches', 'om_hr_payroll','purchase'],
    "images": [],
    'data': [
        "security/ir.model.access.csv",
        "data/seq.xml",
        'views/hr.xml',
        'views/straw_ot.xml'
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
}
