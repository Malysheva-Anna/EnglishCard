import streamlit as st

from application.word_service import get_random_word
from application.user_service import get_or_create_user
from application.word_service import get_answer_options


st.set_page_config(page_title='EnglishCard')

st.title('EnglishCard')
st.write('Привет! Давай учить английские слова.')

if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'current_word' not in st.session_state:
    st.session_state.current_word = None

if 'options' not in st.session_state:
    st.session_state.options = []

if 'answered' not in st.session_state:
    st.session_state.answered = False

if 'answer_message' not in st.session_state:
    st.session_state.answer_message = ''

if st.session_state.user_id is None:
    username = st.text_input('Введи своё имя')

    if st.button('Войти'):
        if username.strip():
            user_id = get_or_create_user(username.strip())
            st.session_state.user_id = user_id
            st.session_state.username = username.strip()
        else:
            st.error('Пожалуйста, введи имя.')

else:
    st.success(
        f'С возвращением, {st.session_state.username}!'
    )

    if st.session_state.current_word is None:
        st.session_state.current_word = get_random_word(
            st.session_state.user_id
        )
        st.session_state.options = get_answer_options(
            st.session_state.user_id,
            st.session_state.current_word[0]
        )

    if st.session_state.current_word:
        word = st.session_state.current_word

        st.subheader('Переведи слово:')
        st.title(word[2])

        for option in st.session_state.options:
            if st.button(option):
                if option == word[1]:
                    st.session_state.answered = True
                    st.session_state.answer_message = 'Правильно!'
                else:
                    st.session_state.answer_message = (
                        'Неправильно! Попробуй ещё раз.'
                    )

        if st.session_state.answer_message:
            if st.session_state.answered:
                st.success(st.session_state.answer_message)
            else:
                st.error(st.session_state.answer_message)

        if st.session_state.answered:
            if st.button('Следующее слово'):
                st.session_state.current_word = None
                st.session_state.options = []
                st.session_state.answered = False
                st.session_state.answer_message = ''
                st.rerun()