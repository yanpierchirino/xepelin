# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class Complement(models.Model):
    _name = "res.complement"
    _description = "Test Complement Data"
    _rec_name = "concept"

    concept = fields.Char(string='Concepto', required=True)
    type = fields.Char(string='Tipo', required=True)
    account = fields.Char(string='Cuenta', required=True)
    tax_information = fields.Char(string='Información sobre impuestos', required=True)
    date = fields.Date(string="Fecha", required=True)
    company_id = fields.Many2one('res.company', string='Empresa', required=True, default=lambda self: self.env.company)
    reconciled_ids = fields.One2many("res.reconciled", "complement_id", string="Conciliacion")
    reconcilie_count = fields.Integer(compute="_compute_reconcilie_count")

    def _compute_reconcilie_count(self):
        for rec in self:
            rec.reconcilie_count = len(rec.reconciled_ids)

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