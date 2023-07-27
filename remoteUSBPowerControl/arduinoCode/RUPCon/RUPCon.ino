// Define os pinos da USB
const int USBPins[] = {2, 3, 4, 5, 6, 7, 8};
const int numUSBs = sizeof(USBPins) / sizeof(USBPins[0]);

void setup() {
  Serial.begin(9600);

  // Configura os pinos dos USBs como saída
  for (int i = 0; i < numUSBs; i++) {
    pinMode(USBPins[i], OUTPUT);
    digitalWrite(USBPins[i], LOW); // Desliga todos os USBs no início
  }
}

void loop() {
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n'); // Lê o comando até encontrar uma quebra de linha
    int USBIndex = -1;
    
    // Verifica se o comando começa com "on_" ou "off_"
    if (comando.startsWith("on_")) {
      USBIndex = comando.substring(3).toInt(); // Obtém o número após "on_"
      if (USBIndex >= 0 && USBIndex < numUSBs) {
        digitalWrite(USBPins[USBIndex], HIGH); // Liga a USB
        Serial.println("Porta USB " + String(USBIndex) + " ligada.");
      } else {
        Serial.println("Porta USB inválida.");
      }
    } else if (comando.startsWith("off_")) {
      USBIndex = comando.substring(4).toInt(); // Obtém o número após "off_"
      if (USBIndex >= 0 && USBIndex < numUSBs) {
        digitalWrite(USBPins[USBIndex], LOW); // Desliga a USB
        Serial.println("Porta USB " + String(USBIndex) + " desligada.");
      } else {
        Serial.println("Porta USB inválida.");
      }
    } else {
      Serial.println("Comando inválido.");
    }
  }
}
