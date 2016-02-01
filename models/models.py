# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Order(models.Model)
    _name = 'helpdesk.order'

    partner_id = fields.Many2one(
        'res.partner', string='Employee_Manager',
        default=lambda self: self.env.user.partner_id.id)
    company_id = fields.Many2one(
        'res.partner', string='Employee_Manager',
        default=lambda self: self.env.user.partner_id.company_id.id)
    name = field.Char(string="Tile", required=True)
    content = field.Text(string="Description", required=True)
    state = fields.Selection([
        ('deleted', "Deleted"),
        ('solved', "Solved"),
        ('open', "Open"),
        ('tracked', "Tracked"),
    ], default='open')

    @api.multi
    def write(self, vals):
        res = super(Order, self).write(vals)
        if vals.get('partner_id'):
            self.message_subscribe([vals['partner_id']])
        return res

    @api.model
    def create(self, vals):
        res = super(Order, self).create(vals)
        res.sudo().confirm_registration()
        return registration


class Answer(models.Model)
    _name = 'helpdesk.answer'

    order_id = fields.Many2one(
        'helpdesk.order', string='Order', required=True,
        readonly=True)
    user_id = fields.Many2one(
        'res.users', string='Agent_Manager',
        default=lambda self: self.env.user.id)
    name = fields.Char(related='order_id.name')
    description = fields.Text(related='order_id.content')
    message = field.Text(string="Message", required=True)
    state = fields.Selection(related='order_id.state')

    @api.multi
    def action_message(self, vals):
        res = super(Answer, self).create(vals)
        res.sudo().confirm_registration()
        return res

    @api.multi
    def action_open(self):
        self.state = 'open'

    @api.multi
    def action_solved(self):
        self.state = 'solved'

    @api.multi
    def action_deleted(self):
        self.state = 'deleted'

    @api.multi
    def action_track(self):
        self.state = 'tracked'
        vals = {'order_id': self.order_id, 'user_id': self.env.user.id, 'name': self.name, 'state': self.state}
        self.pool.get('helpdesk.track_follow').create(vals)

    @api.multi 
    def action_assign(self):
        self.state = 'tracked'
        vals = {'order_id': self.order_id, 'user_id': self.env.user.id, 'name': self.name, 'state': self.state}
        self.pool.get('helpdesk.track_follow').create(vals)


class Track_Follow(models.Model)
    _name = 'helpdesk.track_follow'

    order_id = fields.Many2one(
        'helpdesk.order', string='Order', required=True,
        readonly=True)
    user_id = fields.Many2one(
        'res.users', string='Agent_Manager',
        default=lambda self: self.env.user.id)
    partner_id = fields.Many2one(
        'res.partner', string='Employee_Manager',
        default=lambda self: self.env.user.partner_id.id)
    name = fields.Char(related='order_id.name')
    state = fields.Selection(related='order_id.state')

    @api.multi
    def create(self, vals):
        res = super(Track_Follow, self).create(vals)
        res.sudo().confirm_registration()
        return res
