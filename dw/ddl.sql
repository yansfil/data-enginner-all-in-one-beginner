-- Create an 'order_items' table
CREATE TABLE public.order_items (
	id int4 NULL,
	order_id int4 NULL,
	user_id int4 NULL,
	product_id int4 NULL,
	inventory_item_id int4 NULL,
	status varchar(50) NULL,
	created_at timestamp NULL,
	shipped_at timestamp NULL,
	delivered_at timestamp NULL,
	returned_at timestamp NULL,
	sale_price float4 NULL
);


-- Create an 'monthly_revenue' table
CREATE TABLE public.monthly_revenue (
	id int4 NULL,
	date date NOT NULL,
    total_revenue float4 NOT NULL, 
    total_cnt int4 NOT NULL,
    created_at timestamp NOT NULL DEFAULT NOW()
);

