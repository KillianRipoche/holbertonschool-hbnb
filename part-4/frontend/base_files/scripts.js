document.addEventListener('DOMContentLoaded', () => {
  const placesList = document.getElementById('places-list');
  const priceFilter = document.getElementById('price-filter');

  const places = [
    { name: 'Cozy Cottage', price: 120 },
    { name: 'Urban Loft', price: 200 },
    { name: 'Mountain Cabin', price: 95 },
    { name: 'Cheap Tent', price: 45 },
    { name: 'Luxury Villa', price: 280 }
  ];

  function renderPlaces(maxPrice = null) {
    placesList.innerHTML = '';

    const filteredPlaces = places.filter(place => {
      return maxPrice === null || place.price <= maxPrice;
    });

    filteredPlaces.forEach(place => {
      const card = document.createElement('article');
      card.className = 'place-card';

      card.innerHTML = `
        <h3>${place.name}</h3>
        <p>$${place.price} per night</p>
        <a href="place.html" class="details-link">
          <button class="details-button">View Details</button>
        </a>
      `;

      placesList.appendChild(card);
    });
  }

  // Initial rendering of all places
  renderPlaces();

  // Event listener for filter changes
  if (priceFilter) {
    priceFilter.addEventListener('change', () => {
      const selectedValue = priceFilter.value;
      const max = selectedValue === '300' ? null : parseInt(selectedValue);
      renderPlaces(max);
    });
  }
});
