#include <WiFi.h>
#include <HTTPClient.h>
#include <LiquidCrystal.h>

// Replace with your actual WiFi credentials
#define WIFI_SSID "your_SSID"
#define WIFI_PASSWORD "your_PASSWORD"

// Replace with the actual API endpoints
#define CART_ENDPOINT "http://example.com/cart_sync"
#define PRODUCT_ENDPOINT "http://example.com/product_add"

// Set up the LCD pins (adjust pins as necessary)
LiquidCrystal lcd(12, 11, 5, 4, 3, 2); // Adjust based on your LCD setup

void setup() {
  Serial.begin(9600);            // Begin serial communication
  lcd.begin(16, 2);               // Initialize LCD with 16 columns and 2 rows
  
  lcd.print("Connecting WiFi...");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD); // Connect to WiFi

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  lcd.clear();
  lcd.print("WiFi Connected");
  delay(2000);
  lcd.clear();
}

void loop() {
  if (Serial.available() > 0) {
    String barcodeData = Serial.readStringUntil('\n'); // Read barcode data from scanner
    barcodeData.trim(); // Remove any extra whitespace
    
    if (barcodeData.startsWith("CART")) {
      // Send data to the CART endpoint if it starts with "CART"
      if (sendData(CART_ENDPOINT, barcodeData)) {
        lcd.clear();
        lcd.print("Cart Sync Successful");
      } else {
        lcd.clear();
        lcd.print("Cart Sync Failed");
      }
    } else {
      // Send data to the PRODUCT endpoint for other cases
      if (sendData(PRODUCT_ENDPOINT, barcodeData)) {
        lcd.clear();
        lcd.print("Product Added");
      } else {
        lcd.clear();
        lcd.print("Add Product Failed");
      }
    }
    delay(2000); // Wait 2 seconds before the next read
  }
}

bool sendData(const char* endpoint, String data) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(endpoint);                     // Initialize HTTP connection to the endpoint
    http.addHeader("Content-Type", "application/json"); // Set the content type to JSON

    String payload = "{\"code\":\"" + data + "\"}"; // Create JSON payload
    int httpResponseCode = http.POST(payload); // Send POST request and get the response code

    http.end(); // Close HTTP connection

    return (httpResponseCode == 200); // Return true if request was successful
  } else {
    Serial.println("WiFi Disconnected");
    return false;
  }
}
