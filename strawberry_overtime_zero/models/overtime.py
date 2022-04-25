from odoo import fields,models,api,_
from odoo.tests.common import Form
from datetime import datetime
from odoo.exceptions import UserError, ValidationError

class OvertimeStrawberry(models.Model):
    _name = 'overtime.strawberry'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']

    name = fields.Char("Name", index=True, default=lambda self: _('New'))

    branch_id = fields.Many2one('company.branches', 'Branch Name')
    create_date = fields.Date(string='Create Date', default=fields.Date.context_today)

    user_id = fields.Many2one('res.users', 'Created By', required=True, default=lambda self: self.env.user)

    state = fields.Selection([('draft', 'Draft'),('approval', 'Requested'), ('validate', 'Approved'), ('cancelled', 'Cancelled')], readonly=True,default='draft')
    ot_type = fields.Selection([('montly', 'Montly'), ('day', 'Day')], default='montly',string="OT Type")
    overtime_straw_lines = fields.One2many('overtime.straw.lines','overtime_id')
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.company)
    date_from = fields.Date(string='Date from')
    date_to = fields.Date(string='Date To')

    def action_journal_invoices(self):
        return {
            'name': _('Payslips'),
            'view_mode': 'tree,form',
            'res_model': 'hr.payslip',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.payslip_ids.ids)],
        }



    def action_confirm(self):
        for line in self.overtime_straw_lines:
            line.hr_employee.overtime_monthly = line.total_ot_amount
            if line.hr_employee.contract_id:
                line.hr_employee.contract_id.overtime_monthly = line.total_ot_amount
                line.hr_employee.contract_id.overtime_hrs = line.total_hrs
            line.hr_employee.overtime_hrs = line.total_hrs

        self.write({'state':'validate'})

    @api.onchange('branch_id')
    def onchange_branch_id(self):
        self.overtime_straw_lines =False
        if self.branch_id:
            list = []
            for line in self.env['hr.employee'].search([('branch_id','=',self.branch_id.id)]):
                d = (0, 0, {
                    'hr_employee': line.id,
                    'wage': line.contract_id.wage,
                    'timesheet_cost': line.timesheet_cost,
                })
                list.append(d)
            self.overtime_straw_lines =list
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'overtime.strawberry') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('overtime.strawberry') or _('New')
        return super(OvertimeStrawberry, self).create(vals)
    def action_approval(self):
        self.write({'state':'approval'})



class OvertimeStrawberryLines(models.Model):
    _name = 'overtime.straw.lines'

    overtime_id = fields.Many2one('overtime.strawberry', 'Ref Name')
    hr_employee = fields.Many2one('hr.employee',string="Employee")
    total_hrs = fields.Integer(string="Total Hrs",compute='_compute_total_hrs_new')
    total_hrs_new = fields.Integer(string="Total Hrs New")
    perday_amount = fields.Integer(string="/DAY wages")
    wage = fields.Integer(string="Wages")
    total_ot_amount = fields.Integer(string="OT amount",compute='_compute_total_ot_amount')
    timesheet_cost = fields.Integer(string="Timesheet Cost")
    overtime_straw_dates = fields.One2many('overtime.straw.dates','overtime_id_date')

    # @api.depends('total_hrs','timesheet_cost')
    def _compute_total_ot_amount(self):
        for each in self:
            each.total_ot_amount = each.total_hrs*each.timesheet_cost




    def _compute_total_hrs_new(self):
        for each in self:
            if each.overtime_straw_dates:
                # each.total_hrs_new = sum(each.mapped('overtime_straw_dates').mapped('total_hrs'))
                each.total_hrs = sum(each.mapped('overtime_straw_dates').mapped('total_hrs'))
            else:
                # each.total_hrs_new =0
                each.total_hrs =0


class OvertimeStrawberryDates(models.TransientModel):
    _name = 'overtime.straw.dates'

    name = fields.Char("Name", index=True, default=lambda self: _('New'))
    date = fields.Date(string="Date")
    overtime_id_date = fields.Many2one('overtime.straw.lines', 'Ref Name')
    total_hrs = fields.Integer(string="Total Hrs")

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'overtime.straw.dates') or _('New')
            else:
                vals['name'] = str(vals['date'])
        return super(OvertimeStrawberryDates, self).create(vals)

    # @api.onchange('total_hrs')
    # def onchange_total_hrs(self):
    #     if self.total_hrs:
    #         self.overtime_id_date.total_hrs += self.total_hrs
    #

