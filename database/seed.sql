INSERT IGNORE INTO users (name, username, email, password, role) VALUES
('System Administrator', 'admin', 'admin@gmail.com', 'pbkdf2:sha256:600000$Pm5YehQrbcOvU9AI$68a8939db8fbc7e0f1337f1b45c5f8361b06d03a2ce3799c0e2aaf242799feb1', 'admin'),
('Farmer Demo', NULL, 'farmer@gmail.com', 'pbkdf2:sha256:600000$W9BsuYMHuPJFhbcg$d7fae3c05f398dbe2b7fcfd8fd875cb423fba8d24d7d97925d376a2b8055386c', 'farmer');

INSERT IGNORE INTO crops (id, name, soil, climate, rainfall, ph, season, `yield`, description, image) VALUES
('rice', 'Rice', 'Clayey Soil', 'Warm & Humid', '100-250 cm', '5.5-7.0', 'Kharif (July-November)', '50-60 quintals/hectare', 'Rice is a staple food crop that requires clayey soil with high water content and warm temperature.', '/static/images/rice.jpg'),
('wheat', 'Wheat', 'Loamy Soil', 'Temperate', '50-100 cm', '6.0-7.5', 'Rabi (October-March)', '40-50 quintals/hectare', 'Wheat grows well in loamy soil with moderate rainfall. It''s a winter crop.', '/static/images/wheatcrop.jpg'),
('corn', 'Corn (Maize)', 'Loamy Soil', 'Warm', '50-100 cm', '6.0-7.5', 'Kharif (May-September)', '40-50 quintals/hectare', 'Maize prefers well-drained loamy soil and sunny weather. High yield crop.', '/static/images/Ears-corn.jpg'),
('sunflower', 'Sunflower', 'Loamy & Sandy Soil', 'Warm & Dry', '50-75 cm', '6.0-7.5', 'Summer (February-May)', '15-20 quintals/hectare', 'Sunflower is an oil crop that adapts well to various soils.', '/static/images/sunflower.jpg'),
('cotton', 'Cotton', 'Deep Loamy Soil', 'Warm & Dry', '50-100 cm', '6.0-7.5', 'Kharif (May-October)', '15-20 quintals/hectare', 'Cotton requires well-drained deep loamy soil and warm climate.', '/static/images/cotton.jpg'),
('soybean', 'Soybean', 'Loamy & Clayey Soil', 'Warm', '50-100 cm', '6.0-7.0', 'Kharif (June-October)', '15-25 quintals/hectare', 'Soybean is a protein-rich legume crop suited for loamy soils.', '/static/images/soybean.jpg'),
('sugarcane', 'Sugarcane', 'Loamy & Clayey Soil', 'Warm & Humid', '100-150 cm', '5.5-7.0', 'Year-round (12 months)', '60-70 tonnes/hectare', 'Sugarcane requires rich fertile soil and warm humid climate.', '/static/images/sugarcane.jpg');

INSERT IGNORE INTO soils (id, name, color, texture, ph, fertility, moisture, best_crops, description, image) VALUES
('black soil', 'Black Soil', 'Dark Black', 'Clay', '5.5-8.5', 'High', 'High', 'Cotton, Sugarcane, Wheat', 'Black soil is rich in minerals and organic matter. Excellent for cotton and sugarcane.', '/static/images/black soil.jpg'),
('clayey soil', 'Clayey Soil', 'Brown/Grey', 'Fine', '6.0-8.5', 'High', 'Very High', 'Rice, Wheat, Sugarcane', 'Clayey soil retains moisture and nutrients. Perfect for rice cultivation.', '/static/images/claysoil.jpg'),
('red soil', 'Red Soil', 'Reddish', 'Medium', '5.5-7.5', 'Medium', 'Low', 'Groundnut, Millets, Pulses', 'Red soil is laterite and acidic. Suitable for groundnut and pulses.', '/static/images/red soil.jpg'),
('sandy soil', 'Sandy Soil', 'Light Brown', 'Coarse', '6.0-8.0', 'Low', 'Very Low', 'Carrots, Peanuts, Watermelon', 'Sandy soil drains quickly but lacks nutrients. Needs more fertilizer.', '/static/images/sandysoil.jpg'),
('loamy soil', 'Loamy Soil', 'Brown', 'Medium', '6.0-7.5', 'Very High', 'Good', 'Wheat, Corn, Vegetables', 'Loamy soil is ideal for most crops. Best for overall agriculture.', '/static/images/loamy soil.jpg'),
('silt soil', 'Silt Soil', 'Light Yellow', 'Fine', '6.5-8.0', 'Medium', 'Good', 'Wheat, Rice, Vegetables', 'Silt soil is soft and fertile. Good water retention and drainage.', '/static/images/silt-soil.jpg');

