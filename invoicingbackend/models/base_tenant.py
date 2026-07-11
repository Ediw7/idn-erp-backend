from odoo import models, fields, api


class BaseTenantModel(models.AbstractModel):
    _name = "invoicingbackend.base_tenant"
    _description = "Base Tenant Model for Multi-Company"

    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )
