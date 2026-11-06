import streamlit as st

from application.user_service import get_or_create_user
from application.word_service import get_random_word
from application.word_service import get_answer_options
from application.word_service import add_word
from application.word_service import delete_word
from application.word_service import get_user_words


st.set_page_config(
    page_title='EnglishCard',
    page_icon='📚',
    layout='wide'
)


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


st.title('EnglishCard')

if st.session_state.user_id is None:
    st.caption('Смотря какой fabric, смотря сколько details')
    st.subheader('Войди или зарегистрируйся')

    username = st.text_input('Введи своё имя')

    if st.button('Начать'):
        if username.strip():
            st.session_state.username = username.strip()
            st.session_state.user_id = get_or_create_user(
                st.session_state.username
            )
            st.rerun()
        else:
            st.warning('Введи имя')


else:

    left_col, right_col = st.columns(
        [1, 2.5],
        gap='large'
    )

    with left_col:

        st.subheader(
            f'Привет, {st.session_state.username}!'
        )

        if st.button(
            'Выйти',
            use_container_width=True
        ):
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.current_word = None
            st.session_state.options = []
            st.session_state.answered = False
            st.session_state.answer_message = ''
            st.session_state.attempts = 0
            st.session_state.finished = False

            st.rerun()

        st.divider()

        user_words = get_user_words(
            st.session_state.user_id
        )

        st.metric(
            'Всего слов в словаре',
            len(user_words)
        )

        st.divider()

        st.subheader('Кастомизируй свой словарь')

        with st.expander('➕ Добавить слово'):

            with st.form('add_word_form'):

                english_word = st.text_input(
                    'Английское слово'
                )

                russian_translation = st.text_input(
                    'Перевод на русский'
                )

                submitted = st.form_submit_button(
                    'Добавить',
                    use_container_width=True
                )

                if submitted:

                    if (
                        english_word.strip()
                        and russian_translation.strip()
                    ):
                        add_word(
                            st.session_state.user_id,
                            english_word.strip(),
                            russian_translation.strip()
                        )

                        st.success('Слово добавлено!')
                        st.rerun()

                    else:
                        st.error('Заполни оба поля.')

        with st.expander('🗑️ Удалить слово'):

            words_dict = {
                f'{word[1]} — {word[2]}': word[0]
                for word in user_words
            }

            if words_dict:

                selected_word = st.selectbox(
                    'Выбери слово',
                    options=list(words_dict.keys())
                )

                if st.button(
                    'Удалить',
                    use_container_width=True
                ):
                    delete_word(
                        st.session_state.user_id,
                        words_dict[selected_word]
                    )

                    st.session_state.current_word = None
                    st.session_state.options = []
                    st.session_state.answered = False
                    st.session_state.answer_message = ''
                    st.session_state.attempts = 0
                    st.session_state.finished = False

                    st.rerun()

            else:
                st.write('В твоем словаре пока нет слов.')

    with right_col:

        st.subheader('Тренировка')

        if len(user_words) < 4:

            st.warning(
                'Для тренировки необходимо минимум 4 слова. '
                'Добавь больше слов в свой словарь.'
            )

        else:

            if st.session_state.current_word is None:

                st.session_state.current_word = get_random_word(
                    st.session_state.user_id
                )

                if st.session_state.current_word:

                    st.session_state.options = get_answer_options(
                        st.session_state.user_id,
                        st.session_state.current_word[0]
                    )

            if st.session_state.current_word:

                word = st.session_state.current_word

                with st.container(border=True):

                    st.title(word[2])

                    if not st.session_state.finished:

                        st.caption(
                            f'Попытка '
                            f'{min(st.session_state.attempts + 1, 2)} из 2'
                        )

                    else:
                        st.caption('Ответ завершен')

                    st.divider()

                    if not st.session_state.finished:

                        answer_cols = st.columns(2)

                        for index, option in enumerate(
                            st.session_state.options
                        ):

                            with answer_cols[index % 2]:

                                if st.button(
                                    option,
                                    key=f'answer_{index}',
                                    use_container_width=True
                                ):

                                    if option == word[1]:

                                        st.session_state.answered = True
                                        st.session_state.finished = True

                                        st.session_state.answer_message = (
                                            'Верно! Отличная работа!'
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
                                                'Неправильно, попробуй еще раз.'
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

                        if st.button(
                            'Следующее слово →',
                            use_container_width=True
                        ):

                            st.session_state.current_word = None
                            st.session_state.options = []
                            st.session_state.answered = False
                            st.session_state.answer_message = ''
                            st.session_state.attempts = 0
                            st.session_state.finished = False

                            st.rerun()