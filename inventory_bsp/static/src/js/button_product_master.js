odoo.define('portal_report_bsp.buttonProductMaster', function (require) {
    "use strict";
    var KanbanController = require('web.KanbanController');
    var KanbanView = require('web.KanbanView');
    var viewRegistry = require('web.view_registry');
    var rpc = require('web.rpc'); // Include RPC for server calls

    var KanbanButton = KanbanController.extend({
        buttons_template: 'button_product_master_create.buttons',
        events: _.extend({}, KanbanController.prototype.events, {
            'click .open_product_master_action': '_OpenProductMaster',
        }),
        _OpenProductMaster: function () {
            var self = this;
            // Using RPC call to get the base URL
            rpc.query({
                model: 'ir.config_parameter',
                method: 'get_param',
                args: ['web.base.url']
            }).then(function (base_url) {
                // Using template literal for URL formation
                var redirect_url = `${base_url}/import/product`;
                self.do_action({
                    type: 'ir.actions.act_url',
                    url: redirect_url,
                    target: 'self'
                });
            });
        }
    });

    var ProductMasterKanbanView = KanbanView.extend({
        config: _.extend({}, KanbanView.prototype.config, {
            Controller: KanbanButton,
        }),
    });

    viewRegistry.add('button_product_master_list', ProductMasterKanbanView);
});
