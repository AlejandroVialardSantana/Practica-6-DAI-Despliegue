document.addEventListener('DOMContentLoaded', function() {
    initializeRatingsUI();
});

function initializeRatingsUI() {
    let userId = getCurrentUserId();
    let userRatings = getUserRatings(userId);

    document.querySelectorAll('.star-rating').forEach(starRatingElement => {
        let productId = starRatingElement.getAttribute('data-product-id');
        if (userRatings[productId]) {
            let ratingValue = userRatings[productId];
            updateStarsUI(starRatingElement, ratingValue);
        }
    });
}

function getUserRatings(userId) {
    let allRatings = JSON.parse(localStorage.getItem('ratingsByUser') || '{}');
    return allRatings[userId] || {};
}

function updateStarsUI(starRatingEl, rating) {
    let stars = starRatingEl.querySelectorAll('.bi-star-fill');
    stars.forEach((star, index) => {
        if (index < rating) {
            star.classList.add('checked');
        } else {
            star.classList.remove('checked');
        }
    });
}

function rateProduct(star) {
    const isAuthenticated = star.parentNode.getAttribute('data-is-authenticated') === 'True';
    const productId = star.parentNode.getAttribute('data-product-id');

    if (!isAuthenticated) {
        alert('You need to log in to rate products.');
        return;
    }

    if (hasUserAlreadyRated(productId)) {
        alert('You have already rated this product.');
        return;
    }

    const rating = star.getAttribute('data-value');
    console.log('Rating for product', productId, 'is', rating);

    let siblings = star.parentNode.querySelectorAll('.bi-star-fill');
    siblings.forEach(sib => {
        sib.classList.remove('checked');
    });

    for (let i = 0; i < rating; i++) {
        siblings[i].classList.add('checked');
    }

    sendRatingToServer(productId, rating);

    setUserRated(productId, rating);
}

function sendRatingToServer(productId, newRating) {
    newRating = Number(newRating);

    const currentRateElement = document.getElementById(`rate-average-${productId}`);
    const currentCountElement = document.getElementById(`rate-count-${productId}`);
    let currentRate = Number(currentRateElement.textContent);
    let currentCount = Number(currentCountElement.textContent);

    let newRate = ((currentRate * currentCount) + newRating) / (currentCount + 1);
    let newCount = currentCount + 1;

    const requestBody = {
        rating: {
            rate: newRate,
            count: newCount
        }
    };

    fetch(`/api/products/${productId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer testtoken`
        },
        body: JSON.stringify(requestBody)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if(data.ok === "yes") {
            console.log('New rating saved successfully');
            currentRateElement.textContent = newRate.toFixed(1);
            currentCountElement.textContent = newCount;
        } else {
            console.error('Error from API:', data.error);
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
    });
}

function hasUserAlreadyRated(productId) {
    let userId = getCurrentUserId();
    let userRatings = getUserRatings(userId);
    return userRatings.hasOwnProperty(productId);
}

function setUserRated(productId, rating) {
    let userId = getCurrentUserId();
    let allRatings = JSON.parse(localStorage.getItem('ratingsByUser') || '{}');

    if (!allRatings[userId]) {
        allRatings[userId] = {};
    }

    allRatings[userId][productId] = rating;
    localStorage.setItem('ratingsByUser', JSON.stringify(allRatings));
}

function clearUserRatingsOnLogout() {
    let userId = getCurrentUserId();
    let allRatings = JSON.parse(localStorage.getItem('ratingsByUser') || '{}');

    delete allRatings[userId];
    localStorage.setItem('ratingsByUser', JSON.stringify(allRatings));
}

function getCurrentUserId() {
    let starRatingElement = document.querySelector('.star-rating');
    return starRatingElement ? starRatingElement.getAttribute('data-user-id') : null;
}
