odoo.define('o_button_import_testdata.import_testdata', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var Dialog = require('web.Dialog');
    var rpc = require('web.rpc');
    var core = require('web.core');
    var _t = core._t;

    ListController.include({
        init: function () {
            this._super.apply(this, arguments);
        },

        renderButtons: function ($node) {
            this._super.apply(this, arguments);
            if (this.$buttons) {
                this.$buttons.find('.o_button_import_testdata').click(this.proxy('_import_testdata'));
            }
        },

        _import_testdata: function (e) {
            e.preventDefault();            
            var self = this;
            var context = self.initialState.context;
            context['model'] = self.modelName;
            self.do_action({
                type: 'ir.actions.act_window',
                name: _t('Asistente de Carga de datos'),
                res_model: 'testdata.import.wizard',
                views: [[false, 'form']],
                search_view_id: [false],
                target: 'new',
                domain: [],
                context: context
            });
        }
    });

});
