# -*- coding: utf-8 -*-

from openerp import models, fields

class Order(models.Model)
    _name = 'helpdesk.order'

    partner_id = fields.Many2one(
        'res.partner', string='Employee_Manager',
        default=lambda self: self.env.user.company_id.partner_id)
    name = field.Char(string="Tile", required=True)
    content = field.Text(string="Description", required=True)
    state = fields.Selection([
        ('deleted', "Deleted"),
        ('solved', "Solved"),
        ('open', "Open"),
    ], default='open')

    @api.multi
    def write(self, vals):
        res = super(Order, self).write(vals)
        if vals.get('partner_id'):
            self.message_subscribe([vals['partner_id']])
        return res

    @api.model
    def create(self, vals):
        registration = super(Order, self).create(vals)
        registration.sudo().confirm_registration()
        return registration

    @api.multi
    def action_open(self):
        self.state = 'open'

    @api.multi
    def action_solved(self):
        self.state = 'solved'

    @api.multi
    def action_deleted(self):
        self.state = 'deleted'


class Answer(models.Model)
    _name = 'helpdesk.answer'

    order_id = fields.Many2one(
        'helpdesk.order', string='Order', required=True,
        readonly=True)
    user_id = fields.Many2one(
        'res.users', string='Agent_Manager',
        default=lambda self: self.env.user)
    name = fields.Char(related='order_id.name')
    description = fields.Text(related='order_id.content')
    message = field.Char(string="Message", required=True)

    @api.multi
    def write(self, vals):
        res = super(Answer, self).write(vals)
        if vals.get('user_id'):
            self.message_subscribe([vals['user_id']])
        return res

    @api.model
    def create(self, vals):
        registration = super(Order, self).create(vals)
        registration.sudo().confirm_registration()
        return registration


class Track_Follow(models.Model)
    _name = 'helpdesk.track_follow'

    order_id = fields.Many2one(
        'helpdesk.order', string='Order', required=True,
        readonly=True)
    user_id = fields.Many2one(
        'res.users', string='Agent_Manager',
        default=lambda self: self.env.user)
    partner_id = fields.Many2one(
        'res.partner', string='Employee_Manager',
        default=lambda self: self.env.user.company_id.partner_id)
    name = fields.Char(related='order_id.name')
    state = fields.Selection(related='order_id.state')
