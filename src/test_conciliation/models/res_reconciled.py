# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class Reconciled(models.Model):
    _name = 'res.reconciled'
    _description = "Reconciled"
    _rec_name = "display_name"

    display_name = fields.Char(string="Nombre", compute="_compute_name")
    master_id = fields.Many2one("res.master", string="Información sobre impuestos", required=True, ondelete="restrict")
    date = fields.Date(string="Fecha", required=True)
    company_id = fields.Many2one('res.company', string='Empresa', required=True, default=lambda self: self.env.company)
    amount = fields.Monetary(related="master_id.amount", string="Importe")
    bank_id = fields.Many2one("res.bank", related="master_id.bank_id", string="Banco")
    country_id = fields.Many2one("res.country", related="master_id.country_id", string="Pais")
    currency_id = fields.Many2one('res.currency', related="master_id.currency_id", string='Moneda')
    complement_id = fields.Many2one("res.complement", string='Concepto', required=True, ondelete="restrict")
    type = fields.Char(related="complement_id.type", string='Tipo')
    account = fields.Char(related="complement_id.account", string='Cuenta')

    def _compute_name(self):
        for rec in self:
            rec.display_name = "[%s] %s" %(rec.master_id.tax_information, rec.complement_id.concept)
