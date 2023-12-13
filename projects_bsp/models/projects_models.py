# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import timedelta

class ProjectsModel(models.Model):
    _inherit = 'project.task'
    
    story_point = fields.Integer(string='Story Point', default=1)

    @api.onchange('story_point')
    def _onchange_story_point(self):
        # Calculate the deadline based on the story_point field value
        if self.story_point:
            # Assuming 2 hours for each story point
            hours_for_story_point = 2
            deadline_hours = self.story_point * hours_for_story_point

            # Update the date_deadline field
            if self.date_assign:
                self.date_deadline = fields.Datetime.to_string(fields.Datetime.from_string(self.date_assign) + timedelta(hours=deadline_hours))
            else:
                # If date_assign is not set, you may want to handle this case accordingly
                pass