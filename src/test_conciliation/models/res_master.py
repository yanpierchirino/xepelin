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

    @api.model
    def update_country_id(self, country_id=2):
        records = self.search([('country_id','!=',country_id)])
        records.write({'country_id': country_id})
