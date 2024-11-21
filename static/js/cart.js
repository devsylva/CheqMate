function removeFromCart(cartId, productId) {
  fetch("cart/remove-item/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCsrfToken(), // Fetch CSRF token
    },
    body: JSON.stringify({ cart_id: cartId, product_id: productId }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to remove product from cart");
      }
      return response.json();
    })
    .then((data) => {
      if (data.message) {
        alert(data.message); // Notify the user
        updateCartUI(cartId); // Refresh the cart UI after successful removal
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Could not remove product from cart. Please try again.");
    });
}

// Function to fetch updated cart data and refresh the UI
function updateCartUI(cartId) {
  fetch(`/cart/${cartId}/`) // Adjust endpoint to return cart details
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to fetch cart data");
      }
      return response.json();
    })
    .then((cartData) => {
      const cartItems = document.getElementById("cartItems");
      cartItems.innerHTML = ""; // Clear current items

      if (cartData.items.length === 0) {
        cartItems.innerHTML = "<p>Your cart is empty.</p>";
      } else {
        cartData.items.forEach((item) => {
          const itemElement = document.createElement("div");
          itemElement.className = "cart-item";
          itemElement.innerHTML = `
            <span>${item.product_name}</span>
            <span>#${item.price}</span>
            <button onclick="removeFromCart('${cartData.id}', '${item.product_id}')">Remove</button>
          `;
          cartItems.appendChild(itemElement);
        });
      }

      // Update totals
      document.querySelector(
        ".cart-summary .summary-row.total span:last-child"
      ).textContent = `$${cartData.total_price}`;
    })
    .catch((error) => console.error("Error fetching cart data:", error));
}

// Helper function to get the CSRF token
function getCsrfToken() {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, "csrftoken".length + 1) === "csrftoken=") {
        cookieValue = decodeURIComponent(
          cookie.substring("csrftoken".length + 1)
        );
        break;
      }
    }
  }
  return cookieValue;
}
