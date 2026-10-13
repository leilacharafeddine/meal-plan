"""Builds the 4-week month plan (W43–W46) as site-ready JSON + a readable markdown.

Run:  python3 plan/build_month.py   (from the repo root)
Ingredient tuple: (name, amount, unit, cat)
cat: F fruta y verdura · C carne y pescado · L huevos/lácteos/refrigerados · D despensa
     Z congelados · P pantry (check) · X Lebanese shop
"""
import json, re, datetime as dt
from collections import OrderedDict

# ---------------------------------------------------------------- helpers
def I(name, amt="", unit="", cat="F"):
    return (name, amt, unit, cat)

def S(at, text):
    return {"at": at, "text": text}

def dish(dish, minutes_note, equipment, ingredients, steps, note="", swaps=None, light=False, servings=1, ref=None):
    return dict(dish=dish, note=note or minutes_note, equipment=equipment, ingredients=ingredients,
                steps=steps, swaps=swaps or [], light=light, servings=servings, recipeRef=ref)

FR = {0.25: "¼", 0.5: "½", 0.75: "¾", 1.5: "1½", 2.5: "2½"}
def fmt(a):
    if a == "" or a is None: return ""
    if isinstance(a, (int, float)):
        if a in FR: return FR[a]
        return str(int(a)) if float(a).is_integer() else str(a)
    return str(a)

def qty(a, u):
    return (fmt(a) + (" " + u if u else "")).strip()

PANTRY = "Aceite de oliva virgen extra, sal, pimienta, orégano, pimentón dulce, ajo en polvo, canela, cacao puro, miel, salsa de soja, maicena, vinagre de manzana, mostaza, pan rallado, sésamo, caldo de verduras/pollo (brick o pastilla), mantequilla"

# ================================================================ BREAKFASTS
B = {}
B["yog_kiwi"] = dish("Greek yoghurt, kiwi, berries, oats & almonds", "No cooking.", ["Bowl"],
    [I("Yogur griego natural", 200, "g", "L"), I("Kiwi", 1), I("Frutos rojos", 60, "g", "Z"), I("Copos de avena", 20, "g", "D"), I("Almendras naturales", 15, "g", "D")],
    [S("0–5 min", "Yoghurt in a bowl. Top with sliced kiwi, berries, oats, chopped almonds.")])
B["mush_eggs"] = dish("Mushroom & spinach scrambled eggs on rye", "Ten minutes.", ["Air fryer (toast)", "Frying pan"],
    [I("Huevos", 2, "", "L"), I("Champiñón laminado", 60, "g"), I("Espinacas baby", 1, "handful"), I("Pan de centeno", 1, "slice", "D"), I("Mantequilla", 5, "g", "P")],
    [S("0–3 min", "Air fryer, 200°C, 3 min for the bread."), S("0–4 min", "Butter in pan, medium-high. Fry mushrooms 3 min until golden."),
     S("4–5 min", "Add spinach. Wilt 1 min."), S("5–9 min", "Lower heat. Add beaten eggs. Stir slowly until just set. Season. Serve on the toast.")])
B["cocoa_oats"] = dish("Cocoa overnight oats with kefir, banana & almonds", "Make the night before.", ["Jar (fridge overnight)"],
    [I("Copos de avena", 45, "g", "D"), I("Kéfir", 150, "ml", "L"), I("Yogur griego natural", 30, "g", "L"), I("Cacao puro", 1, "tsp", "P"), I("Plátano", 0.5), I("Almendras naturales", 15, "g", "D")],
    [S("Night before", "Mix oats, kefir, yoghurt, cocoa in a jar. Fridge."), S("0–3 min", "Top with sliced banana and chopped almonds.")])
B["cottage_avo"] = dish("Cottage cheese & avocado rye toast, pumpkin seeds", "Five minutes.", ["Air fryer (toast)"],
    [I("Pan de centeno", 2, "slices", "D"), I("Queso cottage", 100, "g", "L"), I("Aguacate", 0.5), I("Pipas de calabaza", 10, "g", "D"), I("Limón", 0.25)],
    [S("0–3 min", "Air fryer, 200°C, 3 min for the bread."), S("3–5 min", "Mash avocado with lemon and salt. Spread. Top with cottage cheese and pumpkin seeds.")])
B["berry_smoothie"] = dish("Berry, spinach & kefir smoothie + almonds", "Five minutes.", ["Hand blender + tall jug"],
    [I("Kéfir", 250, "ml", "L"), I("Frutos rojos", 80, "g", "Z"), I("Espinacas baby", 1, "handful"), I("Plátano", 0.5), I("Copos de avena", 20, "g", "D"), I("Almendras naturales", 15, "g", "D")],
    [S("0–5 min", "Everything except almonds in a tall jug. Blitz with the hand blender. Almonds on the side.")])
B["eggs_avo"] = dish("Two eggs, avocado & rye toast, small side salad", "Ten minutes.", ["Small pot", "Air fryer (toast)"],
    [I("Huevos", 2, "", "L"), I("Aguacate", 0.5), I("Pan de centeno", 1, "slice", "D"), I("Ensalada mezclum", 1, "handful")],
    [S("0–7 min", "Boil eggs 7 min (jammy)."), S("0–3 min", "Air fryer, 200°C, 3 min for the bread."), S("3–7 min", "Slice avocado. Dress salad with oil and lemon."), S("7–9 min", "Cool and peel eggs. Plate everything.")])
B["pancakes"] = dish("Banana-oat pancakes, Greek yoghurt & kiwi", "After your run.", ["Hand blender + tall jug", "Non-stick frying pan"],
    [I("Plátano", 1), I("Huevos", 2, "", "L"), I("Copos de avena", 40, "g", "D"), I("Yogur griego natural", 60, "g", "L"), I("Kiwi", 1), I("Miel", "", "drizzle", "P")],
    [S("0–3 min", "Banana, eggs, oats, pinch of salt in a tall jug. Blitz with the hand blender."), S("3–15 min", "Non-stick pan, medium, a little butter. Small pancakes, 2 min per side, in batches."), S("15–17 min", "Top with yoghurt, sliced kiwi, honey.")])
B["apple_oats"] = dish("Apple-cinnamon overnight oats with almonds", "Make the night before.", ["Jar (fridge overnight)", "Grater"],
    [I("Copos de avena", 45, "g", "D"), I("Kéfir", 150, "ml", "L"), I("Yogur griego natural", 30, "g", "L"), I("Manzana", 0.5), I("Canela", 0.5, "tsp", "P"), I("Almendras naturales", 15, "g", "D")],
    [S("Night before", "Grate the apple into a jar. Add oats, kefir, yoghurt, cinnamon. Mix. Fridge."), S("0–2 min", "Top with chopped almonds.")])
B["yog_pear"] = dish("Greek yoghurt, pear, granola & almonds", "No cooking.", ["Bowl"],
    [I("Yogur griego natural", 200, "g", "L"), I("Pera", 1), I("Granola sin azúcar añadido", 30, "g", "D"), I("Almendras naturales", 10, "g", "D")],
    [S("0–5 min", "Yoghurt in a bowl. Top with sliced pear, granola, almonds.")])
B["salmon_eggs"] = dish("Smoked salmon & scrambled eggs on rye", "Ten minutes.", ["Air fryer (toast)", "Frying pan"],
    [I("Huevos", 2, "", "L"), I("Salmón ahumado", 50, "g", "C"), I("Pan de centeno", 1, "slice", "D"), I("Mantequilla", 5, "g", "P"), I("Kiwi", 1)],
    [S("0–3 min", "Air fryer, 200°C, 3 min for the bread."), S("0–5 min", "Butter in pan, low. Add beaten eggs. Stir slowly until just set."), S("5–7 min", "Eggs on toast. Lay salmon on top. Black pepper. Kiwi on the side.")])
