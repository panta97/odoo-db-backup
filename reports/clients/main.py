def cliente_puntos(limit):
    query = """
    select
       rp.display_name cliente,
       rp.loyalty_points puntos
    from res_partner rp
    where rp.id <> 47932 -- CLIENTES VARIOS out
        and rp.doc_type = '1' -- DNI only
        and rp.loyalty_points is not  null
    order by puntos desc
    limit {limit};
    """.format(
        limit=limit
    )
    return query


def cliente_descuentos(series, limit):
    query = """
    with t_ai as
    (
        select
            ai.partner_filtered_id,
            ail.price_total discount,
            substr(ai.number, 0, 5) serie
        from account_invoice ai
        join account_invoice_line ail
            on ai.id = ail.invoice_id
        where ai.type in ('out_invoice')
            and ail.price_total < 0
    )
    select
        ai.serie caja,
        rp.display_name cliente,
        sum(ai.discount) descuentos
    from res_partner rp
    inner join t_ai ai
        on rp.id = ai.partner_filtered_id
    where rp.id <> 47932 -- CLIENTES VARIOS out
        and rp.doc_type = '1' -- DNI only
        and ai.serie in ({series})
    group by rp.id, rp.display_name, ai.serie
    order by descuentos asc
    limit {limit};
    """.format(
        series=series, limit=limit
    )
    return query


def cliente_descuentos_all(series, limit):
    query = """
    with t_ai as
    (
        select
            ai.partner_filtered_id,
            ail.price_total discount,
            substr(ai.number, 0, 5) serie
        from account_invoice ai
        join account_invoice_line ail
            on ai.id = ail.invoice_id
        where ai.type in ('out_invoice', 'out_refund')
            and ail.price_total < 0
    )
    select
        rp.display_name cliente,
        sum(ai.discount) descuentos
    from res_partner rp
    inner join t_ai ai
        on rp.id = ai.partner_filtered_id
    where rp.id <> 47932 -- CLIENTES VARIOS out
        and rp.doc_type = '1' -- DNI only
        and ai.serie in ({series})
    group by rp.id, rp.display_name
    order by descuentos asc
    limit {limit};
    """.format(
        series=series, limit=limit
    )
    return query


def cliente_compras(series, limit):
    query = """
    with t_ai as
    (
        select
            ai.partner_filtered_id,
            ai.amount_total,
            substr(ai.number, 0, 5) serie
        from account_invoice ai
        where ai.type in ('out_invoice', 'out_refund')
    )
    select
        ai.serie caja,
        rp.display_name cliente,
        sum(ai.amount_total) compras
    from res_partner rp
    inner join t_ai ai
        on rp.id = ai.partner_filtered_id
    where rp.id <> 47932 -- CLIENTES VARIOS out
        and rp.doc_type = '1' -- DNI only
        and ai.serie in ({series})
    group by rp.id, rp.display_name, ai.serie
    order by compras desc
    limit {limit};
    """.format(
        series=series, limit=limit
    )
    return query


def cliente_compras_all(series, limit):
    query = """
    with t_ai as
    (
        select
            ai.partner_filtered_id,
            case when ai.type = 'out_invoice'
                then ai.amount_total
                else -ai.amount_total
            end amount_total,
            substr(ai.number, 0, 5) serie
        from account_invoice ai
        where ai.type in ('out_invoice', 'out_refund')
    )
    select
        rp.display_name cliente,
        sum(ai.amount_total) compras
    from res_partner rp
    inner join t_ai ai
        on rp.id = ai.partner_filtered_id
    where rp.id <> 47932 -- CLIENTES VARIOS out
        and rp.doc_type = '1' -- DNI only
        and ai.serie in ({series})
    group by rp.id, rp.display_name
    order by compras desc
    limit {limit};
    """.format(
        series=series, limit=limit
    )
    return query
