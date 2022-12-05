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
