SELECT * FROM blog_items;

-- adds new column for the dates
ALTER TABLE blog_items ADD COLUMN new_date DATE;

-- transforms values in date column to new_date
UPDATE blog_items
SET new_date = STR_TO_DATE(`date`, '%M %e, %Y');

-- drop old date column
ALTER TABLE blog_items DROP COLUMN `date`;

-- rename date column (should have done earlier)
ALTER TABLE blog_items RENAME COLUMN new_date TO blog_post_date;