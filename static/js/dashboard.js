// Sample recent activity data
const recentActivities = [
  { id: 1, name: "Organic Bananas", date: "2 hours ago", price: "$2.99" },
  { id: 2, name: "Fresh Milk", date: "3 hours ago", price: "$3.49" },
  { id: 3, name: "Whole Grain Bread", date: "Yesterday", price: "$4.99" },
];

// Initialize dashboard
function initDashboard() {
  renderRecentActivity();
}

// Render recent activity
function renderRecentActivity() {
  const activityList = document.getElementById("activityList");

  activityList.innerHTML = recentActivities
    .map(
      (activity) => `
        <div class="activity-item">
            <div class="activity-info">
                <div class="activity-dot"></div>
                <div class="activity-details">
                    <h4>${activity.name}</h4>
                    <p>${activity.date}</p>
                </div>
            </div>
            <span class="activity-price">${activity.price}</span>
        </div>
    `
    )
    .join("");
}

// Function to get the CSRF token from the cookie
function getCSRFToken() {
    let cookieValue = null;
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            cookieValue = decodeURIComponent(value);
            break;
        }
    }
    return cookieValue;
}

// Fetch and display QR code from backend endpoint
async function generateQRCode(data) {
  try {
    // Replace with your custom endpoint URL
    const response = await fetch("http://localhost:8000/api/startshopping/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(), // Add the CSRF token to the headers
      },
      body: JSON.stringify({ data: data }),
    });

    if (!response.ok) {
      throw new Error("Failed to fetch QR code");
    }

    const result = await response.json();
    const qrCodeURL = result.qrCodeURL;

    // Insert QR code image in modal
    document.getElementById(
      "qrAnimation"
    ).innerHTML = `<img src="${qrCodeURL}" alt="QR Code">`;

    // Show modal
    document.getElementById("qrModal").classList.remove("hidden");
    setTimeout(
      () => document.getElementById("qrModal").classList.add("visible"),
      10
    );
  } catch (error) {
    console.error("Error generating QR code:", error);
  }
}

// Handle start shopping
async function startShopping() {
  const modal = document.getElementById("qrModal");
  const qrAnimation = document.getElementById("qrAnimation");
  const qrStatus = document.getElementById("qrStatus");
  const qrMessage = document.getElementById("qrMessage");

  // Show the modal
  modal.classList.remove("hidden");
  setTimeout(() => modal.classList.add("visible"), 10);

  try {
    // Fetch the image from the endpoint
    const response = await fetch("http://localhost:8000/api/startshopping/", {
      method: "POST",
      headers: {
        "X-CSRFToken": getCSRFToken(), // Add the CSRF token
      },
    });

    if (response.ok) {
      // Convert the image to a URL for display
      const blob = await response.blob();
      const qrImageUrl = URL.createObjectURL(blob);

      // Display the image in the modal
      qrAnimation.innerHTML = `<img src="${qrImageUrl}" alt="QR Code" style="width: 150px; height: auto;" />`;
      qrStatus.textContent = "Your Shopping QR Code";
      qrMessage.textContent = "Scan this code to start your shopping session";
    } else {
      throw new Error("Failed to load QR code.");
    }
  } catch (error) {
    console.error("Error:", error);
    qrStatus.textContent = "Error";
    qrMessage.textContent = "Unable to load QR code. Please try again.";
  }
}


// Handle cancel shopping
function cancelShopping() {
  const modal = document.getElementById("qrModal");
  const qrAnimation = document.getElementById("qrAnimation");
  const qrStatus = document.getElementById("qrStatus");
  const qrMessage = document.getElementById("qrMessage");

  modal.classList.remove("visible");
  setTimeout(() => {
    modal.classList.add("hidden");
    qrAnimation.innerHTML = ""; // Clear QR code image
    qrStatus.textContent = "Your Shopping QR Code";
    qrMessage.textContent = "Scan this code to start your shopping session";
  }, 300);
}


// Initialize dashboard when page loads
document.addEventListener("DOMContentLoaded", initDashboard);
