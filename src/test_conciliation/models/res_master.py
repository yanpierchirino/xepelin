# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class Master(models.Model):
    _name = "res.master"
    _description = "Test Master Data"
    _rec_name = "tax_information"

    tax_information = fields.Char(string='Información sobre impuestos', required=True)
    date = fields.Date(string="Fecha", required=True)
    amount = fields.Monetary(string="Importe", required=True)
    bank_id = fields.Many2one("res.bank", string="Banco", required=True)
    country_id = fields.Many2one("res.country", string="Pais", required=True)
    company_id = fields.Many2one('res.company', string='Empresa', required=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Moneda', required=True, default=lambda self: self.env.company.currency_id)
    reconciled_ids = fields.One2many("res.reconciled", "master_id", string="Conciliacion")
    reconcilie_count = fields.Integer(compute="_compute_reconcilie_count")

    def _compute_reconcilie_count(self):
        for rec in self:
            rec.reconcilie_count = len(rec.reconciled_ids)

    def reconcile(self):
        reconcile_obj = self.env['res.reconciled']
        complement_obj = self.env['res.complement']
        for rec in self:
            complement_ids = complement_obj.search([
                ('tax_information','=',rec.tax_information),('date','=',rec.date)])
            if complement_ids:
                for complement in complement_ids:
                    reconcile_ids = reconcile_obj.search([
                        ('complement_id','=',complement.id),('master_id','=',rec.id)])
                    if not reconcile_ids:
                        reconcile_obj.create({
                            'master_id': rec.id,
                            'date': rec.date,
                            'complement_id': complement.id
                        })

    def action_view_reconcilie(self):
        reconciled = self.mapped('reconciled_ids')
        action = self.env["ir.actions.actions"]._for_xml_id("test_conciliation.res_reconciled_action_window")
        if len(reconciled) > 1:
            action['domain'] = [('id', 'in', reconciled.ids)]
        elif len(reconciled) == 1:
            form_view = [(self.env.ref('test_conciliation.res_reconciled_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = reconciled.id
        else:
            action = {'type': 'ir.actions.act_window_close'}

        return action

    @api.model
    def update_country_id(self, country_id=2):
        records = self.search([('country_id','!=',country_id)])
        records.write({'country_id': country_id})
