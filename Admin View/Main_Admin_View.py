import streamlit as st
from streamlit_navigation_bar import st_navbar
import Data_Loading_Root
import Feedback_Analysis_Root
import Model_Evaluation_Root
import Model_Training_Root
import Data_Preview_Root

# Header-Werte mit Übersetzungen
translations_main = {
    0: ["Language", "Sprache", "Lingua", "Langue", "Idioma", "Idioma", "Språk", "Språk", "Sprog", "Język", "Язык",
        "Мова"],
    1: ["Data Loading", "Datenladen", "Caricamento dati", "Chargement des données", "Carga de datos", "Carregamento de dados", "Datainläsning", "Datainnhenting", "Dataindlæsning", "Ładowanie danych", "Загрузка данных", "Завантаження даних"],
    2: ["Data Preview", "Datenvorschau", "Anteprima dei dati", "Aperçu des données", "Vista previa de datos", "Pré-visualização de dados", "Dataförhandsgranskning", "Datavisning", "Datavisning", "Podgląd danych", "Предпросмотр данных", "Попередній перегляд даних"],
    3: ["Model-Training", "Modelltraining", "Addestramento del modello", "Entraînement du modèle", "Entrenamiento del modelo", "Treinamento do modelo", "Modellträning", "Modelltrening", "Modelltræning", "Trenowanie modelu", "Обучение модели", "Навчання моделі"],
    4: ["Model-Evaluation", "Modellbewertung", "Valutazione del modello", "Évaluation du modèle", "Evaluación del modelo", "Avaliação do modelo", "Modellevaluering", "Modellvurdering", "Modellevaluering", "Ocena modelu", "Оценка модели", "Оцінювання моделі"],
    5: ["Feedback Analyse", "Feedback-Analyse", "Analisi del feedback", "Analyse des retours", "Análisis de comentarios", "Análise de feedback", "Feedback-analys", "Tilbakemeldingsanalyse", "Feedback-analyse", "Analiza opinii", "Анализ отзывов", "Аналіз зворотного зв'язку"],

}


# Mache die Seite so breit wie möglich
st.set_page_config(page_title="OptiModuls (Admin)", layout="wide")

st.markdown(
    """
    <style>
    /*Side bar*/
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
        width: 100%;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
        width: 350px;
        margin-left: -400px;
    }

    """,
    unsafe_allow_html=True,
)

# Speichere die Sprache in der Session
if 'language_index' not in st.session_state:
    st.session_state.language_index = 0

language_index = st.session_state.language_index

if 'language_value' not in st.session_state:
    st.session_state.language_value = 'English'

language_value = st.session_state.language_value


if 'top_nav_value' not in st.session_state:
    st.session_state.top_nav_value = translations_main.get(1)[language_index]

top_nav_value = st.session_state.top_nav_value

# Mach die Frabge von allen Text schwarz
# Define the CSS style for text color
st.markdown("""
    <style>
    /* Change text color of all elements */
    * {
        



    }
    </style>
    """, unsafe_allow_html=True)

# Side bar link Styling
st.markdown("""
    <style>
    .st-emotion-cache-6qob1r {
    background-color: #f3f5e9 !important;
    }   
    </style>
    """, unsafe_allow_html=True)

styles = {
    "nav": {
        "background-color": "#f3f5e9",
        "height": "3.25rem",

    },
    "div": {
        "max-width": "85.25rem",
        "font-size": "20px",
        "font-size": "20px",
        "padding": "1rem",

    },
    "span": {
        "color": "var(--text-color)",
        "border-radius": "0.3rem",
        "padding": "1rem",

    },
    "active": {
        "background-color": "#f7e48f",
        "padding": "1rem"
    },
    "hover": {
        "background-color": "#D3D3D3",
    },
}

options = {
    "show_menu": False,
    "show_sidebar": False,
}

# Header Werte in der ausgewählten Sprache
pages = [
        f'{translations_main.get(1)[language_index]}',
        f'{translations_main.get(2)[language_index]}',
        f'{translations_main.get(3)[language_index]}',
        f'{translations_main.get(4)[language_index]}',
        f'{translations_main.get(5)[language_index]}'

         ]



