"""Question bank for ExpoCiencia 2026: causes of water cuts in Cartagena.

20 Spanish questions split into 5 mixed-topic lists of 4 questions each, aimed
at first-grade readers. Each list combines questions from different parts of
the project (causes, treatment, technology, surveys, conclusions) instead of
sticking to a single topic, so every round feels varied.

An English translation of the same 20 questions (PROJECT_QUESTIONS_EN /
QUESTION_SETS_EN) coexists alongside the Spanish bank as 5 additional lists,
seeded additively -- the Spanish rows are never touched when the English
bank is inserted.
"""

from datetime import datetime, timezone

PROJECT_QUESTIONS: list[dict] = [
    # --- Banco 1: Causas de los cortes de agua (orden 1-4) ---
    {
        "texto": "Según las encuestas, ¿qué causa señalaron principalmente las personas como responsable de los cortes de agua?",
        "opcion_a": "La sequía.",
        "opcion_b": "Las fugas de agua.",
        "opcion_c": "Las tuberías dañadas.",
        "opcion_d": "La alta demanda de agua.",
        "respuesta_correcta": "C",
        "explicacion": "Según los resultados de las encuestas, las tuberías dañadas fueron la causa señalada con mayor frecuencia por las personas encuestadas.",
        "orden": 1,
    },
    {
        "texto": "Si una falla eléctrica detiene las bombas, ¿por qué puede afectarse el servicio de agua?",
        "opcion_a": "Porque las bombas producen la lluvia.",
        "opcion_b": "Porque las bombas ayudan a distribuir el agua hacia las viviendas.",
        "opcion_c": "Porque las bombas reemplazan las tuberías.",
        "opcion_d": "Porque las bombas eliminan la necesidad de tratar el agua.",
        "respuesta_correcta": "B",
        "explicacion": "Las bombas ayudan a distribuir el agua. Por eso, si una falla eléctrica hace que dejen de funcionar, puede afectarse la distribución del agua.",
        "orden": 2,
    },
    {
        "texto": "Si el agua cruda llega a la planta con muchas algas, ¿qué puede ocurrir?",
        "opcion_a": "El proceso de tratamiento puede volverse más lento.",
        "opcion_b": "El agua se convierte inmediatamente en potable.",
        "opcion_c": "Las tuberías producen más agua.",
        "opcion_d": "La cantidad de agua disponible aumenta automáticamente.",
        "respuesta_correcta": "A",
        "explicacion": "La presencia de algas puede hacer necesario lavar los filtros con mayor frecuencia, lo que puede disminuir la cantidad de agua que se produce durante el tratamiento.",
        "orden": 3,
    },
    {
        "texto": "¿Por qué no se puede decir que los cortes de agua tienen una sola causa?",
        "opcion_a": "Porque solamente ocurren cuando llueve.",
        "opcion_b": "Porque las tuberías nunca afectan el servicio.",
        "opcion_c": "Porque todos los cortes tienen una causa diferente.",
        "opcion_d": "Porque pueden combinarse problemas de tuberías, demanda, clima y calidad del agua.",
        "respuesta_correcta": "D",
        "explicacion": "El proyecto muestra que los cortes pueden estar relacionados con diferentes factores, como el estado de las tuberías, la demanda de agua, las condiciones climáticas y las dificultades en el tratamiento.",
        "orden": 4,
    },
    # --- Banco 2: El tratamiento y distribución del agua (orden 5-8) ---
    {
        "texto": "Si 27 de las 30 personas encuestadas dijeron haber sufrido cortes de agua, ¿qué podemos entender de este resultado?",
        "opcion_a": "Que solamente tres personas tienen agua.",
        "opcion_b": "Que muchas de las personas encuestadas han experimentado cortes de agua.",
        "opcion_c": "Que todas las personas de Cartagena tienen cortes todos los días.",
        "opcion_d": "Que las encuestas no sirven para investigar.",
        "respuesta_correcta": "B",
        "explicacion": "27 de las 30 personas encuestadas dijeron haber experimentado cortes, por lo que la mayoría de las personas participantes había vivido esta situación.",
        "orden": 5,
    },
    {
        "texto": "Si una tubería antigua está deteriorada y además recibe cambios fuertes de presión, ¿qué podría suceder?",
        "opcion_a": "Podría producir más agua.",
        "opcion_b": "Podría hacerse nueva.",
        "opcion_c": "Podría romperse y provocar una fuga.",
        "opcion_d": "Podría eliminar la demanda de agua.",
        "respuesta_correcta": "C",
        "explicacion": "Las tuberías deterioradas pueden ser más vulnerables a los cambios de presión, lo que puede provocar grietas, roturas o fugas.",
        "orden": 6,
    },
    {
        "texto": "¿Por qué el crecimiento de la población y el turismo puede aumentar la presión sobre el sistema de agua?",
        "opcion_a": "Porque aumenta la cantidad de agua que las personas necesitan utilizar.",
        "opcion_b": "Porque elimina las fugas de agua.",
        "opcion_c": "Porque hace que las tuberías sean automáticamente más nuevas.",
        "opcion_d": "Porque disminuye el consumo de agua.",
        "respuesta_correcta": "A",
        "explicacion": "Cuando aumenta la población, el turismo o el consumo, también aumenta la cantidad de agua que debe atender el sistema.",
        "orden": 7,
    },
    {
        "texto": "Si es necesario lavar los filtros de la planta con mayor frecuencia, ¿qué puede pasar con la cantidad de agua disponible?",
        "opcion_a": "Puede aumentar inmediatamente.",
        "opcion_b": "No puede cambiar.",
        "opcion_c": "Las bombas producen el agua que falta.",
        "opcion_d": "Puede disminuir mientras se realiza el proceso de tratamiento.",
        "respuesta_correcta": "D",
        "explicacion": "Cuando los filtros necesitan lavarse con mayor frecuencia, el proceso de tratamiento puede volverse más lento y disminuir temporalmente la cantidad de agua disponible.",
        "orden": 8,
    },
    # --- Banco 3: Tecnología e infraestructura (orden 9-12) ---
    {
        "texto": "¿Qué relación existe entre el tratamiento del agua y los cortes de agua?",
        "opcion_a": "El tratamiento elimina la necesidad de utilizar tuberías.",
        "opcion_b": "Si el tratamiento presenta dificultades, puede disminuir la cantidad de agua disponible para distribuir.",
        "opcion_c": "El tratamiento hace que las personas consuman menos agua automáticamente.",
        "opcion_d": "El tratamiento evita cualquier problema en la red.",
        "respuesta_correcta": "B",
        "explicacion": "Si durante el tratamiento se presentan dificultades o el proceso se vuelve más lento, puede disminuir la cantidad de agua disponible para distribuir a la población.",
        "orden": 9,
    },
    {
        "texto": "Si una ciudad necesita cada vez más agua, pero la cantidad de agua disponible disminuye, ¿qué problema puede presentarse?",
        "opcion_a": "Las tuberías dejan de ser necesarias.",
        "opcion_b": "El sistema automáticamente produce más agua.",
        "opcion_c": "Puede aumentar la presión sobre el sistema de abastecimiento.",
        "opcion_d": "El agua deja de necesitar tratamiento.",
        "respuesta_correcta": "C",
        "explicacion": "Cuando existe una mayor necesidad de agua y al mismo tiempo hay menos agua disponible, aumenta la presión sobre el sistema para poder atender la demanda.",
        "orden": 10,
    },
    {
        "texto": "Si los resultados de una encuesta se organizan en tablas y gráficas, ¿qué podemos identificar con mayor facilidad?",
        "opcion_a": "Patrones y causas que aparecen con mayor frecuencia.",
        "opcion_b": "Nuevas respuestas que nadie dio.",
        "opcion_c": "La cantidad de agua que tendrá la ciudad.",
        "opcion_d": "Las tuberías que se van a romper.",
        "respuesta_correcta": "A",
        "explicacion": "Organizar los resultados en tablas y gráficas permite observar los datos con mayor facilidad e identificar patrones y respuestas que aparecen con mayor frecuencia.",
        "orden": 11,
    },
    {
        "texto": "¿Por qué reemplazar tuberías antiguas puede ayudar a mejorar el servicio de agua?",
        "opcion_a": "Porque elimina la necesidad de tratar el agua.",
        "opcion_b": "Porque hace que las personas necesiten menos agua.",
        "opcion_c": "Porque aumenta automáticamente la lluvia.",
        "opcion_d": "Porque puede reducir problemas relacionados con grietas, roturas y fugas.",
        "respuesta_correcta": "D",
        "explicacion": "El deterioro de las tuberías puede producir grietas, roturas y fugas. Por eso, reemplazar las tuberías antiguas puede ayudar a reducir estos problemas.",
        "orden": 12,
    },
    # --- Banco 4: Lo que dicen las encuestas (orden 13-16) ---
    {
        "texto": "Si una encuesta muestra que muchas personas creen que las tuberías dañadas son una causa importante, ¿qué deberían hacer los investigadores?",
        "opcion_a": "Dar por terminada la investigación inmediatamente.",
        "opcion_b": "Ignorar las demás posibles causas.",
        "opcion_c": "Comparar ese resultado con información técnica para comprender mejor el problema.",
        "opcion_d": "Cambiar las respuestas de la encuesta.",
        "respuesta_correcta": "C",
        "explicacion": "La encuesta permite conocer lo que observa la comunidad, pero compararla con información técnica ayuda a comprender mejor el problema y sus diferentes causas.",
        "orden": 13,
    },
    {
        "texto": "¿Por qué la tecnología puede ayudar a prevenir problemas en el sistema de agua?",
        "opcion_a": "Porque herramientas como los medidores de presión pueden ayudar a detectar fallas antes de que la red colapse.",
        "opcion_b": "Porque la tecnología hace que nunca se rompa una tubería.",
        "opcion_c": "Porque los sensores producen agua.",
        "opcion_d": "Porque las bombas funcionan sin electricidad.",
        "respuesta_correcta": "A",
        "explicacion": "Los sistemas de medición y control permiten observar condiciones de la red y pueden ayudar a detectar problemas antes de que provoquen fallas mayores.",
        "orden": 14,
    },
    {
        "texto": "Si el fenómeno de El Niño disminuye el nivel del río Magdalena y del Canal del Dique, ¿por qué esto puede afectar a Cartagena?",
        "opcion_a": "Porque allí están todas las tuberías de las viviendas.",
        "opcion_b": "Porque de allí se capta parte del agua que necesita la ciudad.",
        "opcion_c": "Porque allí se encuentran las bombas de todas las casas.",
        "opcion_d": "Porque el río produce directamente el agua potable.",
        "respuesta_correcta": "B",
        "explicacion": "El proyecto explica que parte del agua utilizada para el abastecimiento de Cartagena se obtiene mediante captación relacionada con el Canal del Dique. Por eso, una disminución importante de los niveles puede afectar la disponibilidad de agua.",
        "orden": 15,
    },
    {
        "texto": "¿Cuál es una de las principales enseñanzas del proyecto sobre el cuidado del agua?",
        "opcion_a": "Que solamente la empresa de acueducto debe cuidar el agua.",
        "opcion_b": "Que los cortes de agua no afectan a las personas.",
        "opcion_c": "Que las tuberías no necesitan mantenimiento.",
        "opcion_d": "Que cuidar y utilizar responsablemente el agua es responsabilidad de todos.",
        "respuesta_correcta": "D",
        "explicacion": "El proyecto concluye que el cuidado del agua no depende solamente de una institución, sino que también requiere un uso responsable por parte de las personas.",
        "orden": 16,
    },
    # --- Banco 5: Lo que aprendimos del proyecto (orden 17-20) ---
    {
        "texto": "¿Por qué es útil comparar los resultados de una encuesta con información técnica?",
        "opcion_a": "Porque permite relacionar lo que observa la comunidad con información que ayuda a comprender el problema.",
        "opcion_b": "Porque permite cambiar las respuestas de las personas.",
        "opcion_c": "Porque demuestra que las encuestas no sirven.",
        "opcion_d": "Porque permite eliminar las causas del problema.",
        "respuesta_correcta": "A",
        "explicacion": "Comparar los resultados de la encuesta con información técnica permite observar el problema desde diferentes fuentes y comprender mejor sus posibles causas.",
        "orden": 17,
    },
    {
        "texto": "Si una tubería antigua presenta grietas y además existe una fuga, ¿qué consecuencia puede tener para el servicio?",
        "opcion_a": "Aumenta automáticamente la cantidad de agua disponible.",
        "opcion_b": "Puede perderse agua antes de que llegue a los usuarios.",
        "opcion_c": "Las bombas producen el agua que se pierde.",
        "opcion_d": "La demanda de agua disminuye.",
        "respuesta_correcta": "B",
        "explicacion": "Una fuga en una tubería puede hacer que parte del agua se pierda antes de llegar a las personas que necesitan utilizarla.",
        "orden": 18,
    },
    {
        "texto": "Si el tratamiento del agua se vuelve más lento y al mismo tiempo aumenta la demanda, ¿por qué puede aumentar la dificultad para mantener el servicio?",
        "opcion_a": "Porque las tuberías dejan de funcionar automáticamente.",
        "opcion_b": "Porque la demanda desaparece.",
        "opcion_c": "Porque se dispone de menos agua para atender una necesidad mayor.",
        "opcion_d": "Porque el agua ya no necesita ser tratada.",
        "respuesta_correcta": "C",
        "explicacion": "Si se dispone de menos agua debido a dificultades en el tratamiento mientras aumenta la cantidad de agua que se necesita, resulta más difícil atender la demanda del sistema.",
        "orden": 19,
    },
    {
        "texto": "Si los cortes de agua pueden tener varias causas, ¿qué sería lo más adecuado para comprender el problema?",
        "opcion_a": "Elegir una causa sin investigar.",
        "opcion_b": "Preguntar solamente a una persona.",
        "opcion_c": "Suponer que todos los cortes son iguales.",
        "opcion_d": "Investigar diferentes factores y comparar información.",
        "respuesta_correcta": "D",
        "explicacion": "El proyecto muestra que para comprender los cortes es necesario considerar diferentes factores y comparar información de distintas fuentes.",
        "orden": 20,
    },
]

