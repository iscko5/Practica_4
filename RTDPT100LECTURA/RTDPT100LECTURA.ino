/*
  2016-FEB-09
  Aplicacion para la lectura de una señal de corriente 4 - 20 mA
  sobre una resistencia de 250 Ohm en la entrada analoga de voltaje
  esto proporcionara lecturas de voltaje de 1 a 5 voltios.
  
  Esta lectura de corriente representa a su vez una temperatura de -50 a +150 C
  que proviene de un RTD PT100 conectada a un transmisor de corriente 4-20 mA
  
  corriente    voltaje(250 Ohm)     ADC    Temperatura
  -----------------------------------------------------
  4  mA        1 V                  205    -50  C
  20 mA        5 V                  1023   +150 C

 La temperatura obtenida despues de los calculos sera enviada en formato ASCII por el puerto serial
 cada vez que se reciba un byte por dicho puerto. (Envio por demanda)

 Automatizanos.com
 
 */

const int EntradaAnaloga = A0;  // Entrada analoga donde estara la resistencia de conversion de corriente a voltaje


int   sensorValor = 0;        
int   temperatura = 0;
int   ByteRecibido = 0;
float f1 = 0;
float t1 = 0;



void setup() {
  // inicializa comunicacion serial a 9600 bps:
  Serial.begin(9600); 
}

void loop() {
  
  // Esperar que se reciba un byte por el puerto serial para enviar la lectura
  // (envio por demanda)
  if(Serial.available() > 0){
     ByteRecibido = Serial.read();
     
     // Obtener la lectura de ADC     
     sensorValor = analogRead(EntradaAnaloga);            
     
     // hacer el mapeo de las señales por cifras multiplicadas por 10 para 
     // obtener decimales, pues la funcion map no recibe numeros flotantes
     temperatura=map(sensorValor,205,1023,-500,1500);

     f1 = temperatura;  // convirtiendo a flotante
     t1 = f1/10.0;      // dividiendo entre 10 ahora se tiene la lectra correcta
                        // con una cifra decimal   

     // Imprimiendo el resultado por el puerto serial
     Serial.print(t1);      
     Serial.print("\n");      
  
  }
  
  
}
