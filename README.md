# ParallelismSimulation
Program to search for a good cpu  architecture for saving power.

Autor: Victor Manuel Lantigua Cano

## Descripción del problema:

En la actualidad contamos con procesadores verdaderamente poderosos y sobre todo contamos con procesadores capaces de realizar grandes cantidades de trabajo haciendo uso del paralelismo para mejorar su eficiencia. El paralelismo consiste en dividir las tareas entre varios procesadores que trabajan sobre estas al mismo tiempo. En equipos con grandes cargas de trabajo se suelen usar varios procesadores para realizar gran cantidad de tareas en paralelo, pero en el sector comercial no solo esto es importante. Los procesadores mientras más potentes, requieren de gran cantidad de energía para trabajar. En este proyecto se pretende ofrecer un modelo para dado un conjunto de procesadores, un determinado wataje y un tiempo, realizar simulaciones para tratar de obtener una arquitectura potente y enérgicamente eficiente.



## Simulación:

Se realizará un simulación de tipo cliente servidor, esta se ejecutará en intervalos de un segundo y contará con un scheduler parar repartir la cantidad de instrucciones que se necesitan ejecutar entre los distintos procesadores. Cuando un procesador ejecute un segundo de instrucciones se calcula la energía consumida y se va acumulando el consumo de cada procesador y la cantidad de instrucciones procesadas.

El scheduler sigue una estrategia en la que le asigna a cada procesador un cantidad de instrucciones equivalente a su poder de procesamiento con respecto a la potencia total de la arquitectura simulada.



## IA:

Se usara un algoritmo genético para tratar de hallar la arquitectura que se quiere lograr. La representación genética de la arquitectura será un array con la cantidad de cada tipo de procesador usado en la arquitectura. La función de entrenamiento será la simulación antes descrita y como métrica se usará la cantidad total de instrucciones procesadas, la cual se hará 0 si durante la simulación se supera el consumo de energía esperado.

Se inicializará la población con tamaño prefijado generando de forma aleatoria con la misma probabilidad la cantidad que se usará de cada procesador. La selección se hará aleatoriamente pero usando el principio de elitismo para asegurar que las mejores arquitecturas serán tomadas en cuenta para la próxima generación. Después llevamos a cabo el cruce y la mutación de forma aleatoria.



## Procesador:

Un procesador está definido por la frecuencia máxima que es capaz de alcanzar en Mhz, el consumo en watts para cuando alcanza su frecuencia máxima, y una cola de instrucciones por ejecutar.



## Recomendaciones:

Para una continuación de este estudio se recomienda:

- La implementación de un DSL para facilitar la definición de nuevos procesadores.
- Buscar una mejor estrategia de scheduling para la asignación de las instrucciones, tal vez, tratarlo como un problema de asignación.
- Tener en cuenta el calentamiento de los procesadores para tener un modelo más acertado.
- Implementar una mejor función para calcular el consumo de los procesadores.
