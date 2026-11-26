document.querySelectorAll('.star-rating').forEach(function (box) {
  var qName = box.dataset.name;
  for (var i = 10; i >= 1; i--) {
    var id = qName + '-' + i;
    box.insertAdjacentHTML(
      'beforeend',
      '<input type="radio" name="' + qName + '" id="' + id + '" value="' + i + '" required>' +
      '<label for="' + id + '" title="' + i + '">★</label>'
    );
  }
});



const form = document.getElementById('contactForm');
const result = document.getElementById('result');
const submitBtn = form.querySelector('button[type="submit"]');
const clearBtn = document.getElementById('clearBtn');

const labels = {
  vardas: 'Vardas',
  pavarde: 'Pavardė',
  email: 'El. paštas',
  titulas: 'Titulas',
  telefonas: 'Tel. numeris',
  adresas: 'Adresas',
  q1: '1 klausimas',
  q2: '2 klausimas',
  q3: '3 klausimas',
  zinute: 'Žinutė'
};

const fields = Object.keys(labels);
const touched = new Set();

function getError(name) {
  const value = form.elements[name].value.trim();

  if (value === '') return 'Šis laukas privalomas';

  if (name === 'vardas' || name === 'pavarde') {
    if (!/^\p{L}+$/u.test(value)) return 'Leidžiamos tik raidės';
  }
  if (name === 'email') {
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) return 'Neteisingas el. pašto formatas';
  }
  if (name === 'telefonas') {
    if (!/^\+370 6\d{2} \d{5}$/.test(value)) return 'Formatas: +370 6xx xxxxx';
  }
  if (name === 'q1' || name === 'q2' || name === 'q3') {
    const n = Number(value);
    if (!(n >= 1 && n <= 10)) return 'Pasirinkite įvertinimą nuo 1 iki 10';
  }
  return '';
}

function showError(name, error) {
  document.getElementById('err-' + name).textContent = error;
  const el = form.elements[name];
  if (el instanceof HTMLElement) {
    el.classList.toggle('is-invalid', error !== '');
  }
}

function update() {
  let allValid = true;
  fields.forEach(function (name) {
    const error = getError(name);
    if (error) allValid = false;
    showError(name, touched.has(name) ? error : '');
  });
  submitBtn.disabled = !allValid;
}

function formatPhone(input) {
  let digits = input.value.replace(/\D/g, '');
  if (input.value.startsWith('+370')) digits = digits.slice(3);
  digits = digits.slice(0, 8);

  if (digits === '') { input.value = ''; return; }

  let formatted = '+370 ' + digits.slice(0, 3);
  if (digits.length > 3) formatted += ' ' + digits.slice(3);
  input.value = formatted;
}

form.addEventListener('input', function (event) {
  const field = event.target;
  if (field.name === 'telefonas') formatPhone(field);
  touched.add(field.name);
  update();
});

form.addEventListener('submit', function (event) {
  event.preventDefault();
  if (submitBtn.disabled) return;

  const data = Object.fromEntries(new FormData(form));
  console.log(data);

  result.innerHTML = '';
  for (const key in data) {
    const p = document.createElement('p');
    p.textContent = labels[key] + ': ' + data[key];
    result.appendChild(p);
  }

  const avg = (Number(data.q1) + Number(data.q2) + Number(data.q3)) / 3;
  const p = document.createElement('p');
  p.textContent = data.vardas + ' ' + data.pavarde + ': ' + avg.toFixed(2);
  result.appendChild(p);
});

clearBtn.addEventListener('click', function () {
  form.reset();
  result.innerHTML = '';
  touched.clear();
  update();
});

update();