B["cocoa_smoothie"] = dish("Cocoa-banana kefir smoothie + almonds", "Five minutes.", ["Hand blender + tall jug"],
    [I("Kéfir", 250, "ml", "L"), I("Plátano", 1), I("Cacao puro", 1, "tsp", "P"), I("Copos de avena", 20, "g", "D"), I("Almendras naturales", 15, "g", "D")],
    [S("0–5 min", "Everything except almonds in a tall jug. Blitz with the hand blender. Almonds on the side.")])
B["avo_egg_toast"] = dish("Avocado & fried egg on rye", "Ten minutes.", ["Air fryer (toast)", "Frying pan"],
    [I("Huevos", 2, "", "L"), I("Aguacate", 0.5), I("Pan de centeno", 1, "slice", "D"), I("Limón", 0.25)],
    [S("0–3 min", "Air fryer, 200°C, 3 min for the bread."), S("0–5 min", "Fry eggs in a little oil, 3–4 min."), S("5–7 min", "Mash avocado with lemon and salt on the toast. Top with eggs.")])
B["cocoa_porridge"] = dish("Cocoa porridge with banana & almonds", "Eat by ~10:30, before V-Power.", ["Microwave"],
    [I("Copos de avena", 50, "g", "D"), I("Leche", 250, "ml", "L"), I("Cacao puro", 1, "tsp", "P"), I("Plátano", 1), I("Almendras naturales", 15, "g", "D")],
    [S("0–4 min", "Oats, milk, cocoa in a big bowl. Microwave 3 min, stir halfway."), S("4–6 min", "Top with sliced banana and chopped almonds.")])
B["mush_feta_eggs"] = dish("Mushroom & feta baked eggs, rye toast", "After your run.", ["Air fryer", "Small ovenproof dish"],
    [I("Huevos", 2, "", "L"), I("Champiñón laminado", 80, "g"), I("Espinacas baby", 1, "handful"), I("Queso feta", 30, "g", "L"), I("Pan de centeno", 1, "slice", "D")],
    [S("0–6 min", "Mushrooms + a drizzle of oil in the small dish. Air fryer, 190°C, 6 min."), S("6–8 min", "Stir in spinach. Make 2 wells. Crack in the eggs. Crumble feta on top."),
     S("8–16 min", "Air fryer, 170°C, 7–8 min until whites set."), S("16–19 min", "Toast bread in the air fryer, 200°C, 3 min. Serve.")])
B["apple_porridge"] = dish("Apple & almond porridge", "Warm start to the bleed week.", ["Microwave", "Grater"],
    [I("Copos de avena", 50, "g", "D"), I("Leche", 250, "ml", "L"), I("Manzana", 0.5), I("Canela", 0.5, "tsp", "P"), I("Almendras naturales", 15, "g", "D"), I("Yogur griego natural", 50, "g", "L")],
    [S("0–4 min", "Oats, milk, grated apple, cinnamon in a big bowl. Microwave 3 min, stir halfway."), S("4–6 min", "Top with yoghurt and chopped almonds.")])
B["yog_granola"] = dish("Greek yoghurt, berries & granola", "No cooking.", ["Bowl"],
    [I("Yogur griego natural", 200, "g", "L"), I("Frutos rojos", 60, "g", "Z"), I("Granola sin azúcar añadido", 30, "g", "D"), I("Almendras naturales", 10, "g", "D")],
    [S("0–5 min", "Yoghurt in a bowl. Top with berries, granola, almonds.")])
B["mush_omelette"] = dish("Mushroom & cheese omelette, rye toast", "Ten minutes.", ["Frying pan", "Air fryer (toast)"],
    [I("Huevos", 2, "", "L"), I("Champiñón laminado", 60, "g"), I("Queso rallado mozzarella", 20, "g", "L"), I("Pan de centeno", 1, "slice", "D")],
    [S("0–3 min", "Air fryer, 200°C, 3 min for the bread."), S("0–4 min", "Fry mushrooms in a little oil, 3 min."), S("4–9 min", "Pour in beaten eggs. Cook 3–4 min on medium. Cheese on one half. Fold.")])
B["berry_oats"] = dish("Berry overnight oats with almonds", "Make the night before.", ["Jar (fridge overnight)"],
    [I("Copos de avena", 45, "g", "D"), I("Kéfir", 150, "ml", "L"), I("Yogur griego natural", 30, "g", "L"), I("Frutos rojos", 60, "g", "Z"), I("Almendras naturales", 15, "g", "D")],
    [S("Night before", "Mix oats, kefir, yoghurt, frozen berries in a jar. Fridge."), S("0–2 min", "Top with chopped almonds.")])
B["kiwi_smoothie"] = dish("Kiwi, spinach & kefir smoothie + almonds", "Five minutes.", ["Hand blender + tall jug"],
    [I("Kéfir", 250, "ml", "L"), I("Kiwi", 2), I("Espinacas baby", 1, "handful"), I("Plátano", 0.5), I("Copos de avena", 20, "g", "D"), I("Almendras naturales", 15, "g", "D")],
    [S("0–5 min", "Peel kiwis. Everything except almonds in a tall jug. Blitz with the hand blender. Almonds on the side.")])
B["mush_toastie"] = dish("Mushroom & cheese toastie (air fryer)", "Eat by ~10:30, before V-Power.", ["Frying pan", "Air fryer"],
    [I("Pan de centeno", 2, "slices", "D"), I("Champiñón laminado", 60, "g"), I("Queso en lonchas (havarti o similar)", 2, "slices", "L"), I("Jamón cocido", 2, "slices", "C"), I("Kiwi", 1)],
    [S("0–4 min", "Fry mushrooms in a little oil, 3 min."), S("4–5 min", "Fill bread: cheese, ham, mushrooms. Close."), S("5–11 min", "Air fryer, 190°C, 6 min, flip halfway. Kiwi on the side.")])

# ================================================================ LUNCHES (cook ×2 unless single)
L = {}
L["chicken_souvlaki"] = dish("Chicken souvlaki rice, peppers, cucumber & tzatziki", "Cook ×2 — tomorrow's lunch is the second portion.", ["Rice cooker", "Air fryer"],
    [I("Pechuga de pollo en filetes", 360, "g", "C"), I("Arroz basmati", 150, "g", "D"), I("Limón", 1), I("Orégano", 1, "tsp", "P"), I("Ajo", 2, "cloves"), I("Pimiento rojo", 1), I("Pepino", 0.5), I("Salsa tzatziki", 6, "tbsp", "L"), I("Ensalada mezclum", 2, "handfuls")],
    [S("0–2 min", "Rinse 150 g rice. Rice cooker, 300 ml water, pinch of salt. Start."), S("2–5 min", "Cube chicken. Mix with 1 tbsp oil, lemon juice, oregano, grated garlic, salt."),
     S("5–17 min", "Air fryer, 200°C, 12 min. Shake halfway."), S("11–17 min", "Pepper strips into the drawer for the last 6 min. Dice cucumber."),
     S("17–20 min", "Plate half: rice, chicken, pepper, cucumber, tzatziki, salad. Box the other half for tomorrow.")],
    swaps=["No raw tomato — cucumber and roasted pepper instead."], servings=2, ref="chicken-souvlaki-rice")
L["turkey_souvlaki"] = dict(L["chicken_souvlaki"], dish="Turkey souvlaki rice, peppers, cucumber & tzatziki",
    ingredients=[I("Pechuga de pavo en filetes", 360, "g", "C")] + L["chicken_souvlaki"]["ingredients"][1:],
    steps=[dict(s, text=s["text"].replace("chicken", "turkey")) for s in L["chicken_souvlaki"]["steps"]])
