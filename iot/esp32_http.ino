#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "Your_WiFi_SSID";
const char* password = "Your_WiFi_Password";
const char* serverUrl = "http://192.168.1.100:5000/send_alert";  // Change to your Python server's IP

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi!");
}

void loop() {
  HTTPClient http;
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");

  String jsonPayload = "{\"message\": \"Patient needs medication reminder!\"}";
  int httpResponseCode = http.POST(jsonPayload);

  Serial.println("Response Code: " + String(httpResponseCode));
  http.end();
  delay(4800000);  // Send alert every 8 hours
}
