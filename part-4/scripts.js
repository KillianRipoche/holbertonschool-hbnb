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
 * Vérifie l'authentification et ajuste la visibilité du lien "Login".
 * Indépendamment de l'authentification, on charge la liste des lieux.
 */
function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!token) {
    if (loginLink) loginLink.style.display = 'block';
  } else {
    if (loginLink) loginLink.style.display = 'none';
  }
  // On récupère les lieux que l'utilisateur soit authentifié ou non
  fetchPlaces(token);
}

/**
 * Récupère la liste des lieux depuis l'API.
 * Si un token est fourni, il sera inclus dans l'en-tête Authorization.
 * En cas d'erreur, on utilise des données d'exemple.
 */
async function fetchPlaces(token) {
  try {
    const headers = { 'Content-Type': 'application/json' };
    if (token) {
      headers['Authorization'] = 'Bearer ' + token;
    }
    const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
      method: 'GET',
      headers: headers,
      credentials: 'include'
    });
    if (response.ok) {
      const data = await response.json();
      console.log("Places récupérées :", data);
      window.allPlaces = data;
      displayPlaces(data);
    } else {
      console.error("Erreur lors de la récupération des places :", response.statusText);
      window.allPlaces = samplePlaces();
      displayPlaces(window.allPlaces);
    }
  } catch (error) {
    console.error("Erreur lors de la récupération des places :", error);
    window.allPlaces = samplePlaces();
    displayPlaces(window.allPlaces);
  }
}

/**
 * Donne des données d'exemple pour les lieux.
 */
function samplePlaces() {
  return [
    {
      id: "1",
      name: "Beach House",
      host: "John Doe",
      price: 100,
      description: "Une magnifique maison en bord de mer, idéale pour des vacances d'été inoubliables.",
      amenities: "Wi-Fi, Kitchen, Heating",
      image: "https://source.unsplash.com/800x500/?beach,house"
    },
    {
      id: "2",
      name: "Cozy Cabin",
      host: "Jane Smith",
      price: 75,
      description: "Un chalet chaleureux niché au cœur des bois, parfait pour se ressourcer.",
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
      description: "Une villa spacieuse et luxueuse avec piscine, idéale pour des séjours haut de gamme.",
      amenities: "Pool, Private Chef, Butler",
      image: "https://source.unsplash.com/800x500/?villa,luxury"
    }
  ];
}

/**
 * Affiche les lieux dans la section #places-list.
 */
function displayPlaces(places) {
  const list = document.getElementById('places-list');
  if (!list) return;
  list.innerHTML = '';

  // Récupérer le token pour déterminer la fonctionnalité du bouton
  const token = getCookie('token');

  places.forEach(place => {
    const card = document.createElement('div');
    card.className = 'place-card';
    card.setAttribute('data-price', place.price);

    let buttonHTML = '';
    if (token) {
      buttonHTML = `<button class="btn" onclick="viewDetails('${place.id}')">View Details</button>`;
    } else {
      buttonHTML = `<button class="btn" onclick="redirectToLogin()">View Details</button>`;
    }

    card.innerHTML = `
      <h3>${place.name}</h3>
      <p>Price: $${place.price} per night</p>
      <p>${place.description}</p>
      ${buttonHTML}
    `;
    list.appendChild(card);
  });
}

/**
 * Redirige l'utilisateur vers la page de login si non authentifié.
 */
function redirectToLogin() {
  alert("Vous devez être connecté pour voir les détails.");
  window.location.href = 'login.html';
}

/**
 * Recherche le lieu via son ID, le stocke dans localStorage et redirige vers place.html.
 */
function viewDetails(placeId) {
  if (!window.allPlaces) {
    console.warn("Aucune place n'a été chargée");
    return;
  }
  const selected = window.allPlaces.find(p => p.id === placeId);
  if (!selected) {
    console.error("Lieu non trouvé:", placeId);
    return;
  }
  localStorage.setItem("selectedPlace", JSON.stringify(selected));
  window.location.href = "place.html";
}

/**
 * Charge les détails du lieu depuis le localStorage sur la page place.html.
 */
function loadPlaceDetails() {
  const raw = localStorage.getItem("selectedPlace");
  if (!raw) {
    console.error("Aucun lieu sélectionné dans le localStorage.");
    return;
  }
  const place = JSON.parse(raw);

  document.getElementById("place-name").textContent = place.name || "Nom non défini";
  document.getElementById("place-host").textContent = `Host: ${place.host || "Non défini"}`;
  document.getElementById("place-price").textContent = `Price: $${place.price || "N/A"} per night`;
  document.getElementById("place-description").textContent = `Description: ${place.description || "N/A"}`;
  document.getElementById("place-amenities").textContent = `Amenities: ${place.amenities || "Aucune"}`;
  const placeImg = document.getElementById("place-image");
  if (placeImg) {
    placeImg.src = place.image || "https://via.placeholder.com/800x500?text=No+Image";
  }
}

/**
 * Gestion du filtre de prix (mise à jour lorsque la valeur change).
 */
function initPriceFilter() {
  const priceFilter = document.getElementById('price-filter');
  if (priceFilter) {
    priceFilter.addEventListener('change', (event) => {
      const selected = event.target.value;
      console.log("Filtrage des lieux avec la valeur :", selected);
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
}

/**
 * Fonction pour gérer le login via login.html.
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
    console.error("Erreur lors du login", error);
    displayError("error-message", "Une erreur est survenue lors du login.");
  }
}

/**
 * Affiche un message d'erreur dans un élément identifié par son ID.
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
 * Affiche un message de succès dans un élément identifié par son ID.
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
 * Initialisation lors du chargement du document.
 */
document.addEventListener('DOMContentLoaded', () => {
  // Si on est sur index.html, vérifier l'authentification, charger les lieux et initialiser le filtre.
  if (document.body.id === "index-page") {
    checkAuthentication();
    initPriceFilter();
  }

  // Si on est sur place.html, charger les détails du lieu.
  if (document.body.id === "place-page") {
    loadPlaceDetails();
  }

  // Si on est sur login.html, attacher l'écouteur d'événement pour le formulaire de login.
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