L["meatballs_mush"] = dish("Beef meatballs in tomato-mushroom sauce, spaghetti", "Cook ×2 — tomorrow's lunch is the second portion.", ["Frying pan with lid", "Large pot"],
    [I("Carne picada de ternera", 250, "g", "C"), I("Champiñón laminado", 200, "g"), I("Ajo", 2, "cloves"), I("Pan rallado", 2, "tbsp", "P"), I("Huevos", 1, "", "L"), I("Perejil fresco", 1, "handful"), I("Tomate triturado", 400, "g", "D"), I("Espaguetis", 180, "g", "D"), I("Parmesano rallado", 30, "g", "L"), I("Ensalada mezclum", 2, "handfuls")],
    [S("0–4 min", "Mix mince, 1 grated garlic clove, breadcrumbs, egg, parsley, salt. Roll 16 small balls. Put pasta water on."),
     S("4–9 min", "1 tbsp oil, medium-high. Brown meatballs all over, 5 min."), S("9–12 min", "Add mushrooms and the other garlic clove. Cook 3 min."),
     S("12–22 min", "Add tomato. Lid on. Simmer 10 min. Cook spaghetti meanwhile."), S("22–24 min", "Plate half with parmesan and salad. Box the other half.")],
    servings=2, ref="spaghetti-meatballs")
L["chicken_pasta_mush"] = dish("Creamy chicken, mushroom & spinach pasta", "Cook ×2 — Saturday's post-V-Power lunch is the second portion.", ["Large pot", "Large frying pan"],
    [I("Pechuga de pollo en filetes", 300, "g", "C"), I("Champiñón laminado", 200, "g"), I("Espinacas baby", 80, "g"), I("Ajo", 2, "cloves"), I("Nata para cocinar ligera", 200, "ml", "L"), I("Parmesano rallado", 30, "g", "L"), I("Macarrones / pasta corta", 160, "g", "D")],
    [S("0–2 min", "Boil salted water. Cut chicken into bite-size pieces. Season."), S("2–13 min", "Cook pasta per packet (~11 min). Keep a mug of pasta water."),
     S("2–8 min", "1 tbsp oil, high. Fry chicken 6 min until golden and cooked."), S("8–12 min", "Add mushrooms 4 min. Add grated garlic 30 s."),
     S("12–16 min", "Pour in cream. Simmer 2 min. Stir in spinach until wilted. Add parmesan."), S("16–18 min", "Add pasta + a splash of pasta water. Plate half. Box the other half.")],
    servings=2)
L["salmon_alioli"] = dish("Salmon with alioli, baby potatoes & green beans", "Your favourite. One drawer, all together.", ["Air fryer"],
    [I("Lomos de salmón", 1, "fillet (~130 g)", "C"), I("Patata baby", 250, "g"), I("Judías verdes", 100, "g"), I("Alioli", 1, "tbsp", "D"), I("Limón", 0.5), I("Perejil fresco", 1, "pinch")],
    [S("0–3 min", "Halve potatoes. Toss with 1 tbsp oil and salt."), S("3–21 min", "Air fryer, 200°C, 18 min. Shake at 9 min."),
     S("11–21 min", "At 11 min: add salmon (skin down, salted) and green beans. Cook the last 10 min together."), S("21–23 min", "Plate. Big spoon of alioli, lemon, parsley.")])
L["salmon_alioli_broc"] = dict(L["salmon_alioli"], dish="Salmon with alioli, baby potatoes & broccoli",
    ingredients=[I("Brócoli (floretes)", 120, "g") if x[0] == "Judías verdes" else x for x in L["salmon_alioli"]["ingredients"]],
    steps=[dict(s, text=s["text"].replace("green beans", "broccoli florets")) for s in L["salmon_alioli"]["steps"]])
L["turkey_stroganoff"] = dish("Turkey & mushroom stroganoff with rice", "Cook ×2 — tomorrow's lunch is the second portion.", ["Rice cooker", "Large frying pan"],
    [I("Pechuga de pavo en filetes", 300, "g", "C"), I("Champiñón laminado", 250, "g"), I("Cebolla", 1), I("Ajo", 1, "clove"), I("Pimentón dulce", 1, "tsp", "P"), I("Nata para cocinar ligera", 200, "ml", "L"), I("Mostaza", 1, "tsp", "P"), I("Arroz basmati", 150, "g", "D"), I("Perejil fresco", 1, "handful"), I("Ensalada mezclum", 2, "handfuls")],
    [S("0–2 min", "Rinse 150 g rice. Rice cooker, 300 ml water, pinch of salt. Start."), S("2–6 min", "Slice onion. 1 tbsp oil, medium. Soften onion 4 min."),
     S("6–11 min", "Turn heat up. Add turkey strips. Cook 5 min until golden."), S("11–16 min", "Add mushrooms and garlic. Cook 5 min."),
     S("16–20 min", "Stir in paprika, cream, mustard. Simmer 3 min. Season."), S("20–22 min", "Plate half with rice, parsley, salad. Box the other half.")],
    servings=2)
L["honeysoy_pork"] = dish("Honey-soy pork, rice & green beans", "Cook ×2 — tomorrow's lunch is the second portion.", ["Rice cooker", "Large frying pan"],
    [I("Filetes de lomo de cerdo", 300, "g", "C"), I("Arroz basmati", 150, "g", "D"), I("Judías verdes", 200, "g"), I("Ajo", 1, "clove"), I("Salsa de soja", 2, "tbsp", "P"), I("Miel", 2, "tbsp", "P"), I("Vinagre de manzana", 1, "tsp", "P"), I("Sésamo", 1, "tsp", "P"), I("Cebolleta", 1), I("Lima", 0.5)],
    [S("0–2 min", "Rinse 150 g rice. Rice cooker, 300 ml water, pinch of salt. Start."), S("2–4 min", "Mix soy, honey, vinegar, grated garlic. Trim beans."),
     S("4–10 min", "Oil, medium-high. Fry beans 3 min. Splash of water, lid, 3 min. Lime juice. Set aside."), S("10–18 min", "Same pan. Season pork. Fry 3 min per side, then 2 min more. No pink inside."),
     S("18–20 min", "Pour in sauce. Bubble 1–2 min until sticky."), S("20–22 min", "Slice. Plate half with rice, beans, sesame, spring onion. Box the other half.")],
    swaps=["No hoisin or sriracha — honey-soy glaze, no heat."], servings=2)
L["farfalle"] = dish("Farfalle with feta, broad beans & jamón", "Cook ×2 — great cold for Saturday after V-Power.", ["Large pot", "Frying pan"],
    [I("Farfalle", 180, "g", "D"), I("Habitas baby", 160, "g", "Z"), I("Chalota", 1), I("Limón", 1), I("Queso feta", 80, "g", "L"), I("Jamón serrano en lonchas", 60, "g", "C"), I("Menta o eneldo fresco", 1, "handful"), I("Ensalada mezclum", 2, "handfuls")],
    [S("0–3 min", "Boil salted water. Blanch broad beans 3 min. Lift out with a slotted spoon."), S("3–14 min", "Cook farfalle in the same water (~11 min). Keep a mug of pasta water."),
     S("4–9 min", "2 tbsp oil, medium. Soften sliced shallot 5 min."), S("14–17 min", "Add pasta, beans, lemon zest + juice, splash of pasta water, most of the feta and herbs. Stir until glossy."),
     S("17–19 min", "Plate half. Tear jamón on top, rest of feta, pepper. Box the other half (jamón separate).")],
    swaps=["Chilli flakes → black pepper and lemon zest.", "Prosciutto → jamón serrano (Mercadona)."], servings=2, ref="farfalle-feta-broad-beans")
