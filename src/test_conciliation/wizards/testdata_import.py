# -*- coding: utf-8 -*-

import io
import datetime
import pandas as pd

from base64 import b64decode
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons.test_conciliation.const import *


class TestdataImportWizard(models.TransientModel):
    _name = 'testdata.import.wizard'
    _description = "Testdata Import wizard"

    file = fields.Binary(string="Archivo", attachment=False)
    filename = fields.Char(string="Archivo")
    date = fields.Date(string="Fecha", default=fields.Date.context_today)
    user_id = fields.Many2one("res.users", string="Usuario", default=lambda self: self.env.uid)

    def action_import(self):
        model = self._context.get('model')
        if not model or model not in OPTIONS.keys():
            raise ValidationError(_("Ocurrio un problema al procesar la importación.\
                \nConsulte a su administrador de sistema para mas información."))
        
        master_obj = self.env[model]
        book_stream = io.BytesIO(b64decode(self.file))
        book = pd.read_excel(book_stream)
        self._check_file(book, model)
        
        try:
            values = book.to_dict(orient='records')
            #Check lines
            for line in values:
                domain = [(k,'=',line[k]) for k in line.keys()]
                rec = master_obj.search(domain)
                if rec:
                    raise ValidationError(_("La linea con los datos %s se encuentra duplicado." % list(line.items())))

            master_obj.create(values)
        except Exception as e:
            raise ValidationError(_(e))

        #RUN reconcilie
        self._run_reconciliation()
       
        act_windows = "test_conciliation.%s_action_window" % model.replace(".","_")
        return self.env.ref(act_windows).read()[0]

    def _check_file(self, book, model):
        errors = []
        filename = OPTIONS[model]['filename']
        fields = OPTIONS[model]['fields']

        if self.filename != filename:
            errors.append(_("- El nombre y tipo de archivo debe ser igual a 'master.xlsx'"))

        if not book.filter(regex="Unname").empty:
            errors.append(_("- Se encontro una ó varias columnas sin nombre."))

        if book.isnull().values.any():
            errors.append(_("- Se encontro una ó varias celdad sin datos."))

        try:
            book[fields]
        except Exception as e:
            errors.append(_(e.args[0]))

        #Check if bank ID exist
        if 'bank_id' in fields:
            bank_ids = [int(i) for i in set((book['bank_id'].values))]
            bank_res = self.env['res.bank'].search([('id','in',bank_ids)]).ids
            bank_diff = [i for i in bank_ids if i not in bank_res]
            if bank_diff:
                errors.append(_("- Los Ids %s de banco no se encuentran en el sistema." % bank_diff))

        #Check if country ID exist
        if 'country_id' in fields:
            country_ids = [int(i) for i in set((book['country_id'].values))]
            country_res = self.env['res.country'].search([('id','in',country_ids)]).ids
            country_diff = [i for i in country_ids if i not in country_res]
            if country_diff:
                errors.append(_("- Los Ids %s de pais no se encuentran en el sistema." % country_diff))

        if errors:
            message = "\n".join(errors)
            raise ValidationError(message)

    def _run_reconciliation(self):
        master_ids = self.env['res.master'].search([('reconciled_ids','=',False)])
        master_ids.reconcile()
