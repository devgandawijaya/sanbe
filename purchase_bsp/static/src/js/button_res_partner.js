odoo.define('portal_report_bsp.buttonResPartner', function (require) {
    "use strict";
    var KanbanController = require('web.KanbanController');
    var KanbanView = require('web.KanbanView');
    var viewRegistry = require('web.view_registry');
    var rpc = require('web.rpc'); // Include RPC for server calls

    var KanbanButton = KanbanController.extend({
        buttons_template: 'button_res_partner_create.buttons',
        events: _.extend({}, KanbanController.prototype.events, {
            'click .open_res_partner_action': '_OpenResPartner',
        }),
        _OpenResPartner: function () {
            var self = this;
            // Using RPC call to get the base URL
            rpc.query({
                model: 'ir.config_parameter',
                method: 'get_param',
                args: ['web.base.url']
            }).then(function (base_url) {
                // Using template literal for URL formation
                var redirect_url = `${base_url}/import-prinsipal-partner`;
                self.do_action({
                    type: 'ir.actions.act_url',
                    url: redirect_url,
                    target: 'self'
                });
            });
        }
    });

    var ResPartnerKanbanView = KanbanView.extend({
        config: _.extend({}, KanbanView.prototype.config, {
            Controller: KanbanButton,
        }),
    });

    viewRegistry.add('button_res_partner_list', ResPartnerKanbanView);
});
