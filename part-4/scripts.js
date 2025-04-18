/**
 * Récupère la valeur d'un cookie selon son nom.
 */
function getCookie(name) {
  const cookies = document.cookie.split(";");
  for (let cookie of cookies) {
    const [key, value] = cookie.trim().split("=");
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
  const token = getCookie("token");
  const loginLink = document.getElementById("login-link");

  if (!token) {
    if (loginLink) loginLink.style.display = "block";
  } else {
    if (loginLink) loginLink.style.display = "none";
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
    const headers = { "Content-Type": "application/json" };
    if (token) headers["Authorization"] = "Bearer " + token;
    const response = await fetch("http://127.0.0.1:5000/api/v1/places/", {
      method: "GET",
      headers: headers,
      credentials: "include",
    });
    if (response.ok) {
      const data = await response.json();
      displayPlaces(data);
    } else {
      console.error("Erreur lors de la récupération des places :", response.statusText);
    }
  } catch (error) {
    console.error("Erreur lors de la récupération des places :", error);
  }
}

/**
 * Affiche les lieux dans la section #places-list.
 */
function displayPlaces(places) {
  const list = document.getElementById("places-list");
  if (!list) return;
  list.innerHTML = "";

  const token = getCookie("token");

  places.forEach((place) => {
    const card = document.createElement("div");
    card.className = "place-card";
    card.setAttribute("data-price", place.price);

    let buttonHTML = "";
    if (token) {
      buttonHTML = `<button class="btn" onclick="viewDetails('${place.id}')">View Details</button>`;
    } else {
      buttonHTML = `<button class="btn" onclick="redirectToLogin()">View Details</button>`;
    }

    card.innerHTML = `
      <h3>${place.title}</h3>
      <p>Price: $${place.price} per night</p>
      <p>${place.description}</p>
      ${buttonHTML}
    `;
    list.appendChild(card);
  });
}

function redirectToLogin() {
  alert("Vous devez être connecté pour voir les détails.");
  window.location.href = "login.html";
}

function viewDetails(placeId) {
  window.location.href = `place.html?id=${placeId}`;
}

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id");
}

function checkAuthenticationAndLoadDetails() {
  const token = getCookie("token");
  const placeId = getPlaceIdFromURL();
  const addReviewSection = document.getElementById("add-review");

  if (!placeId) {
    console.error("Aucun ID de lieu dans l'URL.");
    return;
  }

  if (!token) {
    if (addReviewSection) addReviewSection.style.display = "none";
    fetchPlaceDetails(null, placeId);
  } else {
    if (addReviewSection) addReviewSection.style.display = "block";
    fetchPlaceDetails(token, placeId);
  }
}

async function fetchPlaceDetails(token, placeId) {
  try {
    const headers = { "Content-Type": "application/json" };
    if (token) headers["Authorization"] = "Bearer " + token;

    console.log("Fetching details for place ID:", placeId);

    const res = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
      method: "GET",
      headers,
    });

    if (!res.ok) throw new Error("Erreur API lors de la récupération des détails du lieu");

    const place = await res.json();
    displayPlaceDetails(place);
    loadReviews(placeId);
  } catch (err) {
    console.error("Erreur lors du chargement des détails du lieu :", err);
  }
}


function displayPlaceDetails(place) {
  document.getElementById("place-name").textContent = place.title;
  document.getElementById("place-host").textContent = `Host: ${place.owner.first_name} ${place.owner.last_name}`;
  document.getElementById("place-price").textContent = `Price: $${place.price}`;
  document.getElementById("place-description").textContent = `Description: ${place.description}`;

  const amenitiesIcons = {
    "Wifi": "<img src='./images/icon_wifi.png' alt='Wifi' style='height:20px; vertical-align:middle;'>",
    "Bathroom": "<img src='./images/icon_bath.png' alt='Bathroom' style='height:20px; vertical-align:middle;'>",
    "Bed": "<img src='./images/icon_bed.png' alt='Bed' style='height:20px; vertical-align:middle;'>"
  };

  if (place.amenities.length === 0) {
    document.getElementById("place-amenities").innerHTML = "Amenities: None";
  } else {
    const amenityList = place.amenities.map(a => {
      return `${amenitiesIcons[a.name] || ""} ${a.name}`;
    }).join(" | ");
    document.getElementById("place-amenities").innerHTML = `Amenities: ${amenityList}`;
  }

  document.getElementById("place-image").src = place.image || "https://www.costas-casas.fr/db/huizen/1357/123765-2_57.jpg";
}

