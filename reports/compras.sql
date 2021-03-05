select numero_odoo,
        proveedor,
        numero_factura,
        fecha_factura,
        fecha_vencimiento,
        venta,
        igv,
        importe,
        case
            when estado = 'open' then 'abierto'
            when estado = 'paid' then 'pagado'
            else estado end estado
from (
            select number                        numero_odoo,
                rp.name                       proveedor,
                concat('F', right(ai.l10n_pe_doc_serie, length(ai.l10n_pe_doc_serie) - 1), '-',
                        ai.l10n_pe_doc_number) numero_factura,
                date_invoice                  fecha_factura,
                date_due                      fecha_vencimiento,
                amount_untaxed                venta,
                amount_tax                    igv,
                amount_total                  importe,
                ai.state                      estado
            from account_invoice ai
                    left join res_partner rp
                            on ai.partner_filtered_id = rp.id
            where ai.type = 'in_invoice'
            and ai.journal_sunat_type = '01'
        ) t
order by fecha_factura