QUESTION_SETS: list[dict] = [
    {
        "nombre": "Causas de los cortes de agua",
        "descripcion": "Preguntas variadas sobre las causas de los cortes de agua explicadas en el proyecto.",
        "orden_inicio": 1,
        "orden_fin": 4,
    },
    {
        "nombre": "El tratamiento y distribución del agua",
        "descripcion": "Preguntas variadas sobre encuestas, tuberías, demanda y tratamiento del agua.",
        "orden_inicio": 5,
        "orden_fin": 8,
    },
    {
        "nombre": "Tecnología e infraestructura",
        "descripcion": "Preguntas variadas sobre tratamiento, presión del sistema y análisis de encuestas.",
        "orden_inicio": 9,
        "orden_fin": 12,
    },
    {
        "nombre": "Lo que dicen las encuestas",
        "descripcion": "Preguntas variadas sobre encuestas, tecnología, captación de agua y conclusiones.",
        "orden_inicio": 13,
        "orden_fin": 16,
    },
    {
        "nombre": "Lo que aprendimos del proyecto",
        "descripcion": "Preguntas variadas sobre encuestas, tuberías, tratamiento y conclusiones del proyecto.",
        "orden_inicio": 17,
        "orden_fin": 20,
    },
]

# Nombres exclusivos del banco de 20 preguntas (ExpoCiencia 2026). Ninguno de
# estos 4 nombres existió en bancos anteriores, así que sirven para detectar
# de forma segura si el banco actual ya es la versión nueva.
_NEW_BANK_MARKER_LIST_NAMES = (
    "El tratamiento y distribución del agua",
    "Tecnología e infraestructura",
    "Lo que dicen las encuestas",
    "Lo que aprendimos del proyecto",
)

