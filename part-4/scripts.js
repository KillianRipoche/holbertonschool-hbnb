// Fonction pour vérifier si l'utilisateur est authentifié en lisant le cookie "token"
function checkAuth() {
  const cookies = document.cookie.split(';');
  let token = null;
  cookies.forEach(cookie => {
    const [key, value] = cookie.trim().split('=');
    if (key === 'token') {
      token = value;
    }
  });
  if (!token) {
    // Si aucun token n'est trouvé, rediriger vers la page de login
    window.location.href = 'login.html';
  }
}

// Fonction pour gérer la connexion de l'utilisateur
async function loginUser(email, password) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      // IMPORTANT : On inclut les credentials pour que les cookies soient traités correctement
      credentials: 'include',
      body: JSON.stringify({ email, password })
    });

    console.log("Statut HTTP :", response.status);

    if (response.ok) {
      const data = await response.json();
      console.log("Réponse du serveur :", data);

      // Vérifie que la réponse contient une propriété de token (adaptable selon ce que renvoie ton API)
      const token = data.access_token || data.token;
      if (!token) {
        const errorDiv = document.getElementById("error-message");
        if (errorDiv) {
          errorDiv.textContent = "Erreur : La réponse ne contient pas de token.";
          errorDiv.style.display = "block";
        } else {
          alert("Erreur : La réponse ne contient pas de token.");
        }
        return;
      }

      // Stocker le token dans un cookie (sans le flag Secure pour le développement, car le front est en HTTP)
      document.cookie = `token=${token}; path=/;`;

      // Afficher un message de succès dans l'élément dédié (si présent)
      const msgDiv = document.getElementById("login-message");
      if (msgDiv) {
        msgDiv.textContent = "Connexion réussie ! Redirection en cours...";
      } else {
        alert("Connexion réussie !");
      }

      // Rediriger vers index.html après un léger délai pour laisser le temps de lire le message
      setTimeout(() => {
        window.location.href = 'index.html';
      }, 1500);
    } else {
      console.error("Erreur lors du login :", response.statusText);
      const errorDiv = document.getElementById("error-message");
      if (errorDiv) {
        errorDiv.textContent = "Login failed: " + response.statusText;
        errorDiv.style.display = "block";
      } else {
        alert("Login failed: " + response.statusText);
      }
    }
  } catch (error) {
    console.error('Login failed', error);
    const errorDiv = document.getElementById("error-message");
    if (errorDiv) {
      errorDiv.textContent = "Une erreur est survenue lors du login.";
      errorDiv.style.display = "block";
    } else {
      alert("Une erreur est survenue lors du login.");
    }
  }
}

// Ajout de l'événement sur le formulaire de login
document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      console.log("Tentative de connexion avec l'email :", email);
      await loginUser(email, password);
    });
  }

  // Pour les pages protégées (ex. place.html), vérifie l'authentification
  if (window.location.pathname.endsWith('place.html')) {
    checkAuth();
  }

  // Affichage des détails d'une place (exemple) – adapte selon tes besoins
  if (document.getElementById("place-name")) {
    document.getElementById("place-name").textContent = localStorage.getItem("placeName") || "";
    document.getElementById("place-description").textContent = localStorage.getItem("placeDescription") || "";
    document.getElementById("place-image").src = localStorage.getItem("placeImage") || "";
  }
});

// Fonction pour afficher les détails d'un lieu
function viewDetails(placeId) {
  // Vérifie que l'utilisateur est authentifié
  const cookies = document.cookie.split(';');
  let token = null;
  cookies.forEach(cookie => {
    const [key, value] = cookie.trim().split('=');
    if (key === 'token') {
      token = value;
    }
  });
  if (!token) {
    window.location.href = 'login.html';
    return;
  }

  // Dictionnaires d'exemple pour les détails du lieu
  const placeNames = {
    "1": "Beach House",
    "2": "Cozy Cabin",
    "3": "City Apartment"
  };
  const descriptions = {
    "1": "Beautiful house by the sea, perfect for a summer getaway.",
    "2": "Escape to the woods in this cozy and peaceful cabin.",
    "3": "Modern apartment in the heart of the city, close to everything."
  };
  const images = {
    "1": "https://source.unsplash.com/800x500/?house,beach",
    "2": "https://source.unsplash.com/800x500/?cabin,forest",
    "3": "https://source.unsplash.com/800x500/?apartment,city"
  };

  localStorage.setItem("placeName", placeNames[placeId]);
  localStorage.setItem("placeDescription", descriptions[placeId]);
  localStorage.setItem("placeImage", images[placeId]);

  window.location.href = "place.html";
}
