#Clase manejador de escenas

#Estructura ideal: Árbol debido a que hay una jerarquía de objetos
#Por ejemplo, si tengo un objeto encima de otro, el efecto que ocurra en el objeto de abajo (padre) afectará al otro (hijo)
#Reviso posiciones relativas con respecto al objeto padre
#Transformación padre = M1; Transformación hijo = M1 * M2

#Revisar glPushMatrix y glPopMatrix -> Por lo general guardan los estados anteriores del stack de transformaciones