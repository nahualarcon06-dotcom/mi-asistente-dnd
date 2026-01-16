import streamlit as st
import random
import webbrowser

# --- CONFIGURACIÓN DE ESTILO (Colores de tu código original) ---
COLOR_FONDO = "#121212"
COLOR_TARJETA = "#1E1E1E"
COLOR_DETALLE = "#B22222"
COLOR_TEXTO = "#DCDCDC"
COLOR_ORO = "#FFD700"

st.set_page_config(page_title="D&D ULTIMATE COMPANION 2026", layout="centered")

# Aplicar tus colores mediante CSS
st.markdown(f"""
    <style>
    .stApp {{ background-color: {COLOR_FONDO}; color: {COLOR_TEXTO}; }}
    .stButton>button {{ background-color: {COLOR_DETALLE}; color: white; border-radius: 10px; font-weight: bold; }}
    .stExpander {{ background-color: {COLOR_TARJETA}; border: none; }}
    .resultado-caja {{ 
        background-color: #000; 
        border: 1px solid {COLOR_ORO}; 
        padding: 20px; 
        border-radius: 5px; 
        font-family: 'Consolas', monospace; 
        color: {COLOR_ORO}; 
    }}
    </style>
    """, unsafe_allow_html=True)

# --- GESTIÓN DE DATOS (Equivalente a self.datos_personaje) ---
if 'pj' not in st.session_state:
    st.session_state.pj = {
        "nombre": "Viajero", "fuerza": 0, "destreza": 0,
        "raza": "No definida", "clase": "No definida",
        "alin": "No definido", "historia": "Sin historia registrada..."
    }
    st.session_state.pantalla = "inicio"
    st.session_state.resultado = "El destino aguarda tus tiradas..."

# --- PANTALLA 1: SETUP (Equivalente a setup_datos_pj) ---
if st.session_state.pantalla == "inicio":
    st.markdown(f"<h1 style='text-align: center; color: {COLOR_ORO}; font-family: Georgia;'>📜 FICHA DEL HÉROE</h1>", unsafe_allow_html=True)
    
    with st.container():
        nombre_in = st.text_input("Nombre del Personaje", placeholder="Nombre del Personaje")
        fuerza_in = st.text_input("Bono Fuerza (ej: 2)", placeholder="Bono Fuerza (ej: 2)")
        destreza_in = st.text_input("Bono Destreza (ej: 3)", placeholder="Bono Destreza (ej: 3)")
        
        if st.button("FORJAR DESTINO", use_container_width=True):
            try:
                st.session_state.pj["nombre"] = nombre_in if nombre_in else "Viajero"
                st.session_state.pj["fuerza"] = int(fuerza_in) if fuerza_in else 0
                st.session_state.pj["destreza"] = int(destreza_in) if destreza_in else 0
                st.session_state.pantalla = "main"
                st.rerun()
            except ValueError:
                st.error("¡Solo números en los bonos!")

