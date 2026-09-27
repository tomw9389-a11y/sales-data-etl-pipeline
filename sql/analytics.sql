-- QUERY: daily_revenue
SELECT sale_date,
       ROUND(SUM(revenue), 2) AS revenue,
       SUM(quantity) AS units_sold,
       COUNT(DISTINCT transaction_id) AS transactions
FROM sales
GROUP BY sale_date
ORDER BY sale_date;

-- QUERY: category_performance
SELECT category,
       ROUND(SUM(revenue), 2) AS revenue,
       SUM(quantity) AS units_sold
FROM sales
GROUP BY category
ORDER BY revenue DESC;

-- QUERY: top_products
SELECT product_id,
       product_name,
       ROUND(SUM(revenue), 2) AS revenue,
       SUM(quantity) AS units_sold
FROM sales
GROUP BY product_id, product_name
ORDER BY revenue DESC
LIMIT 5;

-- QUERY: store_performance
SELECT store_id,
       ROUND(SUM(revenue), 2) AS revenue,
       COUNT(DISTINCT transaction_id) AS transactions,
       ROUND(SUM(revenue) / COUNT(DISTINCT transaction_id), 2) AS avg_transaction_value
FROM sales
GROUP BY store_id
ORDER BY revenue DESC;
