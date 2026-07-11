FROM odoo:16

USER root
COPY ./invoicingbackend /mnt/extra-addons/invoicingbackend
COPY ./docker/odoo.conf /etc/odoo/odoo.conf
RUN chown -R odoo:odoo /mnt/extra-addons
USER odoo

EXPOSE 8069
