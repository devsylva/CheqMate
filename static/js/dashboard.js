// Flag to track if the function is already running
let isShoppingStarted = false;

// Function to get the CSRF token
function getCSRFToken() {
  let cookieValue = null;
  const cookies = document.cookie.split(";");
  for (let cookie of cookies) {
    const [name, value] = cookie.trim().split("=");
    if (name === "csrftoken") {
      cookieValue = decodeURIComponent(value);
      break;
    }
  }
  return cookieValue;
}

// Function to start the shopping session and handle QR code generation
async function startShopping() {
  // Prevent multiple clicks from triggering the function again
  if (isShoppingStarted) {
    console.log("Shopping session already started.");
    return;
  }
  isShoppingStarted = true; // Set flag to true to block further clicks

  console.log("startShopping function triggered"); // Log when the function is called
  const modal = document.getElementById("qrModal");
  const qrAnimation = document.getElementById("qrAnimation");
  const qrStatus = document.getElementById("qrStatus");
  const qrMessage = document.getElementById("qrMessage");

  // Show the modal
  modal.classList.remove("hidden");
  setTimeout(() => modal.classList.add("visible"), 10);

  try {
    // Step 1: Fetch the QR Code from the startshopping API
    const response = await fetch("http://localhost:8000/api/startshopping/", {
      method: "POST",
      headers: {
        "X-CSRFToken": getCSRFToken(), // Add CSRF token
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      const result = await response.json();
      const qrImageUrl = result.qrCodeURL;
      const cartId = result.qrCode; // Ensure cartId is returned here

      console.log("Cart ID received:", cartId); // Log the cart ID received

      qrAnimation.innerHTML = `<img src="${qrImageUrl}" alt="QR Code" style="width: 150px; height: auto;" />`;
      qrStatus.textContent = "Your Shopping QR Code";
      qrMessage.textContent = "Scan this code to start your shopping session";

      // Step 2: Set up WebSocket connection to listen for cart sync status
      setupWebSocket(cartId); // Pass the correct cartId here
    } else {
      throw new Error("Failed to load QR code.");
    }
  } catch (error) {
    console.error("Error:", error);
    qrStatus.textContent = "Error";
    qrMessage.textContent = "Unable to load QR code. Please try again.";
  } finally {
    // Reset flag after some delay (e.g., after the shopping session is fully started)
    setTimeout(() => {
      isShoppingStarted = false;
    }, 5000); // Adjust timeout as needed
  }
}

// Function to setup WebSocket connection
function setupWebSocket(cartId) {
  console.log("Setting up WebSocket for cartId:", cartId); // Log WebSocket setup
  const socket = new WebSocket(`ws://localhost:8000/ws/cart/${cartId}/`);

  // Handle connection open
  socket.onopen = function () {
    console.log("WebSocket connection established");
  };

  // Listen for messages from the server
  socket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    console.log("Received data:", data); // Log the received data to check its structure
    window.location.href = `/cart/${cartId}/`;
    // if (data.is_synced === true) {
    //   console.log("Cart is synced, redirecting...");
    //   window.location.href = `/cart/${cartId}/`; // Redirect to the cart page
    // } else {
    //   console.log("Cart is not synced yet.");
    // }
  };

  // Handle errors
  socket.onerror = function (error) {
    console.error("WebSocket error:", error);
  };

  // Handle connection close
  socket.onclose = function () {
    console.log("WebSocket connection closed");
  };
}

// Function to cancel the shopping session and close the modal
function cancelShopping() {
  const modal = document.getElementById("qrModal");
  modal.classList.remove("visible");
  setTimeout(() => modal.classList.add("hidden"), 200);
}

// Wait for the DOM to be loaded and then initialize the dashboard
document.addEventListener("DOMContentLoaded", function () {
  const startButton = document.querySelector(".start-button");
  if (startButton) {
    console.log("Adding event listener for start button"); // Log when event listener is added
    startButton.removeEventListener("click", startShopping); // Ensure we don't add multiple listeners
    startButton.addEventListener("click", startShopping);
  }
});
