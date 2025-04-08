/**
 * Récupère la valeur d'un cookie selon son nom.
 */
function getCookie(name) {
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const [key, value] = cookie.trim().split('=');
    if (key === name) {
      return value;
    }
  }
  return null;
}

/**
 * Vérifie l'authentification (token) et affiche/masque le lien de login.
 * Si on est sur index, on charge les places si token existe.
 */
function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  if (!token) {
    // Pas de token : afficher le lien de login
    if (loginLink) loginLink.style.display = 'block';
  } else {
    // Token présent : masquer le lien de login et fetch places
    if (loginLink) loginLink.style.display = 'none';
    fetchPlaces(token);
  }
}

/**
 * Récupère la liste des lieux depuis l'API (ou fallback samplePlaces).
 * On stocke le résultat dans window.allPlaces pour s'en servir plus tard.
 */
async function fetchPlaces(token) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
      },
      credentials: 'include'
    });

    if (response.ok) {
      const data = await response.json();
      console.log("Places récupérées :", data);
      window.allPlaces = data;         // mémorise la liste
      displayPlaces(data);
    } else {
      console.error("Erreur fetch places:", response.statusText);
      window.allPlaces = samplePlaces();
      displayPlaces(window.allPlaces);
    }
  } catch (error) {
    console.error("Erreur fetch places:", error);
    window.allPlaces = samplePlaces();
    displayPlaces(window.allPlaces);
  }
}

/**
 * Données d'exemple + host, amenities, image
 */
function samplePlaces() {
  return [
    {
      id: "1",
      name: "Beach House",
      host: "John Doe",
      price: 100,
      description: "Une superbe maison au bord de la mer, idéale pour un séjour estival inoubliable.",
      amenities: "Wi-Fi, Kitchen, Heating",
      image: "https://source.unsplash.com/800x500/?beach,house"
    },
    {
      id: "2",
      name: "Cozy Cabin",
      host: "Jane Smith",
      price: 75,
      description: "Un chalet chaleureux dans les bois, parfait pour se ressourcer au calme.",
      amenities: "Fireplace, Sauna, Parking",
      image: "https://source.unsplash.com/800x500/?cabin,forest"
    },
    {
      id: "3",
      name: "City Apartment",
      host: "Mike Johnson",
      price: 150,
      description: "Appartement moderne en centre-ville, proche de toutes commodités.",
      amenities: "Wi-Fi, Air Conditioning, Elevator",
      image: "https://source.unsplash.com/800x500/?apartment,city"
    },
    {
      id: "4",
      name: "Luxury Villa",
      host: "Alice Wonder",
      price: 250,
      description: "Spacieuse villa avec piscine et vue imprenable, idéale pour un séjour de luxe.",
      amenities: "Pool, Private Chef, Butler",
      image: "https://source.unsplash.com/800x500/?villa,luxury"
    }
  ];
}

/**
 * Affiche la liste des lieux dans #places-list (index.html).
 */
function displayPlaces(places) {
  const list = document.getElementById('places-list');
  if (!list) return; // si on n'est pas sur index.html
  list.innerHTML = '';

  places.forEach(place => {
    const card = document.createElement('div');
    card.className = 'place-card';
    card.setAttribute('data-price', place.price);

    card.innerHTML = `
      <h3>${place.name}</h3>
      <p>Price: $${place.price} per night</p>
      <p>${place.description}</p>
      <button class="btn" onclick="viewDetails('${place.id}')">View Details</button>
    `;
    list.appendChild(card);
  });
}

/**
 * Filtrage côté client sur index.html via #price-filter
 */
const priceFilter = document.getElementById('price-filter');
if (priceFilter) {
  priceFilter.addEventListener('change', (event) => {
    const selected = event.target.value;
    const placeCards = document.querySelectorAll('.place-card');
    placeCards.forEach(card => {
      const price = parseFloat(card.getAttribute('data-price'));
      if (selected === 'All') {
        card.style.display = 'block';
      } else {
        const maxPrice = parseFloat(selected);
        card.style.display = (price <= maxPrice) ? 'block' : 'none';
      }
    });
  });
}

/**
 * En cliquant sur "View Details", on retrouve l'objet place dans window.allPlaces,
 * on le stocke sous forme JSON dans localStorage, puis on redirige vers place.html.
 */
function viewDetails(placeId) {
  if (!window.allPlaces) {
    console.warn("Aucune place chargée");
    return;
  }
  const selected = window.allPlaces.find(p => p.id === placeId);
  if (!selected) {
    console.error("Lieu non trouvé:", placeId);
    return;
  }

  // Stockage JSON
  localStorage.setItem("selectedPlace", JSON.stringify(selected));

  window.location.href = "place.html";
}

/**
 * Sur place.html, on récupère l'objet stocké dans localStorage et on met à jour la page.
 */
function loadPlaceDetails() {
  const raw = localStorage.getItem("selectedPlace");
  if (!raw) {
    console.error("Aucun lieu sélectionné dans localStorage");
    return; // ou afficher un message d'erreur
  }
  const place = JSON.parse(raw);

  // Mise à jour de tous les champs
  document.getElementById("place-name").textContent = place.name || "No name";
  document.getElementById("place-host").textContent = `Host: ${place.host || "Unknown"}`;
  document.getElementById("place-price").textContent = `Price: $${place.price || "N/A"} per night`;
  document.getElementById("place-description").textContent = `Description: ${place.description || "N/A"}`;
  document.getElementById("place-amenities").textContent = `Amenities: ${place.amenities || "None"}`;
  const placeImg = document.getElementById("place-image");
  if (placeImg) {
    placeImg.src = place.image || "https://via.placeholder.com/800x500?text=No+Image";
  }
}

/**
 * Authentification login
 */
async function loginUser(email, password) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ email, password })
    });

    if (response.ok) {
      const data = await response.json();
      const token = data.access_token || data.token;
      if (!token) {
        displayError("error-message", "La réponse ne contient pas de token.");
        return;
      }
      document.cookie = `token=${token}; path=/;`;
      displaySuccess("login-message", "Connexion réussie ! Redirection...");
      setTimeout(() => { window.location.href = 'index.html'; }, 1500);
    } else {
      displayError("error-message", "Login failed: " + response.statusText);
    }
  } catch (error) {
    console.error("Login error", error);
    displayError("error-message", "Une erreur est survenue lors du login.");
  }
}

/**
 * Affiche un message d'erreur dans un élément par ID
 */
function displayError(elementId, message) {
  const el = document.getElementById(elementId);
  if (el) {
    el.textContent = message;
    el.style.display = "block";
  } else {
    alert(message);
  }
}

/**
 * Affiche un message de succès dans un élément par ID
 */
function displaySuccess(elementId, message) {
  const el = document.getElementById(elementId);
  if (el) {
    el.textContent = message;
  } else {
    alert(message);
  }
}

/**
 * Setup sur la page login
 */
document.addEventListener('DOMContentLoaded', () => {
  // Sur index.html : checkAuth
  if (document.body.id === "index-page") {
    checkAuthentication();
  }

  // Sur place.html : loadPlaceDetails
  if (document.body.id === "place-page") {
    loadPlaceDetails();
  }


  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', (evt) => {
      evt.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      loginUser(email, password);
    });
  }
});
