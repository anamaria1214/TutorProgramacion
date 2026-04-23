# Ejemplos para Probar el Tutor de Programación

## EJEMPLO 1: EXPLICACIÓN DE CONCEPTO (Python)
**Pregunta del estudiante:**
```
¿Qué es una variable en Python?
```

**Respuesta esperada:**
- Analogía sencilla
- Definición técnica
- Pequeño ejemplo de código

---

## EJEMPLO 2: CÓDIGO CON PRUEBA DE ESCRITORIO (Python)
**Pregunta del estudiante:**
```
Hazme un código en Python que sume los números del 1 al 5
```

**Respuesta esperada:**

### Explicación:
El código recorre números del 1 al 5 y va acumulándolos en una variable. Al final, muestra la suma total.

### Código:
```python
suma = 0  # Inicializamos la variable donde guardaremos el total
for i in range(1, 6):  # i va de 1 a 5
    suma = suma + i  # Sumamos el valor actual de i a suma
print(suma)  # Mostramos el resultado
```

### Prueba de Escritorio:
```
Ejecución con entrada: n=5

Línea 1: suma = 0 → suma: 0
Línea 2: i = 1 (primera iteración)
Línea 3: suma = 0 + 1 → suma: 1
Línea 2: i = 2 (segunda iteración)
Línea 3: suma = 1 + 2 → suma: 3
Línea 2: i = 3
Línea 3: suma = 3 + 3 → suma: 6
Línea 2: i = 4
Línea 3: suma = 6 + 4 → suma: 10
Línea 2: i = 5 (última iteración)
Línea 3: suma = 10 + 5 → suma: 15
Línea 2: Fin del bucle
Línea 4: print(suma)

Output: 15
```

---

## EJEMPLO 3: CÓDIGO CON PRUEBA DE ESCRITORIO (Java)
**Pregunta del estudiante:**
```
Cómo hago en Java un programa que multiplique dos números que pida al usuario?
```

**Respuesta esperada:**

### Explicación:
El programa pide al usuario dos números, los multiplica y muestra el resultado.

### Código:
```java
import java.util.Scanner;

public class Multiplicacion {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        
        System.out.print("Ingresa el primer número: ");
        int num1 = sc.nextInt();
        
        System.out.print("Ingresa el segundo número: ");
        int num2 = sc.nextInt();
        
        int resultado = num1 * num2;  // Multiplicamos
        System.out.println("Resultado: " + resultado);
    }
}
```

### Prueba de Escritorio (con entrada: 4 y 7):
```
Ejecución:

Línea 1: Scanner sc = new Scanner(System.in)
Línea 3: print("Ingresa el primer número: ")
Usuario ingresa: 4
Línea 4: num1 = 4 → num1: 4

Línea 6: print("Ingresa el segundo número: ")
Usuario ingresa: 7
Línea 7: num2 = 7 → num2: 7

Línea 9: resultado = 4 * 7 → resultado: 28
Línea 10: print("Resultado: 28")

Output: Resultado: 28
```

---

## EJEMPLO 4: CONCEPTO EN GO
**Pregunta del estudiante:**
```
Explica qué son los slices en Go y cómo se diferencias de los arrays
```

**Respuesta esperada:**
- Analogía clara (arrays = lista fija, slices = lista flexible)
- Definición técnica breve
- Pequeño ejemplo de código

---

## EJEMPLO 5: CÓDIGO CON BUCLE ANIDADO (Python)
**Pregunta del estudiante:**
```
Hazme un código que imprima una tabla de multiplicar del 1 al 3 por 1 al 3
```

**Respuesta esperada:**

### Código:
```python
for i in range(1, 4):  # Filas: 1, 2, 3
    for j in range(1, 4):  # Columnas: 1, 2, 3
        resultado = i * j
        print(f"{resultado}", end=" ")  # Sin salto de línea
    print()  # Salto de línea al fin de cada fila
```

### Prueba de Escritorio:
```
Ejecución con entrada: rango(1, 4) - números 1, 2, 3

Línea 1: i = 1 (primera iteración del bucle externo)
Línea 2: j = 1 (primera iteración del bucle interno)
Línea 3: resultado = 1 * 1 = 1 → resultado: 1
Línea 4: print(1) → Salida: "1 "

Línea 2: j = 2 (segunda iteración del bucle interno)
Línea 3: resultado = 1 * 2 = 2 → resultado: 2
Línea 4: print(2) → Salida: "1 2 "

Línea 2: j = 3 (tercera iteración del bucle interno)
Línea 3: resultado = 1 * 3 = 3 → resultado: 3
Línea 4: print(3) → Salida: "1 2 3 "

Línea 5: print() → Salto de línea

... (i = 2 sigue el mismo patrón) ...

Línea 1: i = 3 (tercera iteración del bucle externo)
Línea 2: j = 1
Línea 3: resultado = 3 * 1 = 3 → resultado: 3
Línea 4: print(3) → Salida: "3 "
... (continúa hasta j=3: 3*3=9)

Output:
1 2 3
1 2 3
1 2 3
```

---

## CÓMO PROBAR

### Opción 1: Terminal (modo interactivo)
```bash
python script.py
```
Luego escribe las preguntas una por una.

### Opción 2: Streamlit (interfaz visual)
```bash
streamlit run app.py
```
Abre http://localhost:8501 en el navegador.

---

## Preguntas Sugeridas para Probar

### Python:
1. "¿Qué es una función?"
2. "Hazme código que cuente números pares del 1 al 10"
3. "¿Cuál es la diferencia entre listas y tuplas?"

### Java:
1. "¿Qué es una clase?"
2. "Código que calcule el factorial de 5"
3. "Explica qué son los bucles for"

### Go:
1. "¿Qué es una goroutine?"
2. "Hazme un programa que imprima números del 1 al 5"

### General:
1. "¿Cómo se resuelve un problema de programación?"
2. "¿Qué es algoritmo?"
