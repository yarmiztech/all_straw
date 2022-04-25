from odoo import fields,models,api,_
from odoo.tests.common import Form
from datetime import datetime
from odoo.exceptions import UserError, ValidationError
from calendar import monthrange


class Employee(models.Model):
    _inherit = "hr.employee"

    overtime_monthly = fields.Float(string='OT Monthly(Value)')
    overtime_hrs = fields.Float(string='OT Duration(Hrs)')


class Contract(models.Model):
    _inherit = 'hr.contract'

    overtime_monthly = fields.Float(string='OT Monthly(Value)')
    overtime_hrs = fields.Float(string='OT Duration(Hrs)')
    offmonth_amount = fields.Float(string="Off Month")

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def action_payslip_done(self):
        res = super(HrPayslip, self).action_payslip_done()
        print(self)
        self.employee_id.overtime_hrs =0
        self.employee_id.overtime_monthly =0
        for contract in self.employee_id.contract_ids:
            contract.overtime_hrs =0
            contract.overtime_monthly =0
            contract.offmonth_amount =0

    # def compute_sheet(self):
    #     res  = super(HrPayslip, self).compute_sheet()
    #     if self:
    #         if self.date_to.day-self.date_from.day:
    #            total = self.date_to.day-self.date_from.day
    #            if total <=22:
    #                for contract in self.employee_id.contract_ids:
    #                    num_days = monthrange(self.date_to.year, self.date_to.month)[1]
    #                    perday = contract.wage/num_days
    #                    notworking = num_days-total
    #                    contract.offmonth_amount = perday*notworking
    #
