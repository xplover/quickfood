DROP TABLE IF EXISTS foods;

CREATE TABLE foods 
(
    food_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL ,
    price INTEGER NOT NULL,
    Restaurant TEXT,
    info TEXT
);

INSERT INTO foods (name, price, Restaurant, info)
VALUES 
    ('SEMOLINE GNOCCHI', 11.99, 'La Cucina Italian Restaurant', 'Pepperonata, goat cheese and basil'),
    ('SPINACH AND FETA STUFFED CHICKEN', 12.99, 'La Cucina Italian Restaurant', 'With lemon, parsely, and Butter sauce'),
    ('CLASSIC CHICKEN STRONGANOF', 12.99, 'La Cucina Italian Restaurant', 'With parsely butter rice'),
    ('GRILLED RED SNAPPER', 13.99, 'La Cucina Italian Restaurant', 'With quinoa and potato mesh, sauce vierge'),
    ('GRILLED TIGER PRAWN', 14.99, 'La Cucina Italian Restaurant', 'With Crab mear Rissoto'),
    ('MARGHERITA CLASSIC PIZZA', 8.99, 'La Cucina Italian Restaurant', 'With extra cheese'),
    ('Miso Glaze Salmon', 15.99, 'Shanghai Chinese Restaurant', 'With butter haricot beans and water chestnut'),
    ('CRISPY DISH ROLLS', 6.99, 'Shanghai Chinese Restaurant', 'With Spring onions, Cucumber and Duck Sauce'),
    ('CRISPY BROCOLLI SANDWICH', 5.99, 'Shanghai Chinese Restaurant', 'Chilli Mayo, Chopped Brocolli and tempura crumbs'),
    ('SPICY AVOCADO AND TUNA', 7.99, 'Shanghai Chinese Restaurant', 'Hot Sriracha, Spicy mayo, Tuna, Coriander, and Avacado'),
    ('SMOKY EEL', 9.99, 'Shanghai Chinese Restaurant', 'Avocado, Chives, Eel, Seseme seeds, and Teriyaki Glaze'),
    ('SASHIMI ON ICE BOWL', 14.99, 'Shanghai Chinese Restaurant', 'Yellowfin Tuna, Salmon, and Chilean Sea Bass'),
    ('HO FAN NOODLES', 8.99, 'Shanghai Chinese Restaurant', 'With Chilli Oil, and Bejing black bean sauce'),
    ('FRIED FISH', 12.99, 'Spicy Indian Restaurant', 'Semolina crusted fillet from town of karwar, with Green and Red Chutni.'),
    ('CHEESY CHICKEN TIKKA', 16.99, 'Spicy Indian Restaurant', 'Creamy chicken morsels with cheese with Green and Red Chutni.'),
    ('SHAMI KABAB', 12.99, 'Spicy Indian Restaurant', 'Lamb and lentil patties, mildly spiced  with Green and Red Chutni.'),
    ('CREAMY BROCOLLI', 8.99, 'Spicy Indian Restaurant', 'Brocolli florets marinated in cream  with Green and Red Chutni.'),
    ('CHICKEN TIKKA MASALA', 14.99, 'Spicy Indian Restaurant', 'World famous boneless chicken tikka dish  with Green and Red Chutni.'),
    ('CHICKEN BIRYANI', 12.99, 'Spicy Indian Restaurant', 'Long grain rice cooked with chicken  with Green and Red Chutni.');


DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL
);


DROP TABLE IF EXISTS comments;

CREATE TABLE comments
(
    food_id INTEGER,
    name TEXT NOT NULL,
    comment TEXT NOT NULL
);