L["paprika_salmon"] = dish("Paprika salmon, sweet potato fries & sprout slaw", "Weekend cook.", ["Air fryer", "Frying pan"],
    [I("Lomos de salmón", 1, "fillet (~130 g)", "C"), I("Boniato", 1), I("Pimentón dulce", 1, "tsp", "P"), I("Ajo", 1, "clove"), I("Coles de Bruselas", 75, "g"), I("Kale", 1, "handful"), I("Manzana", 0.5), I("Limón", 0.5), I("Yogur griego natural", 30, "g", "L"), I("Pipas de calabaza", 10, "g", "D")],
    [S("0–4 min", "Cut sweet potato into fries. Toss with oil, salt, ½ tsp paprika."), S("4–24 min", "Air fryer, 200°C, 20 min. Shake at 10 min."),
     S("6–12 min", "Thinly slice sprouts, shred kale, apple matchsticks. Toss with lemon, yoghurt, half the grated garlic, salt. Massage 1 min."),
     S("12–14 min", "Season salmon with rest of paprika + garlic, salt."), S("14–24 min", "At 14 min: salmon into the drawer, skin down, for the last 10 min."),
     S("14–16 min", "Toast pumpkin seeds in a dry pan, 2 min."), S("24–26 min", "Plate fries, slaw, salmon. Seeds on top.")],
    swaps=["Smoked paprika is the sweet kind — no heat."], ref="paprika-salmon-slaw")
L["beef_ragu"] = dish("Beef & mushroom ragù rigatoni", "Cook ×2 — iron for the bleed week. Tomorrow's lunch is the second portion.", ["Large frying pan", "Large pot", "Grater"],
    [I("Carne picada de ternera", 300, "g", "C"), I("Champiñón laminado", 200, "g"), I("Cebolla", 0.5), I("Zanahoria", 1), I("Ajo", 2, "cloves"), I("Tomate triturado", 400, "g", "D"), I("Macarrones / rigatoni", 180, "g", "D"), I("Parmesano rallado", 30, "g", "L"), I("Orégano", 1, "tsp", "P"), I("Ensalada mezclum", 2, "handfuls")],
    [S("0–3 min", "Boil salted water. Finely chop onion. Grate carrot."), S("3–6 min", "1 tbsp oil, medium-high. Onion + carrot 3 min."),
     S("6–11 min", "Add mince. Break up. Brown 5 min."), S("11–14 min", "Add mushrooms + garlic. Cook 3 min."),
     S("14–24 min", "Add tomato + oregano. Simmer 10 min. Cook pasta meanwhile."), S("24–25 min", "Plate half with parmesan and salad. Box the other half.")],
    servings=2)
L["chicken_bean_bowl"] = dish("Mild chicken & red bean rice bowl", "Cook ×2 — iron (beans) + vitamin C (lime). Tomorrow's lunch is the second portion.", ["Rice cooker", "Frying pan"],
    [I("Pechuga de pollo en filetes", 360, "g", "C"), I("Arroz basmati", 150, "g", "D"), I("Alubias rojas cocidas", 1, "jar (400 g)", "D"), I("Tomate triturado", 100, "g", "D"), I("Pimentón dulce", 1, "tsp", "P"), I("Ajo en polvo", 1, "tsp", "P"), I("Orégano", 1, "tsp", "P"), I("Lima", 1), I("Perejil fresco", 1, "handful"), I("Lechuga (cogollos)", 2)],
    [S("0–2 min", "Rinse 150 g rice. Rice cooker, 300 ml water, pinch of salt. Start."), S("2–4 min", "Rub chicken with half the paprika, garlic powder, oregano, salt, oil."),
     S("4–16 min", "Hot pan. Chicken 5–6 min per side until cooked. Rest, slice."), S("16–20 min", "Same pan: tomato, rest of paprika, drained beans, juice of ½ lime. Heat 3 min."),
     S("20–22 min", "Plate half: rice, beans, chicken, parsley, lettuce, lime wedge. Box the other half.")],
    swaps=["No chilli or cumin — sweet paprika rub.", "Parsley instead of coriander.", "Warm tomato sauce instead of raw salsa."], servings=2, ref="chicken-bean-rice-bowl")
L["steak_fajita"] = dish("Steak fajita rice with peppers & onion", "Cook ×2 — steak + peppers = iron + vitamin C. Saturday's lunch is the second portion.", ["Rice cooker", "Large frying pan"],
    [I("Filete de añojo (ternera)", 300, "g", "C"), I("Pimientos tricolor", 2), I("Cebolla roja", 1), I("Lima", 1), I("Pimentón dulce", 2, "tsp", "P"), I("Ajo en polvo", 1, "tsp", "P"), I("Orégano", 1, "tsp", "P"), I("Arroz basmati", 150, "g", "D"), I("Perejil fresco", 1, "handful")],
    [S("0–2 min", "Rinse 150 g rice. Rice cooker, 300 ml water, pinch of salt. Start."), S("2–5 min", "Mix paprika, garlic powder, oregano, salt, juice of ½ lime, 1 tbsp oil. Coat steak. Slice peppers + onion."),
     S("5–12 min", "Hot pan. Peppers + onion 7 min until charred. Set aside."), S("12–18 min", "High heat. Steak 2–3 min per side. Rest 3 min. Slice thin."),
     S("18–20 min", "Plate half: rice, veg, steak, lime, parsley. Box the other half (slightly undercook — it finishes when reheated).")],
    swaps=["Mild seasoning: sweet paprika, garlic, oregano. No chilli, no cumin.", "Parsley instead of coriander."], servings=2, ref="steak-fajita-rice")
L["steak_mush_stirfry"] = dish("Honey-soy steak & mushroom stir-fry with rice", "Cook ×2 — tomorrow's lunch is the second portion.", ["Rice cooker", "Large frying pan"],
    [I("Filete de añojo (ternera)", 300, "g", "C"), I("Champiñón laminado", 250, "g"), I("Pimiento rojo", 1), I("Cebolleta", 2), I("Ajo", 2, "cloves"), I("Salsa de soja", 3, "tbsp", "P"), I("Miel", 1, "tbsp", "P"), I("Maicena", 1, "tsp", "P"), I("Arroz basmati", 150, "g", "D"), I("Sésamo", 1, "tsp", "P")],
    [S("0–2 min", "Rinse 150 g rice. Rice cooker, 300 ml water, pinch of salt. Start."), S("2–5 min", "Slice steak thin. Toss with 1 tbsp soy + cornflour. Mix rest of soy with honey + 2 tbsp water."),
     S("5–9 min", "Very hot pan, 1 tbsp oil. Sear steak 2 min. Take out."), S("9–15 min", "Mushrooms + pepper strips 5 min. Garlic + spring onion 1 min."),
     S("15–17 min", "Steak back in. Pour sauce. Bubble 1–2 min."), S("17–19 min", "Plate half with rice and sesame. Box the other half.")],
    swaps=["No chilli."], servings=2)
L["pork_couscous"] = dish("Pork tenderloin, roasted veg & couscous", "Cook ×2 — Saturday's post-V-Power lunch is the second portion.", ["Air fryer", "Kettle / microwave"],
    [I("Solomillo de cerdo", 1, "(~400 g)", "C"), I("Calabacín", 1), I("Pimiento rojo", 1), I("Cebolla roja", 0.5), I("Cuscús", 140, "g", "D"), I("Limón", 1), I("Orégano", 1, "tsp", "P"), I("Pimentón dulce", 1, "tsp", "P"), I("Yogur griego natural", 60, "g", "L"), I("Perejil fresco", 1, "handful")],
    [S("0–4 min", "Chop courgette, pepper, onion. Toss with oil, salt, oregano. Rub pork with oil, paprika, salt."),
     S("4–22 min", "Air fryer, 200°C. Pork + veg together, 18 min. Turn pork at 9 min. Inside must be no longer pink."),
     S("10–15 min", "Couscous in a bowl. 140 ml boiling salted water + lemon juice. Cover 5 min. Fluff with a fork and parsley."),
     S("22–25 min", "Rest pork 3 min. Slice. Plate half with veg, couscous, spoon of yoghurt. Box the other half.")],
    servings=2)
