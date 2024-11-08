// Sample cart data - In a real app, this would come from a backend
let cartItems = [
  {
    id: 1,
    name: "Organic Bananas",
    price: 2.99,
    quantity: 2,
    image:
      "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3",
  },
  {
    id: 2,
    name: "Fresh Milk",
    price: 3.49,
    quantity: 1,
    image:
      "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3",
  },
];

// Initialize cart
function initCart() {
  renderCart();
  updateSummary();
}

// Render cart items
function renderCart() {
  const cartContainer = document.getElementById("cartItems");

  if (cartItems.length === 0) {
    cartContainer.innerHTML = `
            <div class="empty-cart">
                <i data-lucide="shopping-bag"></i>
                <p>Your cart is empty</p>
                <a href="/dashboard.html" class="checkout-button">Start Shopping</a>
            </div>
        `;
    lucide.createIcons();
    return;
  }

  cartContainer.innerHTML = cartItems
    .map(
      (item) => `
        <div class="cart-item" data-id="${item.id}">
            <img src="${item.image}" alt="${item.name}" class="item-image">
            <div class="item-details">
                <h3 class="item-name">${item.name}</h3>
                <p class="item-price">$${item.price.toFixed(2)}</p>
            </div>
            <div class="item-controls">
                <div class="quantity-controls">
                    <button class="quantity-btn" onclick="updateQuantity(${
                      item.id
                    }, -1)">
                        <i data-lucide="minus"></i>
                    </button>
                    <span class="quantity">${item.quantity}</span>
                    <button class="quantity-btn" onclick="updateQuantity(${
                      item.id
                    }, 1)">
                        <i data-lucide="plus"></i>
                    </button>
                </div>
                <button class="remove-btn" onclick="removeItem(${item.id})">
                    <i data-lucide="trash-2"></i>
                </button>
            </div>
        </div>
    `
    )
    .join("");

  lucide.createIcons();
}

// Update item quantity
function updateQuantity(itemId, change) {
  const item = cartItems.find((item) => item.id === itemId);
  if (item) {
    item.quantity = Math.max(0, item.quantity + change);
    if (item.quantity === 0) {
      removeItem(itemId);
    } else {
      renderCart();
      updateSummary();
    }
  }
}

// Remove item from cart
function removeItem(itemId) {
  cartItems = cartItems.filter((item) => item.id !== itemId);
  renderCart();
  updateSummary();
}

// Update order summary
function updateSummary() {
  const subtotal = cartItems.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );
  const tax = subtotal * 0.1;
  const total = subtotal + tax;

  document.getElementById("subtotal").textContent = `$${subtotal.toFixed(2)}`;
  document.getElementById("tax").textContent = `$${tax.toFixed(2)}`;
  document.getElementById("total").textContent = `$${total.toFixed(2)}`;
}

// Handle checkout
function handleCheckout() {
  if (cartItems.length === 0) {
    alert("Your cart is empty!");
    return;
  }
  // In a real app, this would redirect to a checkout page or process
  alert("Proceeding to checkout...");
}

// Handle logout
function handleLogout() {
  // In a real app, this would handle proper logout
  window.location.href = "/login.html";
}

// Initialize cart when page loads
document.addEventListener("DOMContentLoaded", initCart);