INSERT IGNORE INTO fertilizers (id, name, type, npk, best_for, `usage`, precautions, image) VALUES
('urea', 'Urea', 'Nitrogenous', '46-0-0', 'Wheat, Rice, Maize', 'Use specifically for leafy growth and green color. Apply as top dressing.', 'Avoid direct contact with seeds. Store in a dry place to prevent caking.', '/static/images/images.jpg'),
('dap', 'DAP (Diammonium Phosphate)', 'Phosphate', '18-46-0', 'Cotton, Sugarcane, Pulses', 'Best applied at planting time to promote strong root development.', 'Can cause seed damage if placed too close. Use recommended dosage.', '/static/images/images (1).jpg'),
('mop', 'MOP (Muriate of Potash)', 'Potash', '0-0-60', 'Potatoes, Tomatoes, Fruits', 'Improves fruit quality and disease resistance. Apply during crop growth.', 'Can cause chloride toxicity in sensitive crops like tobacco.', '/static/images/about.jpg'),
('npk_complex', 'NPK Complex', 'Balanced', '10-26-26', 'Vegetables, Orchards, Cash Crops', 'Balanced supply of major nutrients. Suitable for basal application.', 'Apply evenly. Avoid over-application to prevent nutrient runoff.', '/static/images/about2.jpg');

INSERT IGNORE INTO market_data (id, crop, variety, price_val, trend, `change`, display_order) VALUES
('rice', 'Rice (Paddy)', 'Basmati', 3200, 'up', '+2.5%', 1),
('wheat', 'Wheat', 'Sharbati', 2800, 'up', '+1.2%', 2),
('corn', 'Corn (Maize)', 'Hybrid', 1950, 'down', '-0.5%', 3),
('cotton', 'Cotton', 'BT Cotton', 7500, 'up', '+5.0%', 4),
('soybean', 'Soybean', 'Yellow', 4600, 'stable', '0.0%', 5),
('sugarcane', 'Sugarcane', 'Variety 86032', 315, 'up', '+1.0%', 6),
('sunflower', 'Sunflower', 'Oilseed', 6400, 'down', '-2.1%', 7);

INSERT IGNORE INTO transactions (id, user_email, crop_id, crop_name, action, price, quantity, total, status, created_at) VALUES
(1, 'farmer@gmail.com', 'rice', 'Rice (Paddy)', 'BUY', 3200, 5, 16000, 'Confirmed', '2026-09-24 09:30:00'),
(2, 'farmer@gmail.com', 'wheat', 'Wheat', 'SELL', 2800, 10, 28000, 'Processing', '2026-09-24 11:45:00');

INSERT IGNORE INTO farmer_queries (id, name, email, subject, message, status, created_at) VALUES
(1, 'Farmer Demo', 'farmer@gmail.com', 'Soil pH & Fertilizer Recommendation', 'My field has Black Soil with pH around 7.5. Which fertilizer combination gives best yield for Cotton?', 'Pending', '2026-09-24 10:15:00'),
(2, 'Ramesh Kumar', 'ramesh@kisan.in', 'Wheat Seeds Variety Inquiry', 'Are certified Sharbati wheat seeds available for the upcoming Rabi season in the market?', 'Resolved', '2026-09-24 11:30:00');