L["mush_risotto"] = dish("Mushroom & pea risotto with a fried egg", "Weekend cook. Warm and grounding.", ["Wide pan", "Small pot (hot stock)", "Frying pan"],
    [I("Arroz redondo", 75, "g", "D"), I("Champiñón laminado", 150, "g"), I("Guisantes", 80, "g", "Z"), I("Cebolla", 0.5), I("Ajo", 1, "clove"), I("Caldo de verduras", 350, "ml", "P"), I("Mantequilla", 10, "g", "P"), I("Parmesano rallado", 15, "g", "L"), I("Huevos", 1, "", "L"), I("Ensalada mezclum", 1, "handful")],
    [S("0–5 min", "Heat stock in the small pot. Butter in wide pan: onion + garlic 2 min, mushrooms 3 min."), S("5–7 min", "Add rice. Toast 1–2 min."),
     S("7–25 min", "Add hot stock a ladle at a time. Stir often. ~18 min. Peas in for the last 4 min."), S("23–26 min", "Fry the egg."),
     S("25–27 min", "Off heat: stir in parmesan. Top with the egg. Salad on the side.")], ref="mushroom-pea-risotto")

def leftover(key):
    d = L[key]
    nm = d["dish"]
    return dict(dish=nm + " (leftover)", note="Second portion of yesterday's lunch.", equipment=["Microwave"], ingredients=[],
                steps=[S("0–3 min", "Microwave 2½–3 min, covered, stir halfway (pasta: add a splash of water)." if "farfalle" not in key else "Eat cold or warm 1½ min. Add the jamón."),
                       S("3–5 min", "Plate with a handful of salad leaves.")],
                swaps=[], light=False, servings=1, recipeRef=d.get("recipeRef"), leftoverOf=nm)

# ================================================================ DINNERS (light little plates)
D = {}
RYE = I("Crispbread de centeno (your usual)", 3, "pieces", "D")
D["hummus_crackers"] = dish("Hummus, rye crispbread, cucumber & carrot sticks, olives", "Light plate. No cooking.", ["Plate"],
    [I("Hummus", 4, "tbsp", "L"), RYE, I("Pepino", 0.25), I("Zanahoria", 1), I("Aceitunas verdes", 8, "", "D")],
    [S("0–5 min", "Cut cucumber and carrot into sticks. Plate with hummus, crispbread, olives.")], light=True)
D["labneh_pitta"] = dish("Labneh with za'atar & olive oil, cucumber, olives, pitta", "Light plate. No cooking.", ["Plate", "Frying pan (warm pitta)"],
    [I("Labneh", 4, "tbsp", "X"), I("Za'atar", 1, "tsp", "X"), I("Pepino", 0.25), I("Aceitunas verdes", 8, "", "D"), I("Pan de pita", 1, "", "D")],
    [S("0–2 min", "Warm pitta in a dry pan, 30 s per side. Cut into triangles."), S("2–5 min", "Labneh on a plate. Olive oil + za'atar on top. Add cucumber and olives.")], light=True)
D["falafel_plate"] = dish("Falafel, hummus & salad leaves", "Light plate.", ["Air fryer"],
    [I("Falafel", 4, "", "L"), I("Hummus", 3, "tbsp", "L"), I("Ensalada mezclum", 1, "handful"), I("Limón", 0.25)],
    [S("0–8 min", "Air fryer, 190°C, 8 min for the falafel."), S("0–3 min", "Dress leaves with lemon and oil."), S("8–9 min", "Plate falafel, hummus, salad.")], light=True)
D["postgap_labneh_eggs"] = dish("After GAP: labneh, 2 boiled eggs, cucumber, rye crispbread", "Light but protein-forward after the evening class.", ["Small pot"],
    [I("Huevos", 2, "", "L"), I("Labneh", 4, "tbsp", "X"), I("Za'atar", 1, "tsp", "X"), I("Pepino", 0.25), RYE],
    [S("0–8 min", "Boil eggs 8 min. Cool in cold water. (Or boil them before class.)"), S("8–10 min", "Labneh + olive oil + za'atar. Plate with halved eggs, cucumber, crispbread.")], light=True)
D["smoked_salmon_crackers"] = dish("Smoked salmon & cream cheese on rye crispbread, cucumber", "Light plate. No cooking.", ["Plate"],
    [I("Salmón ahumado", 60, "g", "C"), I("Queso crema", 2, "tbsp", "L"), RYE, I("Pepino", 0.25), I("Limón", 0.25)],
    [S("0–5 min", "Spread cream cheese on crispbread. Top with salmon, cucumber slices, lemon, black pepper.")], light=True)
D["greek_plate"] = dish("Feta, olives, roasted pepper & rye crispbread", "Light plate. No cooking.", ["Plate"],
    [I("Queso feta", 50, "g", "L"), I("Aceitunas negras / kalamata", 8, "", "D"), I("Pimiento asado (bote)", 0.5, "", "D"), I("Pepino", 0.25), RYE, I("Orégano", 1, "pinch", "P")],
    [S("0–5 min", "Plate feta (olive oil + oregano on top), olives, pepper strips, cucumber, crispbread.")], light=True)
D["ajillo_hummus"] = dish("Champiñones al ajillo, hummus & bread", "Light plate.", ["Frying pan"],
    [I("Champiñón laminado", 150, "g"), I("Ajo", 2, "cloves"), I("Perejil fresco", 1, "pinch"), I("Hummus", 3, "tbsp", "L"), I("Pan de pita", 1, "", "D")],
    [S("0–2 min", "Slice garlic. 1 tbsp oil, medium-high."), S("2–8 min", "Mushrooms 5 min until golden. Garlic in for the last minute. Salt, parsley."), S("8–10 min", "Warm pitta in the same pan. Plate with hummus.")], light=True)
D["hummus_veg_egg"] = dish("Hummus, veg sticks & a boiled egg", "Light plate.", ["Small pot"],
    [I("Huevos", 1, "", "L"), I("Hummus", 4, "tbsp", "L"), I("Zanahoria", 1), I("Pepino", 0.25), I("Pimiento rojo", 0.5), RYE],
    [S("0–8 min", "Boil egg 8 min. Cut veg into sticks meanwhile."), S("8–10 min", "Cool and halve egg. Plate everything.")], light=True)
D["whitebean_mash"] = dish("White bean & feta mash on rye crispbread", "Light plate.", ["Bowl", "Fork"],
    [I("Alubias blancas cocidas", 120, "g", "D"), I("Queso feta", 30, "g", "L"), I("Limón", 0.5), I("Ajo", 0.5, "clove"), RYE, I("Pepino", 0.25)],
    [S("0–5 min", "Rinse beans. Mash with fork, olive oil, lemon, grated garlic, salt. Crumble feta in."), S("5–7 min", "Spread on crispbread. Cucumber on the side.")], light=True)
D["postgap_turkey"] = dish("After GAP: turkey slices, labneh, boiled egg, rye crispbread", "Light but protein-forward after the evening class.", ["Small pot"],
    [I("Pechuga de pavo en lonchas", 60, "g", "C"), I("Huevos", 1, "", "L"), I("Labneh", 3, "tbsp", "X"), I("Za'atar", 1, "tsp", "X"), I("Pepino", 0.25), RYE],
    [S("0–8 min", "Boil egg 8 min. Cool. (Or boil it before class.)"), S("8–10 min", "Plate turkey, labneh with oil + za'atar, egg, cucumber, crispbread.")], light=True)
