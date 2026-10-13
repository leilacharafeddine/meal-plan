# Handoff for Claude Code — The Weekly Board (meal-plan site)

From Leila, prepared with Claude on 13 Oct 2026. Read this whole file before changing anything.

Repo: `leilacharafeddine/meal-plan` · Live: https://leilacharafeddine.github.io/meal-plan/
Files that come with this handoff (attach / add to repo):
- `recipes.json` — recipe library, 29 recipes, one serving each, timed steps, swaps already applied.
- `plan-2026-W43.json`, `plan-2026-W44.json`, `plan-2026-W45.json`, `plan-2026-W46.json` — the month plan, 19 Oct – 15 Nov 2026 (one week object per file, ready to append to `data.json → weeks`).

---

## 1. What to build (checklist)

1. Copy `recipes.json` to the repo root. Load it alongside `data.json`.
2. Append the four week objects to `data.json → weeks`. Don't edit or delete past weeks.
3. Support the new fields (section 6).
4. Build the recipe bottom sheet / pop-up exactly as designed in **Claude Design** (section 7). Content rules are in section 7 — follow them.
5. Build the cycle calendar as designed in Claude Design (section 5).
6. Update the "Food I don't like" list in `data.json → standing.avoid` to match section 2.
7. Shopping categories are Mercadona sections in Spanish (section 8). Add their colours.
8. Commit and push to `main` so GitHub Pages updates. Check the live site on a phone-width screen.

---

## 2. Leila's food rules

**Cooking**
- Cooking for one. Lunch or dinner is often last night's leftovers ("cook once, eat twice").
- Weekday dishes: **25 min max**. Weekend dishes: **35 min max**.
- Lunch (14:00–16:00) is the biggest meal. Dinner (20:00–21:00) is light — except after an evening class, when it's protein-forward.
- A small side salad most days. Loves breakfast — vary breakfasts week to week.
- Shopping at **Mercadona** (Spanish product names, Hacendado where possible).

**Never use**
- Soup — EXCEPT in the bleed week, and then ONLY smooth blended soups (cremas/purés, "baby-food" texture) or a clear broth with noodles. Never chunky soups with soaked pieces.
- Lots of raw tomato (≤ 5 cherry tomatoes is fine; cooked tomato is fine).
- Cilantro / coriander leaf.
- Chilli or anything spicy/hot (no sriracha, sambal, chilli flakes, cayenne, peri peri, hot paprika).
- Heavy Indian-style spice blends (cumin, coriander, chilli-forward, ras el hanout).
- Canned tuna.
- Lentils (or only ground/blended).
- Edamame.
- Tropical fruit (mango, pineapple, coconut, passion fruit).
- Peanut butter, unless essential.
- Turkey AND chicken in the same week.

**Loves / use often**
- Salmon with alioli — every week or two.
- Almonds. Kiwi. Greek yoghurt, eggs, rye bread, avocado, feta, halloumi, white/red beans.
- Open to vegetarian meals if they're nutritious.

**Standard swaps** (already applied in the data)
- Chilli / Cajun / fajita / peri-peri seasoning → sweet smoked paprika + garlic + oregano (+ thyme).
- Coriander → parsley. Raw tomato → cucumber or roasted pepper (jar).
- Sriracha mayo → lime mayo. Sweet chilli → honey-lime glaze.

---

## 3. Equipment (only plan with this)

- **Ninja air fryer, ONE drawer** — bake, crisp, air fry, roast, reheat, dehydrate. Never plan two air-fryer things at once unless they share the drawer.
- **Rice cooker** — all rice, 2 portions at a time for leftovers.
- **Hand blender** (batidora de mano) — soups, sauces, smoothies, batters. No jug blender.
- **Microwave.** Hob with pans and pots.
- **Tiny oven** — no gratins, lasagna or bakes.
- **NO toaster** — toast = "Air fryer, 200°C, 3 min" or a dry frying pan.

---

## 4. Training (new gym, from 19 Oct 2026)

| Day | Class | Type | Time |
|---|---|---|---|
| Mon | Rest | rest | — |
| Tue | GAP | strength | Morning |
| Wed | V-Power | strength | Morning |
| Thu | GAP | strength | Evening |
| Fri | Cycling or GAP | cardio (strength if GAP) | Morning |
| Sat | V-Power | strength | 12:30 |
| Sun | Run | cardio | Morning |

- Leila is no longer injured: **no YouTube / seated workout videos** in new weeks (drop `trainingOverrideTemporary`). Leave old weeks alone.
- Meal timing follows the classes: post-gym breakfast on morning-class days; a **Snack ~18:00 before Thursday's evening GAP** and a protein dinner after; Saturday breakfast by ~10:30, protein lunch after V-Power.

---

## 5. Cycle — what the calendar shows

