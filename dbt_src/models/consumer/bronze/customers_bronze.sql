SELECT
    CAST("CUST_ID" AS VARCHAR) AS "CUST_ID",
    CAST("FIRST_NAME" AS VARCHAR(50)) AS "FIRST_NAME",
    CAST("LAST_NAME" AS VARCHAR(75)) AS "LAST_NAME",
    CAST("EMAIL" AS VARCHAR(75)) AS "EMAIL",
    CAST("PHONE" AS VARCHAR(25)) AS "PHONE",
    CAST("DOB" AS DATE) AS "DOB",
    CAST("MARITAL_STATUS" AS VARCHAR(25)) AS "MARITAL_STATUS",
    CAST("ADDRESS" AS VARCHAR(100)) AS "ADDRESS",
    CAST("CITY" AS VARCHAR(75)) AS "CITY",
    CAST("COUNTY" AS VARCHAR(75)) AS "COUNTY",
    CAST("STATE_PROVINCE" AS VARCHAR(75)) AS "STATE_PROVINCE",
    CAST("POSTAL_CODE" AS VARCHAR(25)) AS "POSTAL_CODE",
    CAST("COUNTRY" AS VARCHAR(75)) AS "COUNTRY",
    CAST("IS_ACTIVE" AS BOOLEAN) AS "IS_ACTIVE",
    CAST("CREATED_AT" AS TIMESTAMP) AS "CREATED_AT",
    TRY_CAST("UPDATED_AT" AS TIMESTAMP) AS "UPDATED_AT",
    TRY_CAST("DELETED_AT" AS TIMESTAMP) AS "DELETED_AT"
FROM {{ source('customers_raw', 'customersynthdata') }}