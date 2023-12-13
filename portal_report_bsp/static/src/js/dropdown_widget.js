odoo.define('portal_report_bsp.dropdown_widget', function (require) {
    "use strict";

    var core = require('web.core');
    var ListRenderer = require('web.ListRenderer');
    var fieldRegistry = require('web.field_registry');
    var dom = require('web.dom');

    var QWeb = core.qweb;
    var _t = core._t;

    var DropdownWidget = ListRenderer.extend({
        events: _.extend({}, ListRenderer.prototype.events, {
            'click .dropdown-trigger': '_onDropdownClick',
        }),

        _renderRow: function (record) {
            var $row = this._super.apply(this, arguments);
            var $dropdownCell = $('<td>')
                .addClass('dropdown-cell')
                .append($('<div>')
                    .addClass('dropdown-trigger')
                    .html('⋮'));
            $row.append($dropdownCell);
            return $row;
        },

        _onDropdownClick: function (ev) {
            var $target = $(ev.currentTarget);
            var $row = $target.closest('tr');
            var recordId = $row.data('id');

            if (recordId) {
                var record = this._getRecord(recordId);

                if ($row.length) {
                    if ($row.hasClass('show-details')) {
                        $row.removeClass('show-details');
                    } else {
                        $row.addClass('show-details');
                    }
                }
            } else {
                console.error("Record ID tidak ditemukan untuk baris ini.");
            }
        },

        _renderSelector: function (tag, disableInput) {
            var $content = dom.renderCheckbox();
            if (disableInput) {
                $content.find("input[type='checkbox']").prop('disabled', disableInput);
            }
            return $('<' + tag + '>')
                .addClass('o_list_record_selector')
                .append($content);
        },

        async _renderView() {
            const oldPagers = this.pagers;
            let prom;
            let tableWrapper;
            if (this.state.count > 0 || !this.noContentHelp) {
                this.pagers = [];
                const orderedBy = this.state.orderedBy;
                this.hasHandle = orderedBy.length === 0 || orderedBy[0].name === this.handleField;
                this._computeAggregates();
                const $table = $('<table class="o_list_table table table-sm table-hover table-striped"/>');
                $table.toggleClass('o_list_table_grouped', this.isGrouped);
                $table.toggleClass('o_list_table_ungrouped', !this.isGrouped);
                const defs = [];
                this.defs = defs;
                if (this.isGrouped) {
                    $table.append(this._renderHeader());
                    $table.append(this._renderGroups(this.state.data));
                    $table.append(this._renderFooter());
                } else {
                    $table.append(this._renderHeader());
                    $table.append(this._renderBody());
                    $table.append(this._renderFooter());
                }
                tableWrapper = Object.assign(document.createElement('div'), {
                    className: 'table-responsive',
                });
                tableWrapper.appendChild($table[0]);
                delete this.defs;
                prom = Promise.all(defs);
            }
            await Promise.all([this._super.apply(this, arguments), prom]);
            this.el.innerHTML = "";
            this.el.classList.remove('o_list_optional_columns');
            oldPagers.forEach(pager => pager.destroy());
            if (tableWrapper) {
                this.el.appendChild(tableWrapper);
                if (document.body.contains(this.el)) {
                    this.pagers.forEach(pager => pager.on_attach_callback());
                }
                if (this._shouldRenderOptionalColumnsDropdown()) {
                    this.el.classList.add('o_list_optional_columns');
                    this.$('table').append(
                        $('<i class="o_optional_columns_dropdown_toggle fa fa-ellipsis-v"/>')
                    );
                    this.$el.append(this._renderOptionalColumnsDropdown());
                }
                if (this.selection.length) {
                    const $checked_rows = this.$('tr').filter(
                        (i, el) => this.selection.includes(el.dataset.id)
                    );
                    $checked_rows.find('.o_list_record_selector input').prop('checked', true);
                    if ($checked_rows.length === this.$('.o_data_row').length) {
                        this.$('thead .o_list_record_selector input').prop('checked', true);
                    }
                }
            }
            if (!this._hasContent() && !!this.noContentHelp) {
                this._renderNoContentHelper();
            }
        },
    });

    fieldRegistry.add('dropdown_widget', DropdownWidget);

    return DropdownWidget;
});
