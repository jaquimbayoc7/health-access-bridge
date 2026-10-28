# Modelo predictivo de barreras: estudio de origen y sus métricas

**Fuente:** manuscrito «A hybrid machine learning approach to predict barrier profiles in youth with physical disabilities», de Julian Andres Quimbayo Castro, Jose Miguel Llanos Mosquera, Alvaro Hernan Alarcon Lopez, Edisney García Perdomo y Willians Aguilar Rodriguez (Corporación Universitaria del Huila, CORHUILA). Código del estudio: https://github.com/jaquimbayoc7/HybridModelDisability (rama `main`).
**Qué es este archivo:** un resumen de los datos y las métricas del estudio, para que el repositorio de HAB tenga a mano la evidencia del modelo que embebe (`backend/model/`). No sustituye al manuscrito.

## Datos

| Campo | Dato |
|---|---|
| Fuente | Conjunto secundario del RLCPD de Garzón (Huila): 899 personas |
| Muestra | 100 jóvenes de 14 a 28 años con discapacidad física (suficiencia estadística χ², p < 0,05; índice de calidad de datos 47,01; valor de información IV = 0,21) |
| Variables | 45 del instrumento del RLCPD; la salida son los perfiles de percepción de barreras |
| Preprocesamiento | *One-hot* de las categóricas, escalamiento mínimo-máximo de las numéricas y sobremuestreo solo en el entrenamiento |
| Partición | 80 % entrenamiento y 20 % prueba, después de generar los perfiles |

## Método

Fase 1: K-Means con k = 3 genera tres perfiles (percepción baja, moderada y alta); se visualizan con PCA. Fase 2: siete modelos supervisados (regresión logística, vecinos más cercanos, bosque aleatorio, Gradient Boosting, XGBoost y otros); Gradient Boosting y XGBoost fueron los mejores. Un análisis de importancia halló una «tríada predictiva»: dificultad de movilidad (Q14), cognición (Q15) y comunicación (Q17).

## Resultados

Gradient Boosting con seis variables de dificultad funcional (partición 80-20):

| Perfil | Precisión | Sensibilidad | F1 |
|---|---|---|---|
| 0 (percepción moderada) | 0,88 | 0,94 | 0,91 |
| 1 (percepción alta) | 1,00 | 1,00 | 1,00 |
| 2 (percepción baja) | 0,90 | 0,83 | 0,87 |

Gradient Boosting con la tríada: exactitud global de 92 %; F1 de 1,00 (alta) y 0,98 (moderada y baja); ROC-AUC entre 0,98 y 1,00 en los tres perfiles.

## Conciliación de las cifras (verificación aritmética)

| Cifra | Resultado de la verificación |
|---|---|
| Tríada: F1 de 1,00, 0,98 y 0,98 | Un F1 de 0,98 exige precisión y sensibilidad de al menos 0,95; la exactitud global (promedio de sensibilidades ponderado por clase) tendría que ser de al menos 95 % |
| Exactitud de 92 % atribuida a la tríada | **Incompatible** con esos F1 |
| Seis variables (tabla 2): sensibilidades 0,94, 1,00 y 0,83 | Exactitud de 92 % **alcanzable** según el peso de cada clase; es la lectura coherente del 92 % |
| Tamaño de la prueba | El 20 % de 100 son 20 casos, pero las sensibilidades de 0,94 y 0,83 exigen al menos 16 y 6 casos en dos clases: las cifras parecen promedios de varias particiones |

Acción recomendada: recalcular la exactitud de la tríada con los datos originales y corregir el manuscrito. Hasta entonces, el trabajo cita los F1 y el ROC-AUC tal como se reportan y presenta el 92 % como «reportado», sin usarlo para comparar modelos.

## Advertencias para quien use estas cifras

- La metodología menciona las variables Q43 a Q45 como entrada del agrupamiento y los resultados las seis variables de dificultad funcional (como la implementación): debe corregirse. Si el agrupamiento y el clasificador usan las mismas variables de dificultad, los perfiles son circulares y las métricas altas no prueban que predigan la percepción real de barreras.
- Los autores indican que el modelo supervisado reproduce la lógica del agrupamiento que generó los perfiles; no son categorías clínicas. Límites declarados: diseño transversal, datos autorreportados, éxito específico de las barreras de transporte, n = 100 y variables ausentes.
- En el estudio el perfil 0 es la percepción moderada, el 1 la alta y el 2 la baja; el backend de HAB describe 0 como bajas, 1 como moderadas y 2 como altas (`backend/app/routers/patients.py`). Verificar con los centroides del modelo que se use.
- El *pipeline* que HAB entrena en cada despliegue (`backend/model/train_model.py`) usa 1.000 registros sintéticos y trece variables; las métricas anteriores no se trasladan a él sin reentrenar con los datos reales.
