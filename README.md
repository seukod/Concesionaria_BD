# Cómo usar el script

## 1. Activar entorno virtual (si corresponde)

Activa tu entorno virtual de Python antes de ejecutar el script.

## 2. Instalar dependencias

```bash
pip install psycopg2-binary matplotlib seaborn numpy
```

## 3. Ejecutar el script

Usa el siguiente comando para iniciar el programa, reemplazando `año` por el valor que quieras consultar:

```bash
python consultas.py año
```

> 💬 **Comentario:** La base de datos está alojada de forma online en Supabase.




# Concesionaria_BD
Sistema Concesionaria 

La base de datos a trabajar constará de una serie de concesionarias de vehículos (autos pequeños), en la cual habrá mínimo 2 sucursales en cada ciudad de Chile. 

La problemática que busca solucionar esta BD es principalmente controlar el espacio de los vehículos en cada concesionaria, manteniendo un orden respecto a la venta de automóviles, además, se requiere mejorar la venta de vehiculas relacionada a la oferta y demanda en cada zona del país, es decir, vender cierto modelo de vehículos dependiendo de la región, comuna y ciudad.

A continuación se explican características y como funciona el sistema a implementar:

-Cada consecionaria posée un ID único, la región donde se encuentra, la comuna, ciudad y dirección. Se indicará la capacidad máxima de cada concesionaria (dependiendo del espacio de cada una) y una lista con la oferta de modelos que tienen. También cada región contará con varias sucursales y una sede principal 

-Cada modelo cuenta con un id único además de su nombre, marca, tipo de vehículo (auto, furgoneta o camioneta), precio y cantidad de dicho modelo. Cantidad de puertas, máximo de pasajeros, Octanaje de gasolina o si utiliza Diesel. Maletero (si es pequeño, mediano o grande) y tipo de tracción.

-También, cada modelo posee una lista 'Auto' donde se puede observar específicamente cada uno, donde su ID será la patente, fecha en la que llegó a la concesionaria, kilometraje, si es nuevo o usado y si ha sido ocupado como auto de prueba. 

-Si un auto pasa 2 años sin venderse, se le aplicará un descuento del 10% de su valor y pasará a ser auto de prueba. En caso de que el periodo de prueba dure 2 años o más se aplicará un protocolo de devolución a empresa. 

-Cada concesionaria posee una lista con sus respectivos autos vendidos y información sobre la venta. Como si el pago fué concretado al contado o en cuotas, nombre del adquisisor, número de patente y fecha de venta. 

 
