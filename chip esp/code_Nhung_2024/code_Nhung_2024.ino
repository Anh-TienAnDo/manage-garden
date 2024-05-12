
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Wire.h>
#include <DHT.h>

#define SCREEN_WIDTH 128 // Chiều rộng của màn hình OLED
#define SCREEN_HEIGHT 64 // Chiều cao của màn hình OLED
// Địa chỉ I2C của màn hình OLED
#define OLED_ADDR 0x3C
// Khởi tạo đối tượng cho màn hình OLED
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_ADDR);
// Khai báo chân kết nối với cảm biến DHT11
#define DHTPIN 2
// Khai báo loại cảm biến DHT
#define DHTTYPE DHT11
// Khởi tạo đối tượng cho cảm biến DHT
DHT dht(DHTPIN, DHTTYPE);
// Khai báo chân kết nối với cảm biến ánh sáng
#define LIGHT_SENSOR A0

#define LED 15
// led
#define FAN 0
// quat

// wifi
const char *ssid = "Xiaomi_9172";    // Tên WiFi của bạn
const char *password = "12341234";  // Mật khẩu WiFi của bạn
//MQTT Broker
const char *mqtt_server = "broker.emqx.io";
const char *topic = "mcu8266/tmp";   // Topic để gửi dữ liệu nhiệt độ và độ ẩm
const char *topic2 = "esp8266/led";  // Topic để điều khiển LED
const char *topic3 = "esp8266/fan";  // Topic để điều khiển quat
const char *mqtt_username = "emqx";
const char *mqtt_password = "12345678";
const int mqtt_port = 1883;
bool ledState = false;
bool fanState = false;
WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  setup_wifi();
  // Khai báo pin LED là output
  pinMode(LED, OUTPUT);
  pinMode(FAN, OUTPUT);
  digitalWrite(LED, LOW);  // Tắt LED ban đầu
  digitalWrite(FAN, LOW);
  // Kết nối tới MQTT broker
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  while (!client.connected()) {
    String client_id = "esp8266-client-";
    client_id += String(WiFi.macAddress());
    Serial.printf("Client %s đang kết nối tới MQTT broker\n", client_id.c_str());
    if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
      Serial.println("Đã kết nối tới MQTT broker");
    } else {
      Serial.print("Kết nối thất bại, mã lỗi: ");
      Serial.print(client.state());
      delay(2000);
    }
  }
  dht.begin();
  client.publish(topic2, "hello emqx");
  client.subscribe(topic2);
  client.subscribe(topic3);

  // Khởi động giao tiếp I2C
  Wire.begin();
  // Khởi động màn hình OLED
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;);
  }
  // Khởi động cảm biến DHT
  dht.begin();
  // Hiển thị một vài văn bản mặc định
  display.display();
  delay(2000);
}

void setup_wifi(){
  delay(10);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Đã kết nối với mạng WiFi");
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Đang thử kết nối MQTT...");
    if (client.connect("nodeMcuDHT11")) {
      Serial.println("Đã kết nối");
    } else {
      Serial.print("Kết nối thất bại, mã lỗi: ");
      Serial.print(client.state());
      Serial.println(" Thử lại sau 2 giây");
      delay(2000);
    }
  }
}

void callback(char* topic, byte *payload, unsigned int length) {
  Serial.print("Nhận tin nhắn từ topic: ");
  Serial.println(topic);
  Serial.print("Nội dung: ");
  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  Serial.print(message);
  if (message == "on" && !ledState) {
    digitalWrite(LED, HIGH);
    ledState = true;
  }
  if (strcmp(topic, topic2) == 0) {
    if (message == "on") {
      digitalWrite(LED, HIGH);  // Bật đèn LED 1
      Serial.println("den 1 bat");
    } else {
digitalWrite(LED, LOW);  // Tắt đèn LED 1
      Serial.println("den 1 tat");
    }
  }else if (strcmp(topic, topic3) == 0) {
    if (message == "on") {

      digitalWrite(FAN, HIGH);  // Bật đèn LED 2
      Serial.println("den 2 bat");
      
    } else {
      digitalWrite(FAN, LOW);  // Tắt đèn LED 2
      Serial.println("den 2 tat");
    }
  }
}

void loop() {
  if(!client.connected()){
    reconnect();
  }
  client.loop();
  // Đọc dữ liệu từ cảm biến DHT
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  // Đọc dữ liệu từ cảm biến ánh sáng
  int lightValue = analogRead(LIGHT_SENSOR);
  // Chuyển đổi giá trị analog thành giá trị ánh sáng
  float lightLevel = map(lightValue, 0, 1023, 0, 100); // Chuyển từ 0-1023 sang 0-100
  // Xóa màn hình
  display.clearDisplay();
  // Hiển thị dữ liệu nhiệt độ và độ ẩm
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 10);
  display.print("Temperature: ");
  display.println(temperature);
  display.print("Humidity: ");
  display.println(humidity);
  // Hiển thị dữ liệu ánh sáng
  display.print("Light: ");
  display.print(lightLevel);
  display.println("%");
  // Hiển thị trên màn hình
  display.display();
  // Đợi một khoảng thời gian trước khi vẽ lại màn hình

  // Tạo đối tượng JSON
  DynamicJsonDocument jsonDoc(200);
  // jsonDoc["id_manh_dat"] = "ID_001";
  jsonDoc["temperature"] = temperature;
  jsonDoc["humidity"] = humidity;
  jsonDoc["light"] = lightValue;
  // Tạo chuỗi JSON
  String payload;
  serializeJson(jsonDoc, payload);
  // Chuyển chuỗi payload sang mảng char để publish
  char charPayload[payload.length() + 1];
  payload.toCharArray(charPayload, payload.length() + 1);
  // Publish dữ liệu lên topic "topic"
  client.publish(topic, charPayload);

  delay(1000);
}