D["yog_cucumber_pitta"] = dish("Yoghurt-cucumber-mint dip with pitta & olives", "Light plate (khiyar bi laban style).", ["Bowl", "Grater", "Frying pan (warm pitta)"],
    [I("Yogur griego natural", 150, "g", "L"), I("Pepino", 0.5), I("Menta o eneldo fresco", 1, "pinch"), I("Ajo", 0.5, "clove"), I("Pan de pita", 1, "", "D"), I("Aceitunas verdes", 8, "", "D")],
    [S("0–4 min", "Grate cucumber, squeeze out water. Mix with yoghurt, mint, grated garlic, salt, olive oil."), S("4–6 min", "Warm pitta in a dry pan. Plate with the dip and olives.")], light=True)
D["ajillo_manchego"] = dish("Champiñones al ajillo, manchego & bread", "Light plate.", ["Frying pan"],
    [I("Champiñón laminado", 150, "g"), I("Ajo", 2, "cloves"), I("Perejil fresco", 1, "pinch"), I("Queso manchego", 40, "g", "L"), I("Pan de centeno", 1, "slice", "D")],
    [S("0–2 min", "Slice garlic. 1 tbsp oil, medium-high."), S("2–8 min", "Mushrooms 5 min until golden. Garlic in for the last minute. Salt, parsley."), S("8–10 min", "Plate with manchego slices and bread.")], light=True)
D["hummus_olives_feta"] = dish("Hummus, olives, feta & cucumber", "Light plate. No cooking.", ["Plate"],
    [I("Hummus", 3, "tbsp", "L"), I("Aceitunas verdes", 8, "", "D"), I("Queso feta", 30, "g", "L"), I("Pepino", 0.25), RYE],
    [S("0–5 min", "Plate everything. Olive oil over the hummus.")], light=True)
D["crema_calabaza"] = dish("Smooth pumpkin soup (crema de calabaza), yoghurt & pumpkin seeds", "Bleed-week soup. Make ×2 — tomorrow's dinner is the second bowl.", ["Pot with lid", "Hand blender"],
    [I("Calabaza troceada", 500, "g"), I("Zanahoria", 1), I("Cebolla", 0.5), I("Caldo de verduras", 500, "ml", "P"), I("Yogur griego natural", 60, "g", "L"), I("Pipas de calabaza", 15, "g", "D"), RYE],
    [S("0–3 min", "Chop onion + carrot. 1 tbsp oil, medium. Soften 3 min."), S("3–18 min", "Add pumpkin + stock. Lid on. Simmer 15 min until soft."),
     S("18–21 min", "Blitz with the hand blender until completely smooth. Season."), S("21–23 min", "Bowl with a swirl of yoghurt + seeds. Crispbread on the side. Fridge the other half.")],
    swaps=["Fully blended — no pieces."], light=True, servings=2)
D["crema_champi"] = dish("Smooth mushroom soup (crema de champiñones)", "Bleed-week soup. Make ×2 — Friday's dinner is the second bowl.", ["Pot with lid", "Hand blender"],
    [I("Champiñón laminado", 300, "g"), I("Cebolla", 0.5), I("Ajo", 1, "clove"), I("Patata", 1, "small"), I("Caldo de verduras", 500, "ml", "P"), I("Nata para cocinar ligera", 50, "ml", "L"), RYE],
    [S("0–3 min", "Chop onion, dice potato. 1 tbsp oil, medium. Onion + garlic 2 min."), S("3–7 min", "Add mushrooms. Cook 4 min."), S("7–19 min", "Add potato + stock. Lid on. Simmer 12 min."),
     S("19–22 min", "Add cream. Blitz with the hand blender until completely smooth. Season."), S("22–23 min", "Serve one bowl with crispbread. Fridge the other.")],
    swaps=["Fully blended — no pieces."], light=True, servings=2)
D["leftover_calabaza_egg"] = dish("Pumpkin soup (leftover) + boiled egg", "Second bowl from yesterday.", ["Microwave", "Small pot"],
    [I("Huevos", 1, "", "L"), RYE],
    [S("0–8 min", "Boil egg 8 min."), S("5–8 min", "Microwave soup 2½ min, stir halfway."), S("8–9 min", "Serve with the halved egg and crispbread.")], light=True)
D["leftover_champi_cheese"] = dish("Mushroom soup (leftover) + cheese on rye", "Second bowl from Wednesday.", ["Microwave", "Air fryer"],
    [I("Pan de centeno", 1, "slice", "D"), I("Queso en lonchas (havarti o similar)", 1, "slice", "L")],
    [S("0–4 min", "Cheese on bread. Air fryer, 190°C, 4 min."), S("0–3 min", "Microwave soup 2½ min, stir halfway."), S("4–5 min", "Serve together.")], light=True)
D["salmon_avo_crackers"] = dish("Smoked salmon & avocado on rye crispbread", "Light plate. No cooking.", ["Plate"],
    [I("Salmón ahumado", 60, "g", "C"), I("Aguacate", 0.5), RYE, I("Limón", 0.25)],
    [S("0–5 min", "Mash avocado with lemon + salt on crispbread. Top with salmon, black pepper.")], light=True)
D["falafel_tzatziki"] = dish("Falafel & tzatziki, cucumber, leaves", "Light plate.", ["Air fryer"],
    [I("Falafel", 4, "", "L"), I("Salsa tzatziki", 3, "tbsp", "L"), I("Pepino", 0.25), I("Ensalada mezclum", 1, "handful")],
    [S("0–8 min", "Air fryer, 190°C, 8 min for the falafel."), S("8–10 min", "Plate with tzatziki, cucumber, leaves.")], light=True)
D["hummus_bread"] = dish("Hummus, olives, cucumber & bread", "Light plate. No cooking.", ["Plate"],
    [I("Hummus", 4, "tbsp", "L"), I("Aceitunas verdes", 8, "", "D"), I("Pepino", 0.25), I("Pan de pita", 1, "", "D")],
    [S("0–5 min", "Warm pitta in a dry pan if you like. Plate everything.")], light=True)


# ================================================================ WEEK STRUCTURE (approved 13 Oct)
LO = "LO:"
WEEKS = [
  ("2026-W43", "19 – 25 October 2026", "End of ovulation → early luteal. Chicken week. Colourful early, then grounding carbs + magnesium.", [
    ("yog_kiwi", "chicken_souvlaki", "hummus_crackers"),
    ("mush_eggs", LO+"chicken_souvlaki", "labneh_pitta"),
    ("cocoa_oats", "meatballs_mush", "falafel_plate"),
    ("cottage_avo", LO+"meatballs_mush", "postgap_labneh_eggs"),
    ("berry_smoothie", "chicken_pasta_mush", "smoked_salmon_crackers"),
    ("eggs_avo", LO+"chicken_pasta_mush", "greek_plate"),
    ("pancakes", "salmon_alioli", "ajillo_hummus")]),
  ("2026-W44", "26 October – 1 November 2026", "Late luteal. Turkey week. Comfort carbs, magnesium (oats, cocoa, almonds, beans), steady blood sugar.", [
    ("apple_oats", "turkey_stroganoff", "labneh_pitta"),
    ("yog_pear", LO+"turkey_stroganoff", "hummus_veg_egg"),
    ("salmon_eggs", "honeysoy_pork", "whitebean_mash"),
    ("cocoa_smoothie", LO+"honeysoy_pork", "postgap_turkey"),
    ("avo_egg_toast", "farfalle", "yog_cucumber_pitta"),
    ("cocoa_porridge", LO+"farfalle", "ajillo_manchego"),
    ("mush_feta_eggs", "paprika_salmon", "hummus_olives_feta")]),
  ("2026-W45", "2 – 8 November 2026", "Bleed Mon–Fri (cycle days 1–5) → follicular weekend. Chicken week. Iron + vitamin C; smooth soups as dinner.", [
    ("apple_porridge", "beef_ragu", "crema_calabaza"),
    ("mush_eggs", LO+"beef_ragu", "leftover_calabaza_egg"),
    ("yog_kiwi", "chicken_bean_bowl", "crema_champi"),
    ("cottage_avo", LO+"chicken_bean_bowl", "postgap_labneh_eggs"),
    ("berry_smoothie", "steak_fajita", "leftover_champi_cheese"),
    ("eggs_avo", LO+"steak_fajita", "falafel_plate"),
    ("pancakes", "salmon_alioli_broc", "labneh_pitta")]),
  ("2026-W46", "9 – 15 November 2026", "Follicular → ovulation (~Sun 15 Nov). Turkey week. Fresh, colourful, lean protein.", [
    ("yog_granola", "turkey_souvlaki", "salmon_avo_crackers"),
    ("mush_omelette", LO+"turkey_souvlaki", "hummus_veg_egg"),
    ("berry_oats", "steak_mush_stirfry", "labneh_pitta"),
    ("avo_egg_toast", LO+"steak_mush_stirfry", "postgap_labneh_eggs"),
    ("kiwi_smoothie", "pork_couscous", "falafel_tzatziki"),
    ("mush_toastie", LO+"pork_couscous", "greek_plate"),
    ("pancakes", "mush_risotto", "hummus_bread")]),
]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
TRAIN = [
  {"class": "Rest day", "type": "rest", "time": ""},
  {"class": "GAP", "type": "strength", "time": "Morning"},
  {"class": "V-Power", "type": "strength", "time": "Morning"},
  {"class": "GAP", "type": "strength", "time": "Evening"},
  {"class": "Cycling or GAP", "type": "cardio", "time": "Morning", "note": "Pick GAP if you feel strong — lunch has enough protein for it."},
  {"class": "V-Power", "type": "strength", "time": "12:30"},
  {"class": "Run", "type": "cardio", "time": "Morning"},
]
ANCHOR = dt.date(2026, 10, 5)

def phase(cd):
    if cd <= 5:  return "Bleed (menstrual)", "Iron + vitamin C, warm meals, smooth soups OK. Train lighter if tired."
    if cd <= 12: return "Follicular", "Fresh, lighter meals, lean protein. Energy rising — good strength days."
    if cd <= 16: return "Ovulation window" + (" (est. ovulation)" if cd == 14 else ""), "Colourful fruit & veg, antioxidants, balanced plates. Highest energy."
    if cd <= 21: return "Luteal (early)", "Complex carbs, magnesium, grounding meals. Steady blood sugar."
    return "Luteal (late)", "Comfort carbs, magnesium (oats, cocoa, almonds, beans, greens). Don't under-eat."

def mealobj(slot, d):
    m = {"slot": slot, "light": d.get("light", False), "dish": d["dish"], "note": d["note"],
         "equipment": d["equipment"], "ingredients": [[n, qty(a, u)] for n, a, u, c in d["ingredients"]],
         "steps": d["steps"]}
    ends = [int(re.findall(r"\d+", s["at"])[-1]) for s in d["steps"] if re.findall(r"\d+", s["at"])]
    m["minutes"] = max(ends) if ends else 5
    if d.get("swaps"): m["swaps"] = d["swaps"]
    if d.get("recipeRef"): m["recipeRef"] = d["recipeRef"]
    if d.get("leftoverOf"): m["leftoverOf"] = d["leftoverOf"]
    return m

CATS = OrderedDict([("F", "Fruta y verdura"), ("C", "Carne y pescado"), ("L", "Huevos, lácteos y refrigerados"), ("D", "Despensa"), ("Z", "Congelados"), ("X", "Tienda libanesa (you buy)"), ("P", "Check pantry")])
BUYHINT = {"Huevos": "docena", "Ajo": "1 cabeza", "Perejil fresco": "1 manojo", "Menta o eneldo fresco": "1 manojo", "Cebolleta": "1 manojo",
           "Crispbread de centeno (your usual)": "1–2 paquetes", "Ensalada mezclum": "bolsas", "Espinacas baby": "bolsa"}

# English names for the shopping list only — the per-meal ingredient lists and recipe
# steps stay in Spanish (Mercadona product names, same store); this is purely so the
# shopping list itself reads in English. Falls back to the Spanish name if a new
# ingredient is added here and not yet translated, rather than erroring.
EN = {
    "Aceitunas negras / kalamata": "Black olives / kalamata", "Aceitunas verdes": "Green olives",
    "Aguacate": "Avocado", "Ajo": "Garlic", "Ajo en polvo": "Garlic powder", "Alioli": "Garlic mayo (alioli)",
    "Almendras naturales": "Almonds (plain)", "Alubias blancas cocidas": "White beans, cooked",
    "Alubias rojas cocidas": "Red beans, cooked", "Arroz basmati": "Basmati rice", "Arroz redondo": "Risotto rice",
    "Boniato": "Sweet potato", "Brócoli (floretes)": "Broccoli (florets)", "Cacao puro": "Pure cocoa powder",
    "Calabacín": "Courgette (zucchini)", "Calabaza troceada": "Pumpkin/squash, diced",
    "Caldo de verduras": "Vegetable stock", "Canela": "Cinnamon", "Carne picada de ternera": "Beef mince",
    "Cebolla": "Onion", "Cebolla roja": "Red onion", "Cebolleta": "Spring onion", "Chalota": "Shallot",
    "Champiñón laminado": "Mushrooms, sliced", "Coles de Bruselas": "Brussels sprouts",
    "Copos de avena": "Rolled oats", "Crispbread de centeno (your usual)": "Rye crispbread (your usual)",
    "Cuscús": "Couscous", "Ensalada mezclum": "Mixed salad leaves", "Espaguetis": "Spaghetti",
    "Espinacas baby": "Baby spinach", "Falafel": "Falafel", "Farfalle": "Farfalle (bow-tie pasta)",
    "Filete de añojo (ternera)": "Beef steak (young beef)", "Filetes de lomo de cerdo": "Pork loin steaks",
    "Frutos rojos": "Mixed berries", "Granola sin azúcar añadido": "Granola, no added sugar",
    "Guisantes": "Peas", "Habitas baby": "Baby broad beans", "Huevos": "Eggs", "Hummus": "Hummus",
    "Jamón cocido": "Cooked ham", "Jamón serrano en lonchas": "Serrano ham, sliced",
    "Judías verdes": "Green beans", "Kale": "Kale", "Kiwi": "Kiwi", "Kéfir": "Kefir", "Labneh": "Labneh",
    "Leche": "Milk", "Lechuga (cogollos)": "Lettuce (little gem)", "Lima": "Lime", "Limón": "Lemon",
    "Lomos de salmón": "Salmon fillets", "Macarrones / pasta corta": "Macaroni / short pasta",
    "Macarrones / rigatoni": "Macaroni / rigatoni", "Maicena": "Cornflour", "Mantequilla": "Butter",
    "Manzana": "Apple", "Menta o eneldo fresco": "Fresh mint or dill", "Miel": "Honey", "Mostaza": "Mustard",
    "Nata para cocinar ligera": "Light cooking cream", "Orégano": "Oregano", "Pan de centeno": "Rye bread",
    "Pan de pita": "Pitta bread", "Pan rallado": "Breadcrumbs", "Parmesano rallado": "Grated parmesan",
    "Patata": "Potato", "Patata baby": "Baby potatoes", "Pechuga de pavo en filetes": "Turkey breast fillets",
    "Pechuga de pavo en lonchas": "Turkey breast, sliced", "Pechuga de pollo en filetes": "Chicken breast fillets",
    "Pepino": "Cucumber", "Pera": "Pear", "Perejil fresco": "Fresh parsley",
    "Pimentón dulce": "Sweet smoked paprika", "Pimiento asado (bote)": "Roasted red pepper (jarred)",
    "Pimiento rojo": "Red pepper", "Pimientos tricolor": "Mixed peppers (tricolour)",
    "Pipas de calabaza": "Pumpkin seeds", "Plátano": "Banana", "Queso cottage": "Cottage cheese",
    "Queso crema": "Cream cheese", "Queso en lonchas (havarti o similar)": "Cheese slices (havarti or similar)",
    "Queso feta": "Feta cheese", "Queso manchego": "Manchego cheese", "Queso rallado mozzarella": "Grated mozzarella",
    "Salmón ahumado": "Smoked salmon", "Salsa de soja": "Soy sauce", "Salsa tzatziki": "Tzatziki sauce",
    "Solomillo de cerdo": "Pork tenderloin", "Sésamo": "Sesame seeds", "Tomate triturado": "Chopped tomato",
    "Vinagre de manzana": "Apple cider vinegar", "Yogur griego natural": "Greek yoghurt, plain",
    "Za'atar": "Za'atar", "Zanahoria": "Carrot",
}

