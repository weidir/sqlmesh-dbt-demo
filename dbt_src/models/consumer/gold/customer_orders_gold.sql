SELECT
    CUST."CUST_ID", -- Customer ID
    ORD."ORDER_COUNT_LIFETIME", -- Total order count for a customer over their lifetime
    ORD."ORDER_COUNT_LAST_12_MONTHS", -- Total order count for a customer over the last 12 months
    ORD."ORDER_COUNT_LAST_6_MONTHS", -- Total order count for a customer over the last 6 months
    ORD."ORDER_COUNT_LAST_3_MONTHS", -- Total order count for a customer over the last 3 months
    ORD."TOTAL_ORDER_VALUE_LIFETIME", -- Total order value for a customer over their lifetime
    ORD."TOTAL_ORDER_VALUE_LAST_12_MONTHS", -- Total order value for a customer over the last 12 months
    ORD."TOTAL_ORDER_VALUE_LAST_6_MONTHS", -- Total order value for a customer over the last 6 months
    ORD."TOTAL_ORDER_VALUE_LAST_3_MONTHS", -- Total order value for a customer over the last 3 months
    ORD."AVERAGE_ORDER_VALUE_LIFETIME", -- Average order value for a customer over their lifetime
    ORD."AVERAGE_ORDER_VALUE_LAST_12_MONTHS", -- Average order value for a customer over the last 12 months
    ORD."AVERAGE_ORDER_VALUE_LAST_6_MONTHS", -- Average order value for a customer over the last 6 months
    ORD."AVERAGE_ORDER_VALUE_LAST_3_MONTHS", -- Average order value for a customer over the last 3 months
    ORD."MAX_ORDER_VALUE_LIFETIME", -- Max order value for a customer over their lifetime
    ORD."MAX_ORDER_VALUE_LAST_12_MONTHS", -- Max order value for a customer over the last 12 months
    ORD."MAX_ORDER_VALUE_LAST_6_MONTHS", -- Max order value for a customer over the last 6 months
    ORD."MAX_ORDER_VALUE_LAST_3_MONTHS", -- Max order value for a customer over the last 3 months
    ORD."MIN_ORDER_VALUE_LIFETIME", -- Min order value for a customer over their lifetime
    ORD."MIN_ORDER_VALUE_LAST_12_MONTHS", -- Min order value for a customer over the last 12 months
    ORD."MIN_ORDER_VALUE_LAST_6_MONTHS", -- Min order value for a customer over the last 6 months
    ORD."MIN_ORDER_VALUE_LAST_3_MONTHS", -- Min order value for a customer over the last 3 months
    ORD."MOST_COMMON_PAYMENT_METHOD_LIFETIME", -- Most common payment method for a customer over their lifetime
    ORD."MOST_COMMON_PAYMENT_METHOD_LAST_12_MONTHS" -- Most common payment method for a customer over the last 12 months