# Suche den Index des ausgewählten Begriffs in den Übersetzungen
def return_selected_page_translated(selected_term, target_language_index):
    for key, value in translations_main.items():
        if selected_term in value:
            return value[target_language_index]


selected_page_transalted = return_selected_page_translated(top_nav_value, language_index)

navigation_bar_top = st_navbar(pages=pages,
                               styles=styles,
                               options=options,
                               selected=selected_page_transalted)

############

# berechne den Index der ausgewählten Sprache
language_dict = {
    'English': 0,
    'Deutsch': 1,
    'Italiano': 2,
    'Français': 3,
    'Español': 4,
    'Português': 5,
    'Svenska': 6,
    'Norsk': 7,
    'Dansk': 8,
    'Polski': 9,
    'Русский': 10,
    'українська': 11

}

# Deine Styles hier
options = list(language_dict.keys())



# Navigationsleiste erstellen
logo_column, text_language_column, drop_down_language_column= st.columns([12.5,1,1.4])
with logo_column:

    # Logo
    hover_style = """
        <style>
        .logo {
            transition: opacity 0.8s ease;
            animation: skalieren 1s infinite linear;
        }
        @keyframes skalieren {
                0% {
        transform: scale(1, 1);
      }
      50% {
        transform: scale(1.1, 1.1);
      }
      100% {
        transform: scale(1, 1);
      }
        }

        </style>
    """

    # Apply the custom CSS
    st.markdown(hover_style, unsafe_allow_html=True)

    st.markdown(
        '<div style="text-align: left;"><img src="https://i.postimg.cc/sgD9f7JH/Opti-Moduls.png" class="logo" width="100"></div>',
        unsafe_allow_html=True
    )


with text_language_column:
    st.write('')
    st.write('')
    st.write(f'**{translations_main.get(0)[language_index]}:** ')

with drop_down_language_column:
    selected_language = st.selectbox('',
                                     options=options)



# Session State überprüfen und neu laden
if 'language_index' not in st.session_state:
    st.session_state.language_index = language_dict.get(selected_language)

if st.session_state.language_index != language_dict.get(selected_language):
    st.session_state.language_index = language_dict.get(selected_language)
    st.experimental_rerun()


# Session State (language_value) überprüfen und neu laden
if 'language_value' not in st.session_state:
    st.session_state.language_value = selected_language

if st.session_state.language_value != selected_language:
    st.session_state.language_value = selected_language
    st.experimental_rerun()

# Session State (top_nav_value) überprüfen und neu laden
if 'top_nav_value' not in st.session_state:
    st.session_state.top_nav_value = str(navigation_bar_top)

if st.session_state.top_nav_value != str(navigation_bar_top):
    st.session_state.top_nav_value = str(navigation_bar_top)
    st.experimental_rerun()



# "Data Loading"
if navigation_bar_top == f'{translations_main.get(1)[language_index]}':
    Data_Loading_Root.run_data_loading_root(language_index,
                                  f'{translations_main.get(1)[language_index]}')

# "Data Preview"
if navigation_bar_top == f'{translations_main.get(2)[language_index]}':
    Data_Preview_Root.run_data_preview_root(language_index,
                                  f'{translations_main.get(2)[language_index]}')

# "Model Training"
if navigation_bar_top == f'{translations_main.get(3)[language_index]}':
    Model_Training_Root.run_model_training_root(language_index,
                                      f'{translations_main.get(3)[language_index]}')


# "Model Evaluation"
if navigation_bar_top == f'{translations_main.get(4)[language_index]}':
    Model_Evaluation_Root.run_model_evaluation_root(language_index,
                                          f'{translations_main.get(4)[language_index]}')

# "Feedback Analysis"
if navigation_bar_top == f'{translations_main.get(5)[language_index]}':
    Feedback_Analysis_Root.run_feedback_analysis_root(language_index,
                                            f'{translations_main.get(5)[language_index]}')