async function loadReviews(placeId) {
  try {
    const res = await fetch("http://127.0.0.1:5000/api/v1/reviews/");
    if (!res.ok) throw new Error("Erreur chargement reviews");

    const allReviews = await res.json();
    const reviews = allReviews.filter(r => r.place_id === placeId);

    const reviewsContainer = document.getElementById("reviews");
    reviewsContainer.innerHTML = "<h3>Reviews</h3>";

    if (reviews.length === 0) {
      reviewsContainer.innerHTML += "<p>No reviews yet.</p>";
    } else {
      reviews.forEach(r => {
        const el = document.createElement("article");
        el.className = "review-card";
        el.innerHTML = `<p>"${r.text}"</p><p>Rating: ${r.rating}/5</p>`;
        reviewsContainer.appendChild(el);
      });
    }
  } catch (err) {
    console.error("Erreur chargement des reviews :", err);
  }
}

function initPriceFilter() {
  const priceFilter = document.getElementById("price-filter");
  if (priceFilter) {
    priceFilter.addEventListener("change", (event) => {
      const selected = event.target.value;
      console.log("Filtrage des lieux avec la valeur :", selected);
      const placeCards = document.querySelectorAll(".place-card");
      placeCards.forEach((card) => {
        const price = parseFloat(card.getAttribute("data-price"));
        if (selected === "All") {
          card.style.display = "block";
        } else {
          const maxPrice = parseFloat(selected);
          card.style.display = price <= maxPrice ? "block" : "none";
        }
      });
    });
  }
}

async function loginUser(email, password) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login/', {
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

function displayError(elementId, message) {
  const el = document.getElementById(elementId);
  if (el) {
    el.textContent = message;
    el.style.display = "block";
  } else {
    alert(message);
  }
}

function displaySuccess(elementId, message) {
  const el = document.getElementById(elementId);
  if (el) {
    el.textContent = message;
  } else {
    alert(message);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  if (document.body.id === "index-page") {
    checkAuthentication();
    initPriceFilter();
  }

  if (document.body.id === "place-page") {
    checkAuthenticationAndLoadDetails();
  }

  const loginForm = document.getElementById("login-form");
  if (loginForm) {
    loginForm.addEventListener("submit", (evt) => {
      evt.preventDefault();
      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;
      loginUser(email, password);
    });
  }
});


// Gestion du formulaire d'ajout de review (add_review.html) avec console.log pour debug

document.addEventListener("DOMContentLoaded", () => {
  if (document.body.id === "add-review-page") {
    console.log("Page add_review.html chargée");
    const token = getCookie("token");
    if (!token) {
      console.warn("Aucun token trouvé - Redirection vers index.html");
      window.location.href = "index.html";
    }

    const placeId = getPlaceIdFromURL();
    console.log("ID du lieu extrait de l'URL :", placeId);

    const reviewForm = document.getElementById("review-form");

    if (reviewForm) {
      reviewForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        console.log("Soumission du formulaire d'avis détectée");

        const reviewText = document.getElementById("review").value;
        const rating = document.getElementById("rating").value;
        console.log("Contenu de l'avis :", reviewText, "Note :", rating);

        try {
          const response = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify({
              text: reviewText,
              rating: parseInt(rating),
              place_id: placeId
            })
          });

          if (response.ok) {
            console.log("Avis ajouté avec succès");
            alert("Review submitted successfully!");
            reviewForm.reset();
          } else {
            console.error("Erreur lors de la soumission de l'avis - Status :", response.status);
            alert("Failed to submit review.");
          }
        } catch (error) {
          console.error("Erreur lors de l'envoi de l'avis :", error);
          alert("Erreur lors de l'envoi de l'avis.");
        }
      });
    } else {
      console.error("Formulaire d'avis introuvable dans la page");
    }
  }
});
