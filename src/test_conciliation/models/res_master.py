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
