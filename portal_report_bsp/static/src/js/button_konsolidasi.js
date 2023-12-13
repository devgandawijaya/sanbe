odoo.define('portal_report_bsp.buttonKonsolidasi', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var viewRegistry = require('web.view_registry');
    var rpc = require('web.rpc'); // Include RPC for server calls

    var TreeButton = ListController.extend({
        buttons_template: 'button_konsolidasi_create.buttons',
        events: _.extend({}, ListController.prototype.events, {
            'click .open_konsolidasi_action': '_OpenKonsolidasi',
        }),
        _OpenKonsolidasi: function () {
            var self = this;
            // Using RPC call to get the base URL
            rpc.query({
                model: 'ir.config_parameter',
                method: 'get_param',
                args: ['web.base.url']
            }).then(function (base_url) {
                // Using template literal for URL formation
                var redirect_url = `${base_url}/import/konsolidasi`;
                self.do_action({
                    type: 'ir.actions.act_url',
                    url: redirect_url,
                    target: 'self'
                });
            });
        }
    });

    var KonsolidasiListView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: TreeButton,
        }),
    });

    viewRegistry.add('button_data_konsolidasi_list', KonsolidasiListView);
});
