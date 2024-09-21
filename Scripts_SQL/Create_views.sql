

CREATE OR REPLACE VIEW public.notas_corretagem_redrex 
AS
WITH fatura_redrex AS (
    SELECT
         CASE cv
                    WHEN 'C' THEN 'Compra'
                    WHEN 'V' THEN 'Venda'
                    ELSE NULL
                END AS cv,
        TO_DATE("vecto", 'DDMMYYYY') AS vecto,
        Cast(n_nota as INT) as n_nota,
        TO_DATE("data_de_pregao", 'DDMMYYYY') AS data_de_pregao,
        CAST("qted" AS INT) AS qted,
        mercadoria as ticker,
        CAST(REPLACE("txop", ',', '.') AS DECIMAL) AS txop,
        CAST(REPLACE("cotacao", ',', '.') AS DECIMAL) AS cotacao
    FROM
        public.fatura_redrex
),

fatura_redrex_small AS (
      SELECT
         CAST("N Nota" AS INT) as n_nota,
         CAST(REPLACE(MAX(CASE WHEN "1" = 'IRR' THEN "2" END), ',', '.') AS DECIMAL) AS irr,
         CAST(REPLACE(MAX(CASE WHEN "1" = 'Ajuste' THEN "2" END), ',', '.') AS DECIMAL)  AS ajuste,
         CAST(REPLACE(MAX(CASE WHEN "1" = 'Tx Corretagem' THEN "2" END), ',', '.') AS DECIMAL)  AS tx_corretagem,
         CAST(REPLACE(MAX(CASE WHEN "1" = 'Taxa' THEN "2" END), ',', '.') AS DECIMAL)  AS taxa,
        TO_DATE("Data de Pregão", 'DDMMYYYY') AS data_de_pregao
    FROM
        public.fatura_redrex_small
    GROUP BY
        "N Nota", "Data de Pregão"
),
final AS (
    SELECT
       'Redrex' AS corretora,
        r.cv,
        r.n_nota,
        r.data_de_pregao,
        r.qted,
        r.ticker,
        r.txop,
        s.tx_corretagem,
        r.cotacao,
        CASE 
            WHEN r.cv = 'Compra' THEN -ROUND((r.qted * r.cotacao * (1 - (s.tx_corretagem + r.txop) / 100)), 2)
            WHEN r.cv = 'Venda' THEN ROUND((r.qted * r.cotacao * (1 - (s.tx_corretagem + r.txop) / 100)), 2)
            ELSE 0 -- Valor padrão caso cv não seja 'C' nem 'V'
        END AS movimentacao
    FROM
        fatura_redrex r
    JOIN
        fatura_redrex_small s
    ON
         r.n_nota = s.n_nota 
       AND r.data_de_pregao = s.data_de_pregao
)

SELECT  corretora,
        cv,
        cast (n_nota as INT) n_nota,
        cast(data_de_pregao AS DATE) data_de_pregao,
        cast(qted AS INT) qted,
        ticker,
        cast(txop AS FLOAT) txop,
        cast(tx_corretagem AS FLOAT) tx_corretagem,
        cast(cotacao AS FLOAT) cotacao,
        cast(movimentacao AS FLOAT) movimentacao
FROM final;



create or replace view public.notas_corretagem_jornada
AS
WITH fatura_jornada AS (SELECT CASE fatura_jornada.cv
                                   WHEN 'C' THEN 'Compra'
                                   WHEN 'V' THEN 'Venda'
                                   ELSE NULL
                                   END                                                               AS cv,
                               to_date(fatura_jornada.vecto, 'DDMMYYYY')                       AS vecto,
                               fatura_jornada.n_nota::integer                                        AS n_nota,
                               to_date(fatura_jornada.data_de_pregao, 'DDMMYYYY')              AS data_de_pregao,
                               fatura_jornada.qted::integer                                          AS qted,
                               fatura_jornada.mercadoria                                             AS ticker,
                               replace(fatura_jornada.txop, ',', '.')::numeric(10, 2)      AS txop,
                               replace(fatura_jornada.cotacao, ',', '.')::numeric(10, 2) AS cotacao
                        FROM public.fatura_jornada),
     fatura_jornada_small AS (SELECT fatura_jornada_small.n_nota::numeric(10, 2)                                          AS n_nota,
                                     replace(fatura_jornada_small.corretagem, ',', '.')::numeric(10, 2)  AS tx_corretagem,
                                     replace(fatura_jornada_small.taxa_de_registro, ',',
                                             '.')::numeric(10, 2)                                          AS taxa,
                                     to_date(fatura_jornada_small.data_de_pregao, 'DDMMYYYY')                 AS data_de_pregao
                              FROM public.fatura_jornada_small),
     final AS (SELECT 'Jornada' AS corretora,
                      r.cv,
                      r.n_nota,
                      r.data_de_pregao,
                      r.qted,
                      r.ticker,
                      r.txop,
                      s.tx_corretagem,
                      r.cotacao,
                      CASE
                          WHEN r.cv = 'Compra' THEN - round(r.qted * r.cotacao *
                                                                  (1 - (s.tx_corretagem + r.txop) / 100),
                                                                  2)
                          WHEN r.cv = 'Venda' THEN round(r.qted * r.cotacao *
                                                               (1 - (s.tx_corretagem + r.txop) / 100),
                                                               2)
                          ELSE 0
                          END         AS movimentacao
               FROM fatura_jornada r
                JOIN fatura_jornada_small s ON r.n_nota = s.n_nota AND r.data_de_pregao = s.data_de_pregao)
SELECT corretora,
       cv,
       n_nota,
       data_de_pregao,
       qted,
       ticker,
       txop         AS txop,
       tx_corretagem AS tx_corretagem,
       cotacao      AS cotacao,
       movimentacao AS movimentacao
FROM final;



--create view gold unindo todas as views
create or replace view notas_corretagem
AS
select * from notas_corretagem_jornada
union all 
select * from notas_corretagem_redrex
