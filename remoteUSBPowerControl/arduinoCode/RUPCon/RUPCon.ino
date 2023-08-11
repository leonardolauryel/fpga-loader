// Set USB pins
const int USBPins[] = {2, 3, 4, 5, 6, 7, 8};
const int numUSBs = sizeof(USBPins) / sizeof(USBPins[0]);

void setup() {
  Serial.begin(9600);

  // Configure USB pins as output
  for (int i = 0; i < numUSBs; i++) {
    pinMode(USBPins[i], OUTPUT);
    digitalWrite(USBPins[i], HIGH); // Turn Off all USBs at startup
  }
}

boolean isValidUSBPort(int USBPort) {
  return USBPort >= 0 && USBPort < numUSBs;
}

void turnOnAllUSBPorts() {
  for (int i = 0; i < numUSBs; i++) {
    digitalWrite(USBPins[i], LOW);
  }

  Serial.println("Todas as portas USB foram ligadas");
}

void turnOffAllUSBPorts() {
  for (int i = 0; i < numUSBs; i++) {
    digitalWrite(USBPins[i], HIGH);
  }

  Serial.println("Todas as portas USB foram desligadas");
}

void turnOnUSBPort(int USBPort) {
  if (isValidUSBPort(USBPort)) {
    digitalWrite(USBPins[USBPort], LOW); // Turn on USB
    Serial.println("Porta USB " + String(USBPort) + " ligada.");
  } else {
    Serial.println("Porta USB inválida.");
  }
}

void turnOffUSBPort(int USBPort) {
  if (isValidUSBPort(USBPort)) {
    digitalWrite(USBPins[USBPort], HIGH); // Turn off USB
    Serial.println("Porta USB " + String(USBPort) + " desligada.");
  } else {
    Serial.println("Porta USB inválida.");
  }
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Read the command until it finds a line break
    int USBPort = -1;
    
    // Check if the command starts with "on_" or "off_"
    if (command.startsWith("on_")) {
      if (command == "on_all") {
        turnOnAllUSBPorts();
      } else {
        USBPort = command.substring(3).toInt(); // Get the number after "on_"
        turnOnUSBPort(USBPort);
      }
    } else if (command.startsWith("off_")) {
      if (command == "off_all") {
        turnOffAllUSBPorts();
      } else {
        USBPort = command.substring(4).toInt(); // Get the number after "off_"
        turnOffUSBPort(USBPort);
      }
    } else {
      Serial.println("Comando inválido.");
    }
  }
}