# --- English translation of the same 20 questions, orden 21-40 ---
# Faithful translations of PROJECT_QUESTIONS: same correct answers, same
# option order, same level of difficulty, no new information added.
PROJECT_QUESTIONS_EN: list[dict] = [
    # --- Bank 1: Causes of Water Cuts (orden 21-24) ---
    {
        "texto": "According to the surveys, what cause did people mainly identify as responsible for water cuts?",
        "opcion_a": "Drought.",
        "opcion_b": "Water leaks.",
        "opcion_c": "Damaged pipes.",
        "opcion_d": "High water demand.",
        "respuesta_correcta": "C",
        "explicacion": "According to the survey results, damaged pipes were the cause most frequently identified by the people who were surveyed.",
        "orden": 21,
    },
    {
        "texto": "If a power failure stops the water pumps, why can the water service be affected?",
        "opcion_a": "Because the pumps produce rain.",
        "opcion_b": "Because the pumps help distribute water to homes.",
        "opcion_c": "Because the pumps replace the pipes.",
        "opcion_d": "Because the pumps eliminate the need to treat the water.",
        "respuesta_correcta": "B",
        "explicacion": "The pumps help distribute water. Therefore, if a power failure causes them to stop working, water distribution can be affected.",
        "orden": 22,
    },
    {
        "texto": "If raw water arrives at the treatment plant with a lot of algae, what can happen?",
        "opcion_a": "The treatment process can become slower.",
        "opcion_b": "The water immediately becomes drinkable.",
        "opcion_c": "The pipes produce more water.",
        "opcion_d": "The amount of available water automatically increases.",
        "respuesta_correcta": "A",
        "explicacion": "The presence of algae may require the filters to be washed more frequently, which can reduce the amount of water produced during treatment.",
        "orden": 23,
    },
    {
        "texto": "Why can't we say that water cuts have only one cause?",
        "opcion_a": "Because they only happen when it rains.",
        "opcion_b": "Because pipes never affect the service.",
        "opcion_c": "Because every water cut has a different cause.",
        "opcion_d": "Because problems with pipes, demand, weather, and water quality can occur together.",
        "respuesta_correcta": "D",
        "explicacion": "The project shows that water cuts can be related to different factors, such as the condition of the pipes, water demand, weather conditions, and difficulties in the treatment process.",
        "orden": 24,
    },
    # --- Bank 2: Water Treatment and Distribution (orden 25-28) ---
    {
        "texto": "If 27 out of the 30 people surveyed said they had experienced water cuts, what can we understand from this result?",
        "opcion_a": "Only three people have water.",
        "opcion_b": "Many of the people surveyed have experienced water cuts.",
        "opcion_c": "Everyone in Cartagena has water cuts every day.",
        "opcion_d": "Surveys are not useful for research.",
        "respuesta_correcta": "B",
        "explicacion": "27 out of the 30 people surveyed said they had experienced water cuts, meaning that most of the participants had experienced this situation.",
        "orden": 25,
    },
    {
        "texto": "If an old pipe is damaged and also experiences strong pressure changes, what could happen?",
        "opcion_a": "It could produce more water.",
        "opcion_b": "It could become new.",
        "opcion_c": "It could break and cause a leak.",
        "opcion_d": "It could eliminate water demand.",
        "respuesta_correcta": "C",
        "explicacion": "Damaged pipes can be more vulnerable to pressure changes, which can cause cracks, breaks, or leaks.",
        "orden": 26,
    },
    {
        "texto": "Why can population growth and tourism increase pressure on the water system?",
        "opcion_a": "Because they increase the amount of water people need to use.",
        "opcion_b": "Because they eliminate water leaks.",
        "opcion_c": "Because they automatically make the pipes newer.",
        "opcion_d": "Because they reduce water consumption.",
        "respuesta_correcta": "A",
        "explicacion": "When the population, tourism, or consumption increases, the water system must provide more water to meet the demand.",
        "orden": 27,
    },
    {
        "texto": "If the treatment plant's filters need to be washed more frequently, what can happen to the amount of available water?",
        "opcion_a": "It can immediately increase.",
        "opcion_b": "It cannot change.",
        "opcion_c": "The pumps produce the missing water.",
        "opcion_d": "It can decrease while the treatment process is being carried out.",
        "respuesta_correcta": "D",
        "explicacion": "When filters need to be washed more frequently, the treatment process can become slower and temporarily reduce the amount of available water.",
        "orden": 28,
    },
    # --- Bank 3: Technology and Infrastructure (orden 29-32) ---
    {
        "texto": "What is the relationship between water treatment and water cuts?",
        "opcion_a": "Treatment eliminates the need to use pipes.",
        "opcion_b": "If the treatment process has difficulties, the amount of water available for distribution may decrease.",
        "opcion_c": "Treatment automatically makes people consume less water.",
        "opcion_d": "Treatment prevents any problems in the water network.",
        "respuesta_correcta": "B",
        "explicacion": "If difficulties occur during water treatment or the process becomes slower, there may be less water available for distribution to the population.",
        "orden": 29,
    },
    {
        "texto": "If a city needs more and more water, but the amount of available water decreases, what problem can occur?",
        "opcion_a": "Pipes are no longer necessary.",
        "opcion_b": "The system automatically produces more water.",
        "opcion_c": "Pressure on the water supply system can increase.",
        "opcion_d": "Water no longer needs to be treated.",
        "respuesta_correcta": "C",
        "explicacion": "When there is a greater need for water while less water is available, the system faces greater pressure to meet the demand.",
        "orden": 30,
    },
    {
        "texto": "If survey results are organized into tables and graphs, what can we identify more easily?",
        "opcion_a": "Patterns and causes that appear more frequently.",
        "opcion_b": "New answers that nobody gave.",
        "opcion_c": "How much water the city will have.",
        "opcion_d": "Which pipes will break.",
        "respuesta_correcta": "A",
        "explicacion": "Organizing survey results into tables and graphs makes the data easier to understand and helps identify patterns and answers that appear most frequently.",
        "orden": 31,
    },
    {
        "texto": "Why can replacing old pipes help improve the water service?",
        "opcion_a": "Because it eliminates the need to treat the water.",
        "opcion_b": "Because it makes people need less water.",
        "opcion_c": "Because it automatically increases rainfall.",
        "opcion_d": "Because it can reduce problems related to cracks, breaks, and leaks.",
        "respuesta_correcta": "D",
        "explicacion": "Damaged pipes can develop cracks, breaks, and leaks. Therefore, replacing old pipes can help reduce these problems.",
        "orden": 32,
    },
    # --- Bank 4: What the Surveys Tell Us (orden 33-36) ---
    {
        "texto": "If a survey shows that many people believe damaged pipes are an important cause, what should researchers do?",
        "opcion_a": "End the research immediately.",
        "opcion_b": "Ignore the other possible causes.",
        "opcion_c": "Compare this result with technical information to better understand the problem.",
        "opcion_d": "Change the survey answers.",
        "respuesta_correcta": "C",
        "explicacion": "A survey helps us understand what the community observes, but comparing it with technical information helps us better understand the problem and its different causes.",
        "orden": 33,
    },
    {
        "texto": "Why can technology help prevent problems in the water system?",
        "opcion_a": "Because tools such as pressure meters can help detect problems before the network fails.",
        "opcion_b": "Because technology makes sure that a pipe can never break.",
        "opcion_c": "Because sensors produce water.",
        "opcion_d": "Because pumps work without electricity.",
        "respuesta_correcta": "A",
        "explicacion": "Measurement and control systems allow us to monitor the water network and can help detect problems before they cause major failures.",
        "orden": 34,
    },
    {
        "texto": "If the El Niño phenomenon lowers the water level of the Magdalena River and the Canal del Dique, why can this affect Cartagena?",
        "opcion_a": "Because all household pipes are located there.",
        "opcion_b": "Because part of the water needed by the city is obtained from there.",
        "opcion_c": "Because all household pumps are located there.",
        "opcion_d": "Because the river directly produces drinking water.",
        "respuesta_correcta": "B",
        "explicacion": "The project explains that part of Cartagena's water supply comes from water captured through the Canal del Dique. Therefore, a significant decrease in water levels can affect water availability.",
        "orden": 35,
    },
    {
        "texto": "What is one of the main lessons of the project about taking care of water?",
        "opcion_a": "Only the water company should take care of water.",
        "opcion_b": "Water cuts do not affect people.",
        "opcion_c": "Pipes do not need maintenance.",
        "opcion_d": "Taking care of water and using it responsibly is everyone's responsibility.",
        "respuesta_correcta": "D",
        "explicacion": "The project concludes that taking care of water is not only the responsibility of an institution; people also need to use this resource responsibly.",
        "orden": 36,
    },
    # --- Bank 5: What We Learned from the Project (orden 37-40) ---
    {
        "texto": "Why is it useful to compare survey results with technical information?",
        "opcion_a": "Because it allows us to relate what the community observes to information that helps us understand the problem.",
        "opcion_b": "Because it allows us to change people's answers.",
        "opcion_c": "Because it proves that surveys are not useful.",
        "opcion_d": "Because it eliminates the causes of the problem.",
        "respuesta_correcta": "A",
        "explicacion": "Comparing survey results with technical information allows us to look at the problem from different sources and better understand its possible causes.",
        "orden": 37,
    },
    {
        "texto": "If an old pipe has cracks and there is also a leak, what consequence can this have for the water service?",
        "opcion_a": "The amount of available water automatically increases.",
        "opcion_b": "Water can be lost before it reaches users.",
        "opcion_c": "The pumps produce the water that is lost.",
        "opcion_d": "Water demand decreases.",
        "respuesta_correcta": "B",
        "explicacion": "A leak in a pipe can cause some of the water to be lost before it reaches the people who need to use it.",
        "orden": 38,
    },
    {
        "texto": "If water treatment becomes slower while water demand increases, why can it become more difficult to maintain the service?",
        "opcion_a": "Because the pipes automatically stop working.",
        "opcion_b": "Because water demand disappears.",
        "opcion_c": "Because there is less water available to meet a greater need.",
        "opcion_d": "Because water no longer needs to be treated.",
        "respuesta_correcta": "C",
        "explicacion": "If less water is available because of difficulties in treatment while the amount of water needed increases, it becomes more difficult for the system to meet the demand.",
        "orden": 39,
    },
    {
        "texto": "If water cuts can have several causes, what would be the best way to understand the problem?",
        "opcion_a": "Choose one cause without investigating.",
        "opcion_b": "Ask only one person.",
        "opcion_c": "Assume that all water cuts are the same.",
        "opcion_d": "Investigate different factors and compare information.",
        "respuesta_correcta": "D",
        "explicacion": "The project shows that understanding water cuts requires considering different factors and comparing information from different sources.",
        "orden": 40,
    },
]

