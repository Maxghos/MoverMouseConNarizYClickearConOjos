**HeadMouse Eyes-Free — Control del cursor usando la nariz y clics con parpadeo prolongado**

Este proyecto permite controlar el cursor del mouse sin usar las manos, utilizando solo movimientos suaves de la nariz y parpadeos con ambos ojos para realizar clics.
Es una herramienta accesible, intuitiva y ligera que funciona con cualquier cámara web estándar.

Diseñado para ser usado “con los ojos cerrados” —literalmente— este sistema combina MediaPipe FaceMesh, OpenCV y PyAutoGUI para mapear en tiempo real la posición del rostro y transformar los gestos naturales en acciones del mouse.

-> Características principales
-> Control de puntero con la nariz

El movimiento del cursor se basa en la posición de la punta de la nariz dentro de una zona de sensibilidad calibrada.
El sistema incluye suavizado para garantizar movimientos fluidos y estables.

-> Clic mediante parpadeo prolongado de ambos ojos

El clic izquierdo se ejecuta cuando el usuario:

Cierra ambos ojos al mismo tiempo

Los mantiene cerrados por más de 0.5 segundos

Y pasa el tiempo de cooldown para evitar clics repetidos

Esto permite clickear sin manos, sin voz y sin hardware adicional.

-> Calibración personalizada

Con solo presionar <, el sistema ajusta automáticamente:

El centro neutral del movimiento de nariz

Las distancias reales del parpadeo cuando los ojos están abiertos
Esto hace que funcione con cualquier rostro, iluminación o postura.

-> Sin reflejo de cámara

La imagen no se espeja, permitiendo un control preciso según la dirección real del movimiento.

-> ¿Para qué sirve? (Casos de uso)

Este proyecto tiene aplicaciones reales en:

-> Accesibilidad e inclusión digital

Usuarios con movilidad reducida pueden utilizar el computador sin manos.

-> Interfaces alternativas e interacción experimental

Ideal para prototipos de interfaces “hands-free”, interacción hombre-máquina y proyectos creativos.

-> Control experimental en juegos o arte digital

Convertir la cara en un input abre posibilidades para gaming, arte generativo o control de instalaciones.

-> Productividad cuando no se pueden usar las manos

Útil en situaciones donde las manos no están disponibles momentáneamente (cocina, laboratorio, etc.).

-> Ventajas

Fácil de usar: solo cámara web y Python.

Extremadamente natural: movimientos mínimos del rostro.

Clic preciso mediante duración del parpadeo, reduciendo falsos positivos.

Libre de manos y silencioso: no requiere voz ni gestos exagerados.

Totalmente local: no envía datos a internet.

Personalizable: sensibilidad, tiempos, distancias… todo ajustable.

-> Cómo funciona técnicamente (resumen)

+Se usa MediaPipe FaceMesh para extraer landmarks del rostro.

+Se rastrea la punta de la nariz como punto principal de movimiento.

+Se detectan las distancias de los párpados para medir parpadeos.

+Se realiza una calibración inicial del centro y el estado “ojo abierto”.

+Se mapea el movimiento facial a coordenadas de pantalla usando PyAutoGUI.

+Se suaviza el movimiento con un filtro exponencial.

+Parpadeo prolongado + cooldown → clic.
