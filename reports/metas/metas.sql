with temp as
    (
    select
           EXTRACT(YEAR FROM ai.date_invoice) año,
           EXTRACT(MONTH FROM ai.date_invoice) mes,
           EXTRACT(WEEK FROM ai.date_invoice) semana,
           EXTRACT(DAY FROM ai.date_invoice) dia,
           case
                when pc.id in (2, 4, 5, 11, 17) then 'CABALLERO'
                when pc.id in (3, 6, 7, 12, 13, 15, 16) then 'DAMA'
                when pc.id in (9, 10, 14) then 'NINO y HOME'
                when pc.id = 8 then pc.name
                else 'OTROS'
            end general,
           ail.price_total venta,
           substr(ai.number, 0, 5) serie
    from account_invoice ai
    left join account_invoice_line ail
        on ai.id = ail.invoice_id
    left join product_product pp
        on ail.product_id = pp.id
    left join product_template pt
        on pp.product_tmpl_id = pt.id
    left join pos_category pc
        on pt.pos_categ_id = pc.id
    where ai.type = 'out_invoice' -- boletas y facturas
    )
select año, mes, semana, dia, general, sum(venta)
from temp
where general = ?
    and serie in (?)
group by año, mes, semana, dia, general
order by año, mes, dia;
