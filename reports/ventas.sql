select aj.sunat_payment_type,
       aj.code,
       ai.l10n_pe_doc_number,
       ai.date_invoice,
       rp.id,
       rp.doc_type,
       rp.doc_number,
       rp.display_name,
       rp.street,
       rp.email,
       ai.amount_total,
       ai.partner_filtered_id,
       ai.sunat_amount_total_allowance,
       ai.amount_igv,
       ai.amount_total,
       ai.refund_invoice_id,
       ai.document_type,
       ail.product_id,
       ail.name,
       ail.uom_id,
       ail.quantity,
       ail.price_unit,
       ail.tax_igv,
       ail.price_total
from account_invoice_line ail
         left join account_invoice ai
                   on ail.invoice_id = ai.id
         left join account_journal aj
                   on ai.journal_id = aj.id
         left join res_partner rp
                   on ai.partner_filtered_id = rp.id
