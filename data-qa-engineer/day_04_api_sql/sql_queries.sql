-- 1. Retrieve all products with a price greater than 100
SELECT *
FROM products
WHERE price > 100;

-- 2. Find products with missing prices
SELECT *
FROM products
WHERE price IS NULL;

-- 3. Find duplicate products using product_url
SELECT product_url, count(*) as duplicate_count
FROM products
GROUP BY product_url
HAVING count(*) > 1;

-- 4. Find products with ratings outside the range 0–5
SELECT * 
FROM products
WHERE rating < 0 or rating > 5;

-- 5. Count products grouped by availability
SELECT availability, count(*) as product_count
FROM products
GROUP BY availability;

-- 6. Calculate the average product price
SELECT AVG(price) as average_price
FROM products;

-- 7. Retrieve products with their category names using INNER JOIN
SELECT
    p.id,
    p.title,
    p.price,
    c.category_name
FROM products p
INNER JOIN categories c 
ON p.category_id = c.category_id;

-- 8. Find products that have no matching category using LEFT JOIN
SELECT
    p.id,
    p.title,
    p.category_id
FROM products p
LEFT JOIN categories c
ON p.category_id = c.category_id
WHERE c.category_id IS NULL;


