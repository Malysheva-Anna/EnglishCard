import streamlit as st

from application.user_service import get_or_create_user
from application.word_service import get_random_word
from application.word_service import get_answer_options
from application.word_service import add_word
from application.word_service import delete_word
from application.word_service import get_user_words


st.set_page_config(page_title='EnglishCard')

st.title('EnglishCard')
st.write('Привет! Давай учить английские слова.')


if 'user_id' not in st.session_state:
    st.session_state.user_id = None

if 'username' not in st.session_state:
    st.session_state.username = None

if 'current_word' not in st.session_state:
    st.session_state.current_word = None

if 'options' not in st.session_state:
    st.session_state.options = []

if 'answered' not in st.session_state:
    st.session_state.answered = False

if 'answer_message' not in st.session_state:
    st.session_state.answer_message = ''

if 'attempts' not in st.session_state:
    st.session_state.attempts = 0

if 'finished' not in st.session_state:
    st.session_state.finished = False


if st.session_state.user_id is None:
    with st.form('login_form'):
        username = st.text_input('Введи своё имя')

        submitted = st.form_submit_button('Войти')

        if submitted:
            if username.strip():
                user_id = get_or_create_user(username.strip())

                st.session_state.user_id = user_id
                st.session_state.username = username.strip()

                st.rerun()
            else:
                st.error('Пожалуйста, введи имя.')


else:
    st.success(
        f'С возвращением, {st.session_state.username}!'
    )

    if st.button('Выйти'):
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.current_word = None
        st.session_state.options = []
        st.session_state.answered = False
        st.session_state.answer_message = ''
        st.session_state.attempts = 0
        st.session_state.finished = False

        st.rerun()

    with st.expander('Добавить своё слово'):
        with st.form('add_word_form'):
            english_word = st.text_input(
                'Английское слово'
            )

            russian_translation = st.text_input(
                'Перевод на русский'
            )

            submitted = st.form_submit_button(
                'Добавить слово'
            )

            if submitted:
                if english_word.strip() and russian_translation.strip():
                    add_word(
                        st.session_state.user_id,
                        english_word.strip(),
                        russian_translation.strip()
                    )

                    st.success('Слово успешно добавлено!')
                else:
                    st.error('Заполни оба поля.')

    with st.expander('Удалить своё слово'):
        user_words = get_user_words(
            st.session_state.user_id
        )

        words_dict = {
            f'{word[1]} — {word[2]}': word[0]
            for word in user_words
        }

        if words_dict:
            selected_word = st.selectbox(
                'Выбери слово для удаления',
                options=list(words_dict.keys())
            )

            if st.button('Удалить слово'):
                delete_word(
                    st.session_state.user_id,
                    words_dict[selected_word]
                )

                st.success('Слово удалено из твоего списка!')
                st.rerun()
        else:
            st.write('У тебя пока нет слов.')

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

        if not st.session_state.finished:
            for option in st.session_state.options:
                if st.button(option):
                    if option == word[1]:
                        st.session_state.answered = True
                        st.session_state.finished = True
                        st.session_state.answer_message = (
                            'Правильно!'
                        )
                    else:
                        st.session_state.attempts += 1

                        if st.session_state.attempts >= 2:
                            st.session_state.finished = True
                            st.session_state.answered = False

                            st.session_state.answer_message = (
                                f'Попытки закончились. '
                                f'Правильный ответ: {word[1]}'
                            )
                        else:
                            st.session_state.answer_message = (
                                'Неправильно! Попробуй ещё раз.'
                            )

        if st.session_state.answer_message:
            if st.session_state.answered:
                st.success(
                    st.session_state.answer_message
                )
            elif st.session_state.finished:
                st.error(
                    st.session_state.answer_message
                )
            else:
                st.warning(
                    st.session_state.answer_message
                )

        if st.session_state.finished:
            if st.button('Следующее слово'):
                st.session_state.current_word = None
                st.session_state.options = []
                st.session_state.answered = False
                st.session_state.answer_message = ''
                st.session_state.attempts = 0
                st.session_state.finished = False

                st.rerun()