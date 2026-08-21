---
marp: true
theme: gaia
_class: lead
paginate: true
backgroundColor: #fcfcfc
color: #222222
style: |
  section {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 21px;
    padding: 35px 50px;
  }
  h1 {
    color: #003366;
    font-size: 36px;
  }
  h2 {
    color: #0055a5;
    font-size: 28px;
    border-bottom: 2px solid #0055a5;
    padding-bottom: 8px;
    margin-top: 0;
  }
  h3 {
    color: #222;
    font-size: 22px;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 17px;
    margin-top: 8px;
  }
  th {
    background-color: #003366;
    color: #ffffff;
    padding: 7px 10px;
    text-align: left;
    font-size: 18px;
  }
  td {
    padding: 5px 10px;
    border-bottom: 1px solid #e0e0e0;
  }
  tr:nth-child(even) {
    background-color: #f4f8fc;
  }
  .flow-step {
    background-color: #f4f8fc;
    border: 2px solid #0055a5;
    border-radius: 8px;
    padding: 10px 8px;
    text-align: center;
    font-size: 16px;
    flex: 1;
    min-height: 95px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .flow-step strong {
    font-size: 18px;
    color: #003366;
    margin-bottom: 4px;
  }
  .flow-arrow {
    color: #0055a5;
    font-size: 24px;
    font-weight: bold;
  }
  .info-box {
    background-color: #f4f8fc;
    border: 2px solid #0055a5;
    padding: 15px 20px;
    border-radius: 8px;
    margin-top: 12px;
  }
  .alert-box {
    background-color: #ffebee;
    border: 2px solid #c62828;
    padding: 12px 18px;
    border-radius: 8px;
    margin-top: 12px;
  }
  .flow-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 15px;
    gap: 8px;
  }

  .book-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
    margin-top: 15px;
  }
  .book-card {
    background: #ffffff;
    border: 2px solid #0055a5;
    border-radius: 8px;
    padding: 12px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
  }
  .book-tag {
    background-color: #003366;
    color: #ffffff;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 13px;
    font-weight: bold;
    margin-bottom: 8px;
  }
  .book-tag.comp {
    background-color: #0055a5;
  }
  .book-img {
    height: 165px;
    width: auto;
    max-width: 100%;
    object-fit: contain;
    border-radius: 4px;
    box-shadow: 0 3px 6px rgba(0,0,0,0.15);
  }
  .book-info {
    font-size: 13px;
    margin-top: 8px;
    line-height: 1.3;
    color: #222;
  }
  .criteria-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
    margin-top: 20px;
  }
  .crit-box {
    background: #ffffff;
    border-left: 6px solid #0055a5;
    box-shadow: 0 4px 8px rgba(0,0,0,0.08);
    padding: 15px;
    border-radius: 6px;
  }
  .crit-box.center {
    grid-column: span 2;
    border-left: 6px solid #2e7d32;
    background-color: #f0fdf4;
    text-align: center;
  }
  .crit-title {
    color: #003366;
    font-weight: bold;
    font-size: 20px;
    margin-bottom: 5px;
  }
  .concept-box {
    border: 1px solid #d0d7de;
    background-color: #ffffff;
    padding: 16px;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    margin-bottom: 12px;
  }
  .solution-box { background-color: #e8f5e9; border: 2px solid #2e7d32; padding: 15px 20px; border-radius: 8px; margin-top: 12px; }
  .problem-box { background-color: #fff8e6; border: 2px solid #ffb300; padding: 15px 20px; border-radius: 8px; margin-top: 12px; }

  .columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    align-items: center;
  }
---

![width:260px](img/tec.jpg)

# TC2038 - Análisis y diseño de algoritmos avanzados
## Aseoria 1

**Profesor** - _Alison Muñoz Capote_  
**Computación - Facultad de Ingeniería**

---

# El Desafío del Enrutador de Red

<div class="problem-box">

**Caso de Estudio 1**

**El Problema:** Imagina que estás diseñando el algoritmo de enrutamiento para un centro de datos. Tienes una matriz de $M \times N$ que representa los nodos de la red. Cada celda de la matriz contiene un número entero positivo que representa la latencia en milisegundos de pasar por ese nodo. Un paquete de datos debe viajar desde el nodo superior izquierdo $(0, 0)$ hasta el nodo inferior derecho $(M-1, N-1)$. Para evitar bucles de enrutamiento, el paquete solo puede moverse hacia la derecha o hacia abajo.

**Objetivo:** Encontrar la ruta que minimice la latencia total del viaje.

</div>



---

# Transmisión de Mensajes en un Clúster

<div class="problem-box">

**Caso de Estudio 2**

**El Problema:** Tienes un arreglo de enteros positivos donde cada índice representa un servidor en un clúster de procesamiento lineal. El valor en cada índice indica la cantidad máxima de _saltos_ hacia adelante que un mensaje puede dar desde ese servidor. Todos los mensajes comienzan en el servidor del índice 0.

Ejemplo: `[2, 3, 1, 1, 4]`

**Objetivo:** Calcular el número mínimo absoluto de saltos necesarios para que el mensaje alcance el último servidor del arreglo.

---

# Detección de Anomalías en Tráfico de Datos

<div class="problem-box">

**Caso de Estudio 3**

**El Problema:** El sistema de monitoreo de una arquitectura distribuida registra las fluctuaciones de rendimiento (delays) por segundo. Los valores se almacenan en un arreglo de números enteros, los cuales pueden ser positivos (el sistema procesó más rápido de lo esperado) o negativos (el sistema experimentó retrasos).

**Objetivo:** Encontrar el periodo de tiempo continuo (subarreglo contiguo) que represente la mayor ganancia neta de rendimiento (la suma máxima).


---