# --- PANTALLA 2: INTERFAZ PRINCIPAL (Equivalente a main_gui) ---
else:
    st.markdown(f"<h1 style='text-align: center; color: {COLOR_ORO}; font-family: Georgia;'>⚔️ {st.session_state.pj['nombre'].upper()} ⚔️</h1>", unsafe_allow_html=True)
    
    # Mostrar Info actual
    texto_info = f"RAZA: {st.session_state.pj['raza']} | CLASE: {st.session_state.pj['clase']}  \nALINEAMIENTO: {st.session_state.pj['alin']}"
    st.markdown(f"<p style='text-align: center; font-style: italic; color: {COLOR_TEXTO};'>{texto_info}</p>", unsafe_allow_html=True)

    # Botones superiores
    col_ed, col_mu = st.columns(2)
    with col_ed:
        with st.popover("📝 Editar Ficha", use_container_width=True):
            st.markdown(f"<h3 style='color: {COLOR_ORO};'>DETALLES ÉPICOS</h3>", unsafe_allow_html=True)
            nueva_raza = st.text_input("Raza (ej: Elfo)", value=st.session_state.pj["raza"])
            nueva_clase = st.text_input("Clase (ej: Guerrero)", value=st.session_state.pj["clase"])
            nuevo_alin = st.text_input("Alineamiento (ej: Legal Bueno)", value=st.session_state.pj["alin"])
            nueva_hist = st.text_area("Historia", value=st.session_state.pj["historia"])
            if st.button("GUARDAR CAMBIOS"):
                st.session_state.pj.update({"raza": nueva_raza, "clase": nueva_clase, "alin": nuevo_alin, "historia": nueva_hist})
                st.rerun()
    with col_mu:
        # Nota: En web el audio automático está restringido, se pone un reproductor manual.
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3") # Ejemplo, puedes cambiar el link

    # Sección de Dados (Equivalente a frame_dados)
    st.markdown(f"<h3 style='color: {COLOR_DETALLE}; text-align: center;'>LANZAMIENTOS DE DADOS</h3>", unsafe_allow_html=True)
    
    cols = st.columns(5)
    dados = [("d20", 20), ("d12", 12), ("d10", 10), ("d8", 8), ("d6", 6)]
    
    for i, (n, c) in enumerate(dados):
        if cols[i].button(n, use_container_width=True):
            res = random.randint(1, c)
            msg = f"--- TIRADA {n} ---\nResultado Base: {res}\nTotal con FUERZA: {res + st.session_state.pj['fuerza']}\nTotal con DESTREZA: {res + st.session_state.pj['destreza']}"
            if c == 20 and res == 20: msg += "\n\n🔥 ¡CRÍTICO NATURAL! 🔥"
            st.session_state.resultado = msg

    if st.button("🔺 TIRAR d4 PIRAMIDAL", use_container_width=True):
        res = random.randint(1, 4)
        otros = [n for n in [1, 2, 3, 4] if n != res]
        random.shuffle(otros)
        st.session_state.resultado = f"      ▲\n     / {res} \\\n    / {otros[0]} {otros[1]} \\\n   /_______\\\n\nResultado: {res}"

    # Cuadro de resultados (Equivalente a res_frame)
    st.markdown(f"<pre class='resultado-caja'>{st.session_state.resultado}</pre>", unsafe_allow_html=True)

    # SECCIONES DE AYUDA (Texto original íntegro)
    def crear_ayuda(titulo, texto, url):
        with st.expander(titulo):
            st.write(texto)
            if url:
                st.link_button("▶️ Ver Video Tutorial", url)

    crear_ayuda("0. ¿QUÉ NECESITAS?", 
               "Para comenzar tu viaje en D&D necesitas tres pilares fundamentales:\n1. Imaginación y amigos (de 3 a 6 es ideal).\n2. Un set de datos poliédricos (d4, d6, d8, d10, d12, d20).\n3. Una hoja de personaje donde anotarás tus estadísticas y equipo.\n4. El Manual del Jugador o las Reglas Básicas impresas o en PDF.", None)

    crear_ayuda("2. ¿CÓMO JUGAR?", 
               "D&D se basa en una conversación constante. El DM describe una situación, tú dices qué quieres hacer y los dados deciden si lo logras. La fórmula básica es:\n[Tirada de d20] + [Tus Bonificadores] vs [Dificultad (CD)].\nSi el resultado es igual o mayor a la CD, ¡tienes éxito!", "https://youtu.be/ZBIcmhIhDig")

    crear_ayuda("4. SISTEMA DE COMBATE", 
               "El combate ocurre por turnos:\n1. Iniciativa: Se tira d20 + Destreza para ver quién actúa primero.\n2. Turno: En tu turno puedes realizar un Movimiento y una Acción (Atacar, Lanzar Hechizo, Ayudar).\n3. Ataque: Tiras d20 para superar la CA (Clase de Armadura) del enemigo.", "https://youtu.be/WyYJdUDyeWA")

    crear_ayuda("5. EL DUNGEON MASTER (DM)", 
               "El DM es el narrador, el arquitecto del mundo y el árbitro de las reglas. Su objetivo no es ganar a los jugadores, sino crear una historia épica juntos. Controla a los monstruos y a los personajes no jugadores (PNJs).", "https://youtu.be/TmiQXA3WiwU")

    if st.button("📖 ABRIR MANUAL PDF COMPLETO", use_container_width=True):
        webbrowser.open("https://media.wizards.com/2023/downloads/dnd/SRD_CC_v5.1_ES.pdf")