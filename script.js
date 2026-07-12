async function loadWeek() {
  const res = await fetch('data/week.json');
  const week = await res.json();

  document.getElementById('week-label').textContent = week.weekLabel;
  document.getElementById('dislikes-list').textContent = week.profile.dislikes.join(', ');
  document.getElementById('profile-notes').textContent = week.profile.notes;

  renderRhythm(week.mealTimes);
  renderDays(week.days);
  renderTraining(week.training);
  renderShoppingList(week.shoppingList);
}

function renderRhythm(mealTimes) {
  const container = document.getElementById('rhythm-container');
  container.innerHTML = mealTimes.map(m => `
    <div class="rhythm-card">
      <div class="rhythm-meal">${m.meal}</div>
      <div class="rhythm-window">${m.window}</div>
      <div class="rhythm-note">${m.note}</div>
    </div>
  `).join('');
}

function renderTraining(training) {
  const target = document.querySelector('.training .eyebrow');
  if (target) target.nextElementSibling.insertAdjacentHTML('afterend',
    `<p class="training-target">${training.weeklyTarget}</p>`);
  const container = document.getElementById('training-container');
  container.innerHTML = training.schedule.map(d => `
    <div class="training-card ${d.type} ${d.priority ? 'priority' : ''}">
      <div class="training-day">${d.day}</div>
      <div class="training-class">${d.class}</div>
      <div class="training-type">${d.priority ? '★ strength' : d.type}</div>
      ${d.note ? `<div class="training-note">${d.note}</div>` : ''}
    </div>
  `).join('');
}

function ingredientListHTML(ingredients) {
  return `<ul class="ingredient-list">${ingredients.map(i =>
    `<li><span>${i.item}</span><span class="qty">${i.qty}</span></li>`
  ).join('')}</ul>`;
}

function mealHTML(slotLabel, meal, isDinner) {
  const slotMarkup = isDinner
    ? `<span class="light-tag">${slotLabel}</span>`
    : slotLabel;
  return `
    <div class="meal ${slotLabel.toLowerCase()}">
      <div class="meal-slot">${slotMarkup}</div>
      <div class="meal-name">${meal.name}</div>
      ${meal.note ? `<div class="meal-note">${meal.note}</div>` : ''}
      ${ingredientListHTML(meal.ingredients)}
    </div>
  `;
}

function renderDays(days) {
  const container = document.getElementById('days-container');
  container.innerHTML = days.map(day => `
    <article class="day-card">
      <h3 class="day-name">${day.day}</h3>
      <div class="meals">
        ${mealHTML('Breakfast', day.breakfast, false)}
        ${mealHTML('Lunch', day.lunch, false)}
        ${mealHTML('Dinner', day.dinner, true)}
      </div>
    </article>
  `).join('');
}

function renderShoppingList(shoppingList) {
  const container = document.getElementById('shopping-container');
  container.innerHTML = Object.entries(shoppingList).map(([category, items]) => `
    <div class="shop-category">
      <h3>${category}</h3>
      <ul>
        ${items.map(i => `<li><span>${i.item}</span><span class="qty">${i.qty}</span></li>`).join('')}
      </ul>
    </div>
  `).join('');
}

loadWeek().catch(err => {
  console.error('Could not load week.json', err);
  document.getElementById('week-label').textContent = 'Could not load this week\'s plan';
});
