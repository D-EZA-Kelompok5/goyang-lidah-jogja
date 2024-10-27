# Format: query_id, menu_id, relevance_score
# Relevance scores:
# 3 = Perfect match
# 2 = Highly relevant
# 1 = Somewhat relevant
# 0 = Not relevant (not included in qrels to save space)

qrels = [
    # Makanan pedas (q1)
    ("q1", 11, 3),  # Ayam Woku Endes
    ("q1", 51, 3),  # Ayam Woku
    ("q1", 39, 3),  # Rica Ayam Kampung
    ("q1", 15, 2),  # Ayam Goreng Sambal Combrang
    ("q1", 12, 2),  # Ikan Baracuda Sambel Ijo
    ("q1", 36, 1),  # Javanese Fried Noodle
    
    # Hidangan vegetarian (q2)
    ("q2", 31, 3),  # Vegan Omelette
    ("q2", 59, 3),  # Salad Roll
    ("q2", 42, 3),  # Salad Mentimun
    ("q2", 32, 3),  # Fruit Salad
    ("q2", 60, 3),  # Smoothie Bowl
    ("q2", 86, 2),  # Lotek Kupat
    ("q2", 88, 2),  # Gado-Gado Kupat
    ("q2", 89, 2),  # Ketoprak
    
    # Menu seafood segar (q3)
    ("q3", 47, 3),  # Kepiting Saus Singapur
    ("q3", 48, 3),  # Udang Asam Manis
    ("q3", 12, 3),  # Ikan Baracuda Sambel Ijo
    ("q3", 97, 3),  # Udang Galah Masak Tauco
    ("q3", 98, 3),  # Udang Galah Saus Tiram
    ("q3", 96, 2),  # Gurame Semur
    ("q3", 99, 2),  # Gurame Bakar Sambal Dewa
    ("q3", 100, 2), # Gurame Lombok Ijo
    ("q3", 90, 2),  # Cumi Goreng Telur Asin
    
    # Makanan tradisional jawa (q4)
    ("q4", 66, 3),  # Gudeng Nasi Krecek Dan Telur Bebek
    ("q4", 67, 3),  # Gudeg Nasi Krecek Dan Chicken Wing
    ("q4", 68, 3),  # Gudeg Nasi Krecek Telur Bebek Dan Tahu
    ("q4", 69, 3),  # Gudeg Nasi Krecek Telur Bebek Dan Dada Ayam
    ("q4", 70, 3),  # Gudeg Nasi Krecek Telur Bebek Dan Ayam Suwir
    ("q4", 36, 2),  # Javanese Fried Noodle
    ("q4", 37, 2),  # Javanese Noodle Soup
    ("q4", 40, 2),  # Nasi Magelangan
    
    # Menu ayam (q5)
    ("q5", 1, 3),   # Ayam Kesuma
    ("q5", 2, 3),   # Ayam Sauce Areh
    ("q5", 11, 3),  # Ayam Woku Endes
    ("q5", 15, 3),  # Ayam Goreng Sambal Combrang
    ("q5", 51, 3),  # Ayam Woku
    ("q5", 55, 3),  # Picatta Chicken
    ("q5", 62, 3),  # Ayam Bumbu Rujak
    ("q5", 65, 3),  # Ayam Panggang Dada
    ("q5", 81, 3),  # Jogja Fried Chicken
    ("q5", 82, 3),  # Chicken Curry Sauce
    ("q5", 83, 3),  # Satay Ayam
    ("q5", 84, 3),  # Opor Ayam
    ("q5", 85, 3),  # Soto Ayam
    
    # Minuman kopi (q41)
    ("q41", 19, 3), # Espresso
    ("q41", 20, 3), # Coffee Crema
    ("q41", 33, 3), # Cup Coffee
    ("q41", 10, 3), # Turkish Coffee
    ("q41", 9, 2),  # Cappuccino With Oat Milk
    
    # Minuman dingin segar (q42)
    ("q42", 5, 3),  # Es Jeruk
    ("q42", 56, 3), # Power Plant
    ("q42", 57, 3), # Root Boost
    ("q42", 29, 3), # Strawberry Milkshakes
    ("q42", 58, 3), # Ice Almond Choco
    ("q42", 24, 2), # Soda Gembira
    
    # Menu premium diatas 50000 (q22)
    ("q22", 4, 3),   # Bebek (300000)
    ("q22", 26, 3),  # Capcay Ayam (350000)
    ("q22", 47, 3),  # Kepiting Saus Singapur (150000)
    ("q22", 96, 3),  # Gurame Semur (67000)
    ("q22", 99, 3),  # Gurame Bakar Sambal Dewa (67000)
    ("q22", 6, 3),   # Smoked Brisket Pizza (67000)
    ("q22", 7, 3),   # Capricciosa Pizza (67000)
    
    # Makanan berkuah (q26)
    ("q26", 37, 3),  # Javanese Noodle Soup
    ("q26", 41, 3),  # Soup Kacang Merah
    ("q26", 46, 3),  # Sop Hisit Ayam
    ("q26", 54, 3),  # Michee Pot
    ("q26", 61, 3),  # Sayur Lodeh
    ("q26", 76, 2),  # Paklay Goreng/Kuah
    ("q26", 77, 2),  # Cap Cay Goreng/Kuah
    ("q26", 78, 2),  # Bakmi Goreng/Kuah
    ("q26", 79, 2),  # Bihun Goreng/Kuah
    ("q26", 85, 3),  # Soto Ayam
    
    # Masakan italia (q8)
    ("q8", 6, 3),    # Smoked Brisket Pizza
    ("q8", 7, 3),    # Capricciosa Pizza
    ("q8", 16, 3),   # Spaghetti Bolognese
    ("q8", 17, 3),   # Spaghetti Aglio E Olio
    ("q8", 18, 3),   # Fettucine Al Pesto
    
    # Menu sambal (q36)
    ("q36", 12, 3),  # Ikan Baracuda Sambel Ijo
    ("q36", 15, 3),  # Ayam Goreng Sambal Combrang
    ("q36", 99, 3),  # Gurame Bakar Sambal Dewa
    ("q36", 100, 3), # Gurame Lombok Ijo
    
    # Masakan asam manis (q37)
    ("q37", 48, 3),  # Udang Asam Manis
    
    # And many more query-document pairs...
    # The full implementation would include relevance scores for all meaningful combinations
]