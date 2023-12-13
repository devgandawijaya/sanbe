from odoo.http import request

def _get_action_id(name, model_id):
    action_model = request.env['ir.actions.server'].sudo()

    action_id = action_model.create({
        'name': name,
        'usage': 'ir_cron',
        'state': 'code',
        'model_id': model_id.id
    })
    action_model.env.cr.commit()

    return action_id