FROM (
    SELECT * 
    FROM {{ ref("customers_silver") }}
    WHERE "IS_ACTIVE" = TRUE
) CUST
LEFT JOIN (
    SELECT 
        "CUST_ID", 
        -- Get total order count for a customer over their lifetime
        COUNT(*) AS "ORDER_COUNT_LIFETIME",
        -- Get total order count for a customer over the last 12 months
        COUNT(CASE WHEN ORDER_TMSTP >= DATEADD(month, -12, CURRENT_DATE) THEN 1 ELSE NULL END) AS "ORDER_COUNT_LAST_12_MONTHS",
        -- Get total order count for a customer over the last 6 months
        COUNT(CASE WHEN ORDER_TMSTP >= DATEADD(month, -6, CURRENT_DATE) THEN 1 ELSE NULL END) AS "ORDER_COUNT_LAST_6_MONTHS",
        -- Get total order count for a customer over the last 3 months
        COUNT(CASE WHEN ORDER_TMSTP >= DATEADD(month, -3, CURRENT_DATE) THEN 1 ELSE NULL END) AS "ORDER_COUNT_LAST_3_MONTHS",
        -- Get total order value for a customer over their lifetime
        SUM("ORDER_TOTAL") AS "TOTAL_ORDER_VALUE_LIFETIME",
        -- Get order value over last 12 months
        SUM(CASE WHEN ORDER_TMSTP >= DATEADD(month, -12, CURRENT_DATE) THEN order_total ELSE 0 END) AS "TOTAL_ORDER_VALUE_LAST_12_MONTHS",
        -- Get order value over last 6 months
        SUM(CASE WHEN ORDER_TMSTP >= DATEADD(month, -6, CURRENT_DATE) THEN order_total ELSE 0 END) AS "TOTAL_ORDER_VALUE_LAST_6_MONTHS",
        -- Get order value over last 3 months
        SUM(CASE WHEN ORDER_TMSTP >= DATEADD(month, -3, CURRENT_DATE) THEN order_total ELSE 0 END) AS "TOTAL_ORDER_VALUE_LAST_3_MONTHS",
        -- Get average order value for a customer over their lifetime
        AVG("ORDER_TOTAL") AS "AVERAGE_ORDER_VALUE_LIFETIME",
        -- Get average order value for a customer over the last 12 months
        AVG(CASE WHEN ORDER_TMSTP >= DATEADD(month, -12, CURRENT_DATE) THEN order_total ELSE NULL END) AS "AVERAGE_ORDER_VALUE_LAST_12_MONTHS",
        -- Get average order value for a customer over the last 6 months
        AVG(CASE WHEN ORDER_TMSTP >= DATEADD(month, -6, CURRENT_DATE) THEN order_total ELSE NULL END) AS "AVERAGE_ORDER_VALUE_LAST_6_MONTHS",
        -- Get average order value for a customer over the last 3 months
        AVG(CASE WHEN ORDER_TMSTP >= DATEADD(month, -3, CURRENT_DATE) THEN order_total ELSE NULL END) AS "AVERAGE_ORDER_VALUE_LAST_3_MONTHS",
        -- Get max order value for a customer over their lifetime
        MAX("ORDER_TOTAL") AS "MAX_ORDER_VALUE_LIFETIME",
        -- Get max order value for a customer over the last 12 months
        MAX(CASE WHEN ORDER_TMSTP >= DATEADD(month, -12, CURRENT_DATE) THEN order_total ELSE NULL END) AS "MAX_ORDER_VALUE_LAST_12_MONTHS",
        -- Get max order value for a customer over the last 6 months
        MAX(CASE WHEN ORDER_TMSTP >= DATEADD(month, -6, CURRENT_DATE) THEN order_total ELSE NULL END) AS "MAX_ORDER_VALUE_LAST_6_MONTHS",
        -- Get max order value for a customer over the last 3 months
        MAX(CASE WHEN ORDER_TMSTP >= DATEADD(month, -3, CURRENT_DATE) THEN order_total ELSE NULL END) AS "MAX_ORDER_VALUE_LAST_3_MONTHS",
        -- Get min order value for a customer over their lifetime
        MIN("ORDER_TOTAL") AS "MIN_ORDER_VALUE_LIFETIME",
        -- Get min order value for a customer over the last 12 months
        MIN(CASE WHEN ORDER_TMSTP >= DATEADD(month, -12, CURRENT_DATE) THEN order_total ELSE NULL END) AS "MIN_ORDER_VALUE_LAST_12_MONTHS",
        -- Get min order value for a customer over the last 6 months
        MIN(CASE WHEN ORDER_TMSTP >= DATEADD(month, -6, CURRENT_DATE) THEN order_total ELSE NULL END) AS "MIN_ORDER_VALUE_LAST_6_MONTHS",
        -- Get min order value for a customer over the last 3 months
        MIN(CASE WHEN ORDER_TMSTP >= DATEADD(month, -3, CURRENT_DATE) THEN order_total ELSE NULL END) AS "MIN_ORDER_VALUE_LAST_3_MONTHS",
        -- Get the most common purchase category for a customer
        MODE("PAYMENT_METHOD") AS "MOST_COMMON_PAYMENT_METHOD_LIFETIME",
        -- Get the most common purchase category for a customer over last 12 months
        MODE(CASE WHEN ORDER_TMSTP >= DATEADD(month, -12, CURRENT_DATE) THEN "PAYMENT_METHOD" ELSE NULL END) AS "MOST_COMMON_PAYMENT_METHOD_LAST_12_MONTHS"
    FROM {{ ref("orders_silver") }}
    WHERE "ORDER_STATUS" = 'COMPLETED'
    GROUP BY "CUST_ID"
) ORD
ON CUST."CUST_ID" = ORD."CUST_ID"