QUESTION_SETS_EN: list[dict] = [
    {
        "nombre": "Causes of Water Cuts",
        "descripcion": "Mixed questions about the causes of water cuts explained in the project.",
        "orden_inicio": 21,
        "orden_fin": 24,
    },
    {
        "nombre": "Water Treatment and Distribution",
        "descripcion": "Mixed questions about surveys, pipes, demand, and water treatment.",
        "orden_inicio": 25,
        "orden_fin": 28,
    },
    {
        "nombre": "Technology and Infrastructure",
        "descripcion": "Mixed questions about treatment, system pressure, and survey analysis.",
        "orden_inicio": 29,
        "orden_fin": 32,
    },
    {
        "nombre": "What the Surveys Tell Us",
        "descripcion": "Mixed questions about surveys, technology, water capture, and conclusions.",
        "orden_inicio": 33,
        "orden_fin": 36,
    },
    {
        "nombre": "What We Learned from the Project",
        "descripcion": "Mixed questions about surveys, pipes, treatment, and project conclusions.",
        "orden_inicio": 37,
        "orden_fin": 40,
    },
]

# Los 5 nombres son exclusivos del banco en inglés: ninguno coincide con
# bancos anteriores ni con el banco en español, así que sirven para detectar
# de forma segura si el banco en inglés ya fue sembrado.
_ENGLISH_BANK_MARKER_LIST_NAMES = (
    "Causes of Water Cuts",
    "Water Treatment and Distribution",
    "Technology and Infrastructure",
    "What the Surveys Tell Us",
    "What We Learned from the Project",
)


