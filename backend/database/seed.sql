INSERT INTO states
(state_name,state_code)
VALUES
('Uttar Pradesh','UP');

INSERT INTO divisions
(division_name,state_id)
VALUES
('Varanasi',1);

INSERT INTO districts
(district_name,division_id)
VALUES
('Ghazipur',1);

INSERT INTO complaint_categories
(category_name)
VALUES
('Electricity');

INSERT INTO complaint_subcategories
(subcategory_name,category_id)
VALUES
('Transformer',1);

INSERT INTO complaint_priorities
(priority_name)
VALUES
('Medium');

INSERT INTO complaint_statuses
(status_name)
VALUES
('Pending');