def shopping(cooked):
    agg = OrderedDict()
    for d in cooked:
        for n, a, u, c in d["ingredients"]:
            un = {"cloves": "clove", "slices": "slice", "handfuls": "handful", "fillet (~130 g)": "fillet"}.get(u, u)
            k = (c, n, un if isinstance(a, (int, float)) else "")
            if k not in agg: agg[k] = [0, [], c]
            if isinstance(a, (int, float)): agg[k][0] += a
            elif a or u: agg[k][1].append((a + " " + u).strip())
    out = OrderedDict((v, []) for v in CATS.values())
    pantry = set()
    seen = set()
    for (c, n, u), (tot, extra, _) in agg.items():
        if c == "P": pantry.add(n); continue
        if n in seen and n in ("Ajo", "Perejil fresco", "Menta o eneldo fresco", "Cebolleta"): continue
        seen.add(n)
        if u == "" and isinstance(tot, (int, float)) and tot and not float(tot).is_integer() and n not in ("Huevos",):
            import math; tot = math.ceil(tot)
        if n == "Ajo": out[CATS[c]].append([n, "1 head"]); continue
        if n in ("Perejil fresco", "Menta o eneldo fresco", "Cebolleta"): out[CATS[c]].append([n, "1 bunch"]); continue
        if n == "Crispbread de centeno (your usual)": out[CATS[c]].append([n, f"{fmt(tot)} pieces → 1 pack"]); continue
        if n == "Huevos": out[CATS[c]].append([n, f"{fmt(tot)} → 1 dozen" if tot <= 12 else f"{fmt(tot)} → 2 dozen"]); continue
        if u == "handful" and n in ("Ensalada mezclum", "Espinacas baby", "Kale"):
            out[CATS[c]].append([n, f"{fmt(tot)} handfuls → {max(1, round(tot / 5 + 0.49))} bag(s)"]); continue
        if n == "Pan de centeno": out[CATS[c]].append([n, f"{fmt(tot)} slices → 1 loaf"]); continue
        if u == "fillet": out[CATS[c]].append([n, f"{fmt(tot)} fillet(s), ~130 g each"]); continue
        if u in ("tbsp", "tsp", "pinch", "slice", "pieces") and n not in ("Queso en lonchas (havarti o similar)", "Jamón cocido"):
            label = {"Hummus": "tub(s)", "Salsa tzatziki": "tub", "Labneh": "tub", "Za'atar": "pot", "Queso crema": "tub", "Alioli": "jar"}.get(n, "")
            out[CATS[c]].append([n, (f"{fmt(tot)} {u}" + (f" → {label}" if label else "")).strip()]); continue
        q = qty(tot, u) if tot else ""
        if extra: q = (q + " + " if q else "") + ", ".join(sorted(set(extra)))
        out[CATS[c]].append([n, q])
    for k in list(out):
        merged = OrderedDict()
        for n, q in out[k]:
            merged[n] = (merged[n] + " + " + q) if n in merged and q else (merged.get(n) or q)
        out[k] = [[EN.get(n, n), q] for n, q in merged.items()]
    out[CATS["P"]] = [[EN.get(p, p), "check"] for p in sorted(pantry, key=lambda p: EN.get(p, p))]
    return [{"category": k, "items": v} for k, v in out.items() if v]

weeks_json = []
for wid, label, tagline, rows in WEEKS:
    monday = dt.date.fromisocalendar(2026, int(wid[-2:]), 1)
    days, cooked = [], []
    for i, (b, l, dn) in enumerate(rows):
        date = monday + dt.timedelta(days=i)
        cd = (date - ANCHOR).days % 28 + 1
        ph, focus = phase(cd)
        meals = [mealobj("Breakfast", B[b])]; cooked.append(B[b])
        if l.startswith(LO):
            meals.append(mealobj("Lunch", leftover(l[3:])))
        else:
            meals.append(mealobj("Lunch", L[l])); cooked.append(L[l])
        meals.append(mealobj("Dinner", D[dn])); cooked.append(D[dn])
        days.append({"day": DAYS[i], "date": date.isoformat(), "training": TRAIN[i],
                     "cycle": {"day": cd, "phase": ph, "focus": focus}, "meals": meals})
    w = {"id": wid, "label": label, "index": "Week " + wid[-2:], "tagline": tagline,
         "cycle": {"mode": "natural (practice — currently on the pill)", "anchor": "Day 1 = Mon 5 Oct 2026, 28-day cycle, bleed Mon–Fri",
                   "summary": f"Cycle days {days[0]['cycle']['day']}–{days[-1]['cycle']['day']}: {tagline.split('.')[0]}."},
         "soupRule": "Soups only in the bleed week, only smooth blended (cremas) or clear broth with noodles.",
         "days": days, "shopping": shopping(cooked)}
    weeks_json.append(w)
    json.dump(w, open(f"plan/{wid}.json", "w"), ensure_ascii=False, indent=2)

# ---------------------------------------------------------------- markdown
MD = ["# Month plan — 19 Oct to 15 Nov 2026\n",
      "Practice natural cycle (as if off the pill): day 1 = Mon 5 Oct. Lunches cooked ×2 (Mon→Tue, Wed→Thu, Fri→Sat), Sunday fresh. Dinners are light Mediterranean plates. Weekday dishes ≤25 min, weekend ≤35 min.\n"]
for w in weeks_json:
    MD.append(f"\n---\n\n# {w['index']} · {w['label']}\n_{w['tagline']}_\n")
    for d in w["days"]:
        t = d["training"]; c = d["cycle"]
        MD.append(f"## {d['day']} {d['date'][8:]}/{d['date'][5:7]} — {t['class']}{' ('+t['time']+')' if t['time'] else ''} · Cycle day {c['day']}: {c['phase']}")
        MD.append(f"_{c['focus']}_\n")
        for m in d["meals"]:
            MD.append(f"### {m['slot']} · {m['dish']} — {m['minutes']} min")
            MD.append(m["note"])
            MD.append("What you need: " + ", ".join(m["equipment"]))
            if m.get("swaps"): MD.append("Swapped for you: " + " ".join(m["swaps"]))
            if m["ingredients"]: MD.append("Ingredients: " + ", ".join(f"{n} {q}".strip() for n, q in m["ingredients"]))
            MD += [f"- **{s['at']}** — {s['text']}" for s in m["steps"]] + [""]
    MD.append(f"## Shopping list — {w['index']}")
    for c in w["shopping"]:
        MD.append(f"**{c['category']}:** " + "; ".join(f"{n} ({q})" if q else n for n, q in c["items"]))
open("plan/month-plan.md", "w").write("\n".join(MD) + "\n")
print("ok", [w["id"] for w in weeks_json])