def _insert_questions(connection, questions: list[dict]) -> dict[int, int]:
    connection.executemany(
        """
        INSERT INTO preguntas (
            texto, opcion_a, opcion_b, opcion_c, opcion_d,
            respuesta_correcta, explicacion, activa, orden
        ) VALUES (
            :texto, :opcion_a, :opcion_b, :opcion_c, :opcion_d,
            :respuesta_correcta, :explicacion, 1, :orden
        )
        """,
        questions,
    )

    rows = connection.execute(
        "SELECT id, orden FROM preguntas ORDER BY orden ASC, id ASC"
    ).fetchall()
    return {int(row["orden"]): int(row["id"]) for row in rows}


def _insert_question_sets(
    connection, order_to_id: dict[int, int], question_sets: list[dict]
) -> None:
    created_at = datetime.now(timezone.utc).isoformat()

    for question_set in question_sets:
        cursor = connection.execute(
            """
            INSERT INTO listas_preguntas (nombre, descripcion, activa, fecha_creacion)
            VALUES (?, ?, 1, ?)
            """,
            (question_set["nombre"], question_set["descripcion"], created_at),
        )
        set_id = int(cursor.lastrowid)

        items = []
        question_order = 1
        for orden in range(question_set["orden_inicio"], question_set["orden_fin"] + 1):
            items.append((set_id, order_to_id[orden], question_order))
            question_order += 1

        connection.executemany(
            """
            INSERT INTO lista_preguntas_items (lista_id, pregunta_id, question_order)
            VALUES (?, ?, ?)
            """,
            items,
        )


