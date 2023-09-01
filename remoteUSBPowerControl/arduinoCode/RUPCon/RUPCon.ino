// Seta os pinos das portas de fornecimento de energia
const int powerSupplyPins[] = {2, 3, 4, 5, 6, 7, 8};
const int numPowerSuppliers = sizeof(powerSupplyPins) / sizeof(powerSupplyPins[0]);

void setup() {
  Serial.begin(9600);

  // Configura os pinos das portas de fornecimento de energia como OUTPUT
  for (int i = 0; i < numPowerSuppliers; i++) {
    pinMode(powerSupplyPins[i], OUTPUT);
    digitalWrite(powerSupplyPins[i], HIGH); // Desliga todas as portas de fornecimento de energia ao iniciar
  }
}

boolean isValidPowerSupplyPort(int powerSupplyPort) {
  return powerSupplyPort >= 0 && powerSupplyPort < numPowerSuppliers;
}

void turnOnAllPowerSuppliersPorts() {
  for (int i = 0; i < numPowerSuppliers; i++) {
    digitalWrite(powerSupplyPins[i], LOW);
  }

  Serial.println("Todas as portas de fornecimento de energia foram ligadas");
}

void turnOffAllPowerSuppliersPorts() {
  for (int i = 0; i < numPowerSuppliers; i++) {
    digitalWrite(powerSupplyPins[i], HIGH);
  }

  Serial.println("Todas as portas de fornecimento de energia foram desligadas");
}

void turnOnPowerSupplyPort(int powerSupplyPort) {
  if (isValidPowerSupplyPort(powerSupplyPort)) {
    digitalWrite(powerSupplyPins[powerSupplyPort], LOW); // Turn on de fornecimento de energia
    Serial.println("Porta de fornecimento de energia " + String(powerSupplyPort) + " ligada.");
  } else {
    Serial.println("Porta de fornecimento de energia inválida.");
  }
}

void turnOffPowerSupplyPort(int powerSupplyPort) {
  if (isValidPowerSupplyPort(powerSupplyPort)) {
    digitalWrite(powerSupplyPins[powerSupplyPort], HIGH); // Turn off de fornecimento de energia
    Serial.println("Porta de fornecimento de energia " + String(powerSupplyPort) + " desligada.");
  } else {
    Serial.println("Porta de fornecimento de energia inválida.");
  }
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Read the command until it finds a line break
    int powerSupplyPort = -1;
    
    // Check if the command starts with "on_" or "off_"
    if (command.startsWith("on_")) {
      if (command == "on_all") {
        turnOnAllPowerSuppliersPorts();
      } else {
        powerSupplyPort = command.substring(3).toInt(); // Get the number after "on_"
        turnOnPowerSupplyPort(powerSupplyPort);
      }
    } else if (command.startsWith("off_")) {
      if (command == "off_all") {
        turnOffAllPowerSuppliersPorts();
      } else {
        powerSupplyPort = command.substring(4).toInt(); // Get the number after "off_"
        turnOffPowerSupplyPort(powerSupplyPort);
      }
    } else {
      Serial.println("Comando inválido.");
    }
  }
}
