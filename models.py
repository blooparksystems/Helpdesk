# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Order(models.Model):
    _name = 'helpdesk.order'

    partner_id = fields.Many2one(
        'res.partner', string='Employee',
        default=lambda self: self.env.user.partner_id.id, store=True, invisible="1")
    company_id = fields.Many2one(
        'res.partner', string='Company',
        default=lambda self: self.env.user.partner_id.company_id.id, store=True, invisible="1")
    name = fields.Char(string="Title", required=True, store=True)
    content = fields.Text(string="Description", required=True, store=True)
    states = fields.Selection([
        ('deleted', "Deleted"),
        ('solved', "Solved"),
        ('open', "Open"),
    ], default='open', store=True)

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
        return res

    @api.multi
    def action_solved(self):
        self.state = 'solved'

    @api.multi
    def action_deleted(self):
        self.state = 'deleted'

    @api.multi
    def action_track(self):
        vals = {'order_id': self.order_id, 'user_id': self.env.user.id, 'name': self.name, 'state': self.state}
        self.pool.get('helpdesk.track.follow').create(vals)

    @api.multi 
    def action_assign(self):
        vals = {'order_id': self.order_id, 'user_id': self.env.user.id, 'name': self.name, 'state': self.state}
        self.pool.get('helpdesk.track.follow').create(vals)


class Answer(models.Model):
    _name = 'helpdesk.answer'

    order_id = fields.Many2one(
        'helpdesk.order', string='Order', required=True,
        readonly=True)
    user_id = fields.Many2one(
        'res.users', string='Agent',
        default=lambda self: self.env.user.id, store=True)
    name = fields.Char(related='order_id.name', store=True)
    description = fields.Text(related='order_id.content', store=True)
    message = fields.Text(string="Message", required=True, domain=[('state', '=', 'open')], store=True)
    state = fields.Selection(related='order_id.state', store=True)

    @api.multi
    def action_message(self, vals):
        res = super(Answer, self).create(vals)
        res.sudo().confirm_registration()
        return res


class Track_Follow(models.Model):
    _name = 'helpdesk.track.follow'

    order_id = fields.Many2one(
        'helpdesk.order', string='Order', required=True,
        readonly=True, store=True)
    user_id = fields.Many2one(
        'res.users', string='Agent',
        default=lambda self: self.env.user.id, store=True)
    partner_id = fields.Many2one(
        'res.partner', string='Employee_Manager',
        default=lambda self: self.env.user.partner_id.id, store=True)
    name = fields.Char(related='order_id.name', store=True)
    state = fields.Selection(related='order_id.state', store=True)

    @api.multi
    def create(self, vals):
        res = super(Track_Follow, self).create(vals)
        res.sudo().confirm_registration()
        return res
