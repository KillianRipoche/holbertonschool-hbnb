document.addEventListener('DOMContentLoaded', () => {
  const placesList = document.getElementById('places-list');
  const priceFilter = document.getElementById('price-filter');

  // Liste des lieux avec leur prix
  const places = [
    { name: 'Cozy Cottage', price: 120 },
    { name: 'Urban Loft', price: 200 },
    { name: 'Mountain Cabin', price: 95 },
    { name: 'Cheap Tent', price: 45 },
    { name: 'Luxury Villa', price: 280 }
  ];

  // Fonction pour afficher les lieux en fonction du filtre
  const displayPlaces = (maxPrice) => {
    placesList.innerHTML = '';
    const filteredPlaces = places.filter(place => place.price <= maxPrice);

    filteredPlaces.forEach(place => {
      const card = document.createElement('div');
      card.className = 'place-card';

      card.innerHTML = `
        <h3>${place.name}</h3>
        <p>$${place.price} per night</p>
        <button class="btn" onclick="location.href='place.html'">View Details</button>
      `;

      placesList.appendChild(card);
    });
  };

  priceFilter.addEventListener('change', (e) => {
    const maxPrice = parseInt(e.target.value, 10);
    displayPlaces(maxPrice);
  });

  // Affichage initial avec un maxPrice élevé pour afficher toutes les places
  displayPlaces(300);
});