def clear_question_bank(connection) -> None:
    connection.execute("UPDATE partida_preguntas SET pregunta_id = NULL")
    connection.execute("DELETE FROM lista_preguntas_items")
    connection.execute("DELETE FROM listas_preguntas")
    connection.execute("DELETE FROM preguntas")


def seed_cartagena_water_bank(connection, *, replace: bool = False) -> bool:
    question_count = connection.execute("SELECT COUNT(*) FROM preguntas").fetchone()[0]
    if question_count > 0 and not replace:
        return False

    if replace:
        clear_question_bank(connection)

    order_to_id = _insert_questions(connection, PROJECT_QUESTIONS)
    _insert_question_sets(connection, order_to_id, QUESTION_SETS)
    return True


def seed_question_sets_if_missing(connection) -> None:
    existing_sets = connection.execute("SELECT COUNT(*) FROM listas_preguntas").fetchone()[0]
    if existing_sets > 0:
        return

    rows = connection.execute(
        "SELECT id, orden FROM preguntas ORDER BY orden ASC, id ASC"
    ).fetchall()
    order_to_id = {int(row["orden"]): int(row["id"]) for row in rows}
    _insert_question_sets(connection, order_to_id, QUESTION_SETS)
    _insert_question_sets(connection, order_to_id, QUESTION_SETS_EN)


def needs_cartagena_water_bank_migration(connection) -> bool:
    existing_list_names = {
        row["nombre"]
        for row in connection.execute("SELECT nombre FROM listas_preguntas").fetchall()
    }
    return not set(_NEW_BANK_MARKER_LIST_NAMES).issubset(existing_list_names)


def needs_english_water_bank_migration(connection) -> bool:
    existing_list_names = {
        row["nombre"]
        for row in connection.execute("SELECT nombre FROM listas_preguntas").fetchall()
    }
    return not set(_ENGLISH_BANK_MARKER_LIST_NAMES).issubset(existing_list_names)


def seed_english_water_bank(connection) -> bool:
    """Additively insert the English bank. Never touches existing rows --
    unlike seed_cartagena_water_bank, this has no `replace` option, because
    the Spanish bank must never be cleared when adding the English one.
    """
    order_to_id = _insert_questions(connection, PROJECT_QUESTIONS_EN)
    _insert_question_sets(connection, order_to_id, QUESTION_SETS_EN)
    return True
