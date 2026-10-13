# Brief for Claude Code — Month plan (19 Oct – 15 Nov 2026)

Repo: leilacharafeddine/meal-plan · Live: https://leilacharafeddine.github.io/meal-plan/
Week files live in the project docs: `claude/plan-2026-W43.json` (W44–W46 follow, same shape).

## What to do
1. Append each week object from the plan file to `data.json → weeks`. Don't edit past weeks.
2. Weeks now run **Monday–Sunday** (7 days). New gym timetable (from W43):
   Mon Rest · Tue GAP (morning) · Wed V-Power (morning) · Thu GAP (evening) · Fri Cycling or GAP (morning) · Sat V-Power (12:30) · Sun Run (morning).
   `training` now has an optional `time` ("Morning", "Evening", "12:30") and optional `note`. Show the time next to the class name.
   Leila is no longer injured: drop `trainingOverrideTemporary` / YouTube workout videos from new weeks. Leave old weeks as they are.
   Meals can include a `"Snack"` slot (e.g. before an evening class) — give it an accent colour (`#c98a2f`).
3. New optional fields — render them if present, ignore if missing:
   - `day.date` (ISO), `day.cycle` → `{ day, phase, focus }`: show as a small line under the training chip, e.g. "Cycle day 17 · Luteal (early)".
   - `meal.minutes`: show as "20 min" next to the dish name.
   - `meal.steps` → `[{ at, text }]`: the cooking instructions. Show on "See recipe" (design is in Claude Design — follow that).
   - `meal.swaps` → strings: "Swapped for you" note.
   - `meal.equipment` → strings (e.g. "Air fryer", "Frying pan", "Microwave"): show in the recipe bottom sheet as "What you need". No cutlery.
   - `meal.recipeRef`: id in `recipes.json` (full recipe library, 29 recipes). Optional link only.
   - `week.cycle`, `week.snack`: show once at the top / bottom of the week.
4. Shopping categories are now Mercadona sections in Spanish: `Fruta y verdura`, `Carne y pescado`, `Huevos, lácteos y refrigerados`, `Despensa`, `Congelados`. Add them to the `catColor` map (reuse Produce / Protein / Dairy / Pantry colours; Congelados = `#1f8fb8`).
5. Copy `claude/recipes.json` (project doc) to the repo root as `recipes.json`.

## Instruction text rules (keep these when editing steps)
- One action per step. Imperative. No filler. Max ~20 words.
- Every step starts with a time range (`"0–5 min"`). Use "Night before" for overnight prep.
- Say the appliance and setting: "Air fryer, 200°C, 12 min."
- Last step = plate it.
- `minutes` = end of the last step.

## Hard rules for any edit
- Weekday dishes ≤ 25 min. Weekend ≤ 35 min.
- Never: soup (except bleed-week days), lots of raw tomato (≤ 5 cherry tomatoes OK), cilantro, chilli/spicy, heavy Indian-style spice blends, canned tuna, lentils, tropical fruit. Peanut butter only if essential.
- No turkey and chicken in the same week.
- Tiny oven — no gratins/bakes. Main appliance: Ninja air fryer, ONE drawer (bake, crisp, air fry, roast, reheat, dehydrate). Never plan two air-fryer items at the same time unless they share the drawer.
- Also owned: rice cooker (use for rice, cook 2 portions at a time), hand blender (soups, sauces, smoothies, batters — no jug blender), microwave.
- No toaster: toast = "Air fryer, 200°C, 3 min" or a dry frying pan.
- Soups: bleed week only, and only smooth blended (crema/puré) or clear broth with noodles. No chunky soups.
- Lunch is the biggest meal; dinner is light.
