from odoo import fields,models,api
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

class PurchaseReportLine(models.Model):
    _name = 'purchase.report.line'

    name= fields.Char(default='Purchase Report',index=True)
    type = fields.Selection([('Day Book', 'Day Book'), ('Date Wise', 'Date Wise')], default='Day Book')
    from_date = fields.Date('From Date', default=datetime.now().date().strftime(DEFAULT_SERVER_DATETIME_FORMAT))
    to_date = fields.Date('To Date', default=datetime.now().date().strftime(DEFAULT_SERVER_DATETIME_FORMAT))
    date = fields.Date('Date', default=datetime.now().date().strftime(DEFAULT_SERVER_DATETIME_FORMAT))
    transaction_type = fields.Boolean(string='Transaction Type')
    transaction_type_purchase = fields.Boolean(string='Purchase',default=1)
    vendor = fields.Many2one('res.partner')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)
    purchase_report_lines = fields.One2many('purchase.report.lines','purchase_report_line')

    @api.onchange('from_date','to_date','date','vendor')
    def create_purchase_lines(self):
        if self.type == 'Day Book':
            if self.date:
                if self.transaction_type_purchase==True:
                    self.purchase_report_lines = None
                    # day_book=self.env['account.payment'].search([('date','=',self.date),('payment_type','=', 'outbound'),('state', '=', 'posted'),('partner_type','=', 'supplier')])
                    purchase_report = self.env['account.payment'].search([('date', '=', self.date), ('payment_type', '=', 'outbound'),('state','=','posted'),('partner_type', '=', 'supplier')])
                    book_lines_2 = []
                    for i in purchase_report:
                        line_2 = (0, 0, {
                            'date': i.date,
                            # 'description':'Local Purchase',
                            'description': i.name,
                            'source': i.ref,
                            'vendor': i.partner_id.name,
                            'invoice_amount': i.amount,
                            'debit': 0,
                            'credit': i.amount,
                        })
                        book_lines_2.append(line_2)
                    self.update({
                        'purchase_report_lines': book_lines_2
                    })
                    if self.vendor:
                        self.purchase_report_lines = None
                        # day_book=self.env['account.payment'].search([('date','=',self.date),('payment_type','=', 'outbound'),('state', '=', 'posted'),('partner_type','=', 'supplier')])
                        purchase_report = self.env['account.payment'].search([('date', '=', self.date), ('payment_type', '=', 'outbound'),('state', '=', 'posted'),('partner_type', '=', 'supplier'),('partner_id','=',self.vendor.name)])
                        book_lines_2 = []
                        for i in purchase_report:
                            line_2 = (0, 0, {
                                'date': i.date,
                                # 'description':'Local Purchase',
                                'description': i.name,
                                'source': i.ref,
                                'vendor': i.partner_id.name,
                                'invoice_amount': i.amount,
                                'debit': 0,
                                'credit': i.amount,
                            })
                            book_lines_2.append(line_2)
                        self.update({
                            'purchase_report_lines': book_lines_2
                        })
        if self.type == 'Date Wise':
            if self.from_date:
                if self.to_date:
                    if self.transaction_type_purchase==True:
                        self.purchase_report_lines = None
                        purchase_report = self.env['account.payment'].search(
                            [('date', '>=', self.from_date),('date', '<=', self.to_date), ('payment_type', '=', 'outbound'),('state','=','posted'),('partner_type', '=', 'supplier')])
                        book_lines = []
                        for i in purchase_report:
                            line_6 = (0, 0, {
                                'date': i.date,
                                'description': i.name,
                                'source': i.ref,
                                'vendor': i.partner_id.name,
                                'invoice_amount': i.amount,
                                'debit': 0,
                                'credit': i.amount,
                            })
                            book_lines.append(line_6)
                        self.update({
                            'purchase_report_lines': book_lines
                        })
                        if self.vendor:
                            if self.transaction_type_purchase == True:
                                self.purchase_report_lines = None
                                purchase_report = self.env['account.payment'].search([('date', '>=', self.from_date), ('date', '<=', self.to_date),('payment_type', '=', 'outbound'), ('state', '=', 'posted'),('partner_type', '=', 'supplier'),('partner_id','=',self.vendor.name)])
                                book_lines = []
                                for i in purchase_report:
                                    line_6 = (0, 0, {
                                        'date': i.date,
                                        'description': i.name,
                                        'source': i.ref,
                                        'vendor': i.partner_id.name,
                                        'invoice_amount': i.amount,
                                        'debit': 0,
                                        'credit': i.amount,
                                    })
                                    book_lines.append(line_6)
                                self.update({
                                    'purchase_report_lines': book_lines
                                })

    # @api.multi
    def print_purchase_report(self):
        return self.env.ref('advanced_common_day_book.purchase_report_en_ar').report_action(self)


class PurchaseReportLines(models.Model):
    _name = 'purchase.report.lines'

    purchase_report_line = fields.Many2one('purchase.report.line')
    date = fields.Date('Date')
    description = fields.Char('Description')
    source = fields.Char('Source')
    vendor = fields.Char('Vendor')
    invoice_amount = fields.Float('Invoice Amount')
    debit = fields.Float('Debit')
    credit = fields.Float('Credit')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)
