odoo.define('portal_report_bsp.buttonProductCategory', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var viewRegistry = require('web.view_registry');
    var rpc = require('web.rpc'); // Include RPC for server calls

    var TreeButton = ListController.extend({
        buttons_template: 'button_product_category_create.buttons',
        events: _.extend({}, ListController.prototype.events, {
            'click .open_product_category_action': '_OpenProductCategory',
        }),
        _OpenProductCategory: function () {
            var self = this;
            // Using RPC call to get the base URL
            rpc.query({
                model: 'ir.config_parameter',
                method: 'get_param',
                args: ['web.base.url']
            }).then(function (base_url) {
                // Using template literal for URL formation
                var redirect_url = `${base_url}/import/product/category`;
                self.do_action({
                    type: 'ir.actions.act_url',
                    url: redirect_url,
                    target: 'self'
                });
            });
        }
    });

    var ProductCategoryListView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: TreeButton,
        }),
    });

    viewRegistry.add('button_product_category_list', ProductCategoryListView);
});