**Reality:** Leila takes the combined pill, 21 active pills + 7-day break (no placebo). Packs start on Saturdays. Current pack started Sat 10 Oct 2026. She bleeds Mon–Fri of the break week (4–5 days). On the pill there is no ovulation.
- Next break: Sat 31 Oct – Fri 6 Nov (bleed ~Mon 2 – Fri 6 Nov). Next pack Sat 7 Nov. Repeats every 28 days.

**This month is planned as a practice natural cycle** (as if she were off the pill), so the habits are ready if she stops it. Day 1 = Mon 5 Oct, 28-day cycle, ovulation ~14 days before the next bleed.

| Week | Dates | Cycle days | Phase | Food focus | Training feel |
|---|---|---|---|---|---|
| W43 | 19–25 Oct | 15–21 | Ovulation tail → early luteal | Colourful veg/fruit, then complex carbs + magnesium | High energy → steady |
| W44 | 26 Oct – 1 Nov | 22–28 | Late luteal | Complex carbs, magnesium (almonds, oats, beans, dark chocolate, greens), grounding meals | Moderate |
| W45 | 2–8 Nov | 1–7 | Bleed Mon–Fri → follicular | Iron (red meat, beans, spinach) + vitamin C, warm meals, smooth soups allowed | Lighter if tired |
| W46 | 9–15 Nov | 8–14 | Follicular → ovulation (~Sun 15 Nov) | Fresh, lighter, lean protein, colourful | Strength, highest energy |

- The calendar (designed in Claude Design, updated 13 Oct) should show both: the real pill bleed dates and the practice phases. Each day shows "Cycle day X · Phase".
- Keep a way to switch later between **pill mode** and **natural-cycle mode**. If she moves to a copper IUD, natural mode applies fully; with a hormonal IUD, bleeds may be light or absent, so phases come from tracking rather than bleeding.
- Source of the phase tips: women's-health workshop by Mary Delberghe (naturopath). Phase eating is coaching-level advice; the iron / protein / steady-blood-sugar / eat-enough-for-training parts are well supported.

---

## 6. Data format (new fields — render if present, ignore if missing)

Week:
- `cycle` → `{ mode, anchor, summary }` — show once at the top of the week.
- `snack` → string — optional snack tip, show once at the bottom.
- `soupRule` → string.

Day (weeks now run Monday–Sunday, 7 days):
- `date` (ISO).
- `training` → `{ class, type, time, note? }` — show the time next to the class.
- `cycle` → `{ day, phase, focus }` — small line under the training chip: "Cycle day 17 · Luteal (early)".

Meal:
- `slot` can now be `"Snack"` as well as Breakfast / Lunch / Dinner. Snack accent colour `#c98a2f`.
- `minutes` — total time. Show "20 min" by the dish name.
- `equipment` → strings, e.g. `["Rice cooker", "Air fryer"]`. Shown in the bottom sheet as **"What you need"**. Never cutlery.
- `steps` → `[{ at, text }]` — the instructions.
- `swaps` → strings — "Swapped for you".
- `recipeRef` → id in `recipes.json` (optional; the meal's own `steps` win if both exist).

Shopping categories (Mercadona sections) and colours:
`Fruta y verdura` #37b98c · `Carne y pescado` #9c3f47 · `Huevos, lácteos y refrigerados` #2f9fc9 · `Despensa` #6a8f9a · `Congelados` #1f8fb8.

---

## 7. Recipe bottom sheet / pop-up

**Design:** Leila has designed this in Claude Design (updated 13 Oct 2026). Build it to match that design — don't invent a new look. Opens from a "See recipe" button on each meal card; the button must not tick the meal as done (stop the click from reaching the card).

**Content, in this order:**
1. Dish name, meal slot, total time ("20 min"), serves 1.
2. Cycle phase + why this dish fits (one line).
3. **What you need** — the `equipment` list.
4. Swapped for you — only if there are swaps.
5. Ingredients — name + quantity, Spanish Mercadona name where given.
6. Method — each step shows its time range ("0–5 min") and one short instruction.
7. Source link (small, at the bottom) if the meal has a `recipeRef`.

**Language rules — keep every instruction like this:**
- Straight to the point. Imperative. One action per step. ~20 words max.
- Every step starts with a time range: `0–5 min`. Overnight prep = `Night before`.
- Always name the appliance and setting: "Air fryer, 200°C, 12 min." "Rice cooker, 300 ml water."
- Last step = how to plate it.
- `minutes` = end of the last step.
- No chatty filler, no "simply", no "enjoy!".

---

## 8. Shopping list

- One list per week, grouped by Mercadona section, Spanish product names, quantity to buy.
- Merge duplicates. If two items are near-identical, keep the healthier one.
- Mark pantry staples "check pantry" instead of making her buy them weekly.

---

## 9. If something isn't clear

Ask Leila — don't guess on food rules. If a recipe step would break a rule above (spice, raw tomato, time, equipment), fix it using the standard swaps in section 2.
