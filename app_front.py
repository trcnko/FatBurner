import requests
from datetime import date
import streamlit as st

from styles import CUSTOM_CSS

BACKEND_URL = 'http://194.87.74.105:8000'
# BACKEND_URL = 'http://localhost:8000'
# BACKEND_URL = 'http://backend:8000'

st.markdown(CUSTOM_CSS,
    unsafe_allow_html=True
)


if "recipe_ingredients" not in st.session_state:
    st.session_state["recipe_ingredients"] = []

st.title('FatBurner ₊˚⊹♡\n🍰🍔🧁🍡🧃🍠🧀🥧🍫🍨🍕🥞🧇🫐🍒🥐')
st.markdown(
    """
    ### Чем тут можно заняться? („•֊•„)
    * 🍝 **Вести дневник** — записывать порции съеденного за день
    * 🍕 **Расширять базу** — добавлять новые продукты и их КБЖУ на 100 г
    * 🥘 **Собирать целые блюда** — рассчитывать итоговую калорийность сложных рецептов на 100 г
    
    ###### *только не забудьте авторизоваться (←_←)*
    ---
    """
)


with st.sidebar:
    st.title('Управление профилем (^-^*)/')
    user_name = st.text_input('Введите свой никнейм', key='input_user_name')
    is_new_user = st.checkbox('(•⩊•) Я новый пользователь (Регистрация)', key='reg_checkbox')

    if not is_new_user:
        if st.button('Войти ⚷', use_container_width=True, key='btn_login'):
            if user_name:
                response = requests.get(
                    url=f'{BACKEND_URL}/users/{user_name}/stats',
                    params={'date_query': str(date.today())}
                )
                if response.status_code == 200:
                    st.session_state['user_name'] = user_name
                    st.success('Добро пожаловать (*^ω^)')
                else:
                    st.session_state['user_name'] = ''
                    st.error('Никнейм не найден (｡•́︿•̀｡)')
            else:
                st.warning('Введите никнейм Σ(°ロ°)!!!')
    else:
        target_calories = st.number_input('Цель калорий на день ૮˶ᵔᵕᵔ˶ა', key='sidebar_target', min_value=0, value=0, format="%d")
        if st.button('Создать профиль ✍', use_container_width=True, key='btn_reg'):
            if user_name:
                payload = {
                    "name": user_name,
                    "daily_target": target_calories
                }
                response = requests.post(url=f'{BACKEND_URL}/users', json=payload)
                if response.status_code in [200, 201]:
                    st.session_state['user_name'] = user_name
                    st.success(f"Профиль '{user_name}' создан (*^ω^)")
                elif response.status_code == 400:
                    st.error("Этот никнейм уже занят (｡•́︿•̀｡)")
            else:
                st.warning("Введите никнейм для регистрации Σ(°ロ°)!!!")

    st.markdown('---')
    user_name1 = st.session_state.get('user_name', '')
    if user_name1:
        st.markdown(f"**Авторизован:** `{user_name1}`")
    else:
        st.markdown("**Вход не выполнен**")


tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Дневник ",
    "🍝 Записать прием пищи ",
    "🍕 Добавить новый продукт ",
    '🥘 Добавить своё блюдо '
])


with tab1:
    date_query = st.date_input('Выберите дату', date.today(), key='tab1_date_input')

    current_user = st.session_state.get('user_name', '')

    if current_user:
        response = requests.get(url=f'{BACKEND_URL}/users/{current_user}/stats', params={'date_query': str(date_query)})

        if response.status_code in [200, 201]:
            data = response.json()

            st.write(f"#### ヾ(・ω・)メ(・ω・)ノ\n #### Привет, {data['user_name']}! Ваш отчет за {data['date']}:")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(label="😋 Уже съедено", value=f"{int(data['total_eaten']['ККалории'])} ккал")
            with col2:
                st.metric(label="😬 Осталось доесть", value=f"{int(data['remains'])} ккал")
            with col3:
                st.metric(label="😉 Твоя цель на день", value=f"{int(data['daily_target'])} ккал")

            st.write("**БЖУ:**")
            st.write(f"🍗 Белки: {round(data['total_eaten']['Белки'], 1)} г | 🥑 Жиры: {round(data['total_eaten']['Жиры'], 1)} г | 🍌 Углеводы: {round(data['total_eaten']['Углеводы'], 1)} г")
            st.write('#### История питания за день: ')
            if data['meals_history']:
                st.dataframe(data['meals_history'], use_container_width=True)

                if 'show_delete_menu' not in st.session_state:
                    st.session_state.show_delete_menu = False

                if st.button('Удалить блюдо из дневника 🗑️'):
                    st.session_state.show_delete_menu = True
                    st.rerun()

                if st.session_state.show_delete_menu:
                    options = {}
                    for m in data['meals_history']:
                        label = f"{m['Продукт']} ({m['Калории, ккал']} ккал)"
                        options[label] = m['id']

                    selected_label = st.selectbox("Выберите, какое блюдо нужно стереть (゜_゜;)", options=list(options.keys()))
                    col_del, col_can = st.columns(2)

                    with col_del:
                        if st.button("Стереть", type="primary"):
                            meal_id_to_delete = options[selected_label]
                            del_resp = requests.delete(f"{BACKEND_URL}/meals/{meal_id_to_delete}")

                            if del_resp.status_code == 200:
                                st.session_state.show_delete_menu = False
                                st.rerun()
                            else:
                                st.error("(╥﹏╥) Не удалось удалить блюдо на сервере")

                    with col_can:
                        if st.button("Отмена (〃￣ω￣)"):
                            st.session_state.show_delete_menu = False
                            st.rerun()

            else:
                st.error('В этот день Вы еще ничего не кушали (◕‿◕)♡')
        else:
            st.error("Пользователь не найден на бэкенде!")
    else:
        st.warning("(←_←) Войдите в профиль, чтобы увидеть свой дневник питания!")


with tab3:
    product_name = st.text_input("Название продукта", key='prod_name_tab2')
    calories = st.number_input('Калории на 100г', min_value=0, value=0, format="%d", key='cal_tab2')
    proteins = st.number_input('Белки на 100г', min_value=0.0, value=0.0, format='%.1f', key='prot_tab2')
    fats = st.number_input('Жиры на 100г', min_value=0.0, value=0.0, format='%.1f', key='fats_tab2')
    carbs = st.number_input('Углеводы на 100г', min_value=0.0, value=0.0, format='%.1f', key='carbs_tab2')

    if st.button("Сохранить продукт", key='save_prod_btn'):
        if not product_name:
            st.error('Введите название продукта Σ(°ロ°)!!!')
        elif not st.session_state.get('user_name', ''):
            st.error(f"(←_←) Войдите в профиль")
        else:
            payload = {
                "name": product_name,
                "calories": calories,
                "proteins": proteins,
                "fats": fats,
                "carbs": carbs
            }
            response = requests.post(url=f'{BACKEND_URL}/products', json=payload)
            if response.status_code in [201, 200]:
                st.success(f"Продукт '{product_name}' успешно сохранен в общую базу (◕‿◕)♡")
            else:
                st.error(f"Ошибка сервера ({response.status_code}) (｡•́︿•̀O\)")


with tab2:
    prod_response = requests.get(url=f'{BACKEND_URL}/products')
    prod_list = prod_response.json()

    if prod_list:
        products_dict = {p['name']: p['product_id'] for p in prod_list}
        meal_date = st.date_input('Дата', date.today())
        selected_prod_name = st.selectbox("Выберите продукт из базы", options=list(products_dict.keys()))
        grams = st.number_input('Граммы', min_value=0, value=0, format='%d')

        if st.button('Записать'):
            current_user = st.session_state.get('user_name', '')
            if not current_user:
                st.error('(←_←) Войдите в профиль')
            else:
                chosen_id = products_dict[selected_prod_name]
                payload = {
                    "user_name": current_user,
                    "product_id": chosen_id,
                    "grams": grams,
                    "date": str(meal_date)
                }

                response = requests.post(url=f'{BACKEND_URL}/meals', json=payload)
                if response.status_code in [200, 201]:
                    st.success("Прием пищи записан в Ваш дневник! 𓎩")
                    st.rerun()
                else:
                    # st.error(f"статус-код: {response.status_code}")
                    st.error(f"(←_←) Войдите в профиль")
    else:
        st.write('В базе данных пока нет ни одного продукта! =(')


with tab4:
    st.write('##### ‧₊˚⋅𓐐𓎩‧₊˚ ⋅ Расчет КБЖУ собственного блюда')

    recipe_name = st.text_input("Название готового блюда", key="recipe_name_input")

    prod_response = requests.get(url=f'{BACKEND_URL}/products')
    prod_list = prod_response.json()

    if prod_list:
        products_dict = {p['name']: p['product_id'] for p in prod_list}
        selected_prod_name = st.selectbox("Выберите продукт из базы", options=list(products_dict.keys()), key='recipe_selectbox')
        grams = st.number_input('Граммы', min_value=0, value=0, format='%d', key='recipe_grams_input')

        if st.button('Добавить ингредиент в рецепт'):
            current_product = None
            for p in prod_list:
                if p['name'] == selected_prod_name:
                    current_product = p
                    break

            ing_calories = current_product['calories'] * grams * 0.01
            ing_proteins = current_product['proteins'] * grams * 0.01
            ing_fats = current_product['fats'] * grams * 0.01
            ing_carbs = current_product['carbs'] * grams * 0.01

            ing_data = {
                'name': selected_prod_name,
                'weight': grams,
                'calories': ing_calories,
                'proteins': ing_proteins,
                'fats': ing_fats,
                'carbs': ing_carbs
            }

            st.session_state['recipe_ingredients'].append(ing_data)
            st.write(f'Добавлен ингредиент "{selected_prod_name}" - {grams} г')

        if st.session_state["recipe_ingredients"]:
            st.write("##### ୧ ‧₊˚ 𓐐⋅ Текущие ингредиенты в блюде:")
            for ing in st.session_state["recipe_ingredients"]:
                st.write(f"₊˚⊹⋆ {ing['name']}: {ing['weight']} г")

        if st.button('Рассчитать итоговое КБЖУ блюда'):
            total_weight = 0
            total_cal = 0
            total_prot = 0
            total_fats = 0
            total_carbs = 0

            for i in st.session_state['recipe_ingredients']:
                total_weight += i['weight']
                total_cal += i['calories']
                total_prot += i['proteins']
                total_fats += i['fats']
                total_carbs += i['carbs']

            if not recipe_name:
                st.error('Введите название продукта (×﹏×)')

            elif not st.session_state.get('user_name', ''):
                st.error("(←_←) Войдите в профиль!")

            elif total_weight == 0:
                st.error("Вес блюда равен 0 грамм! Сначала добавь ингредиенты ┐('～`;)┌")

            else:
                final_cal = (total_cal / total_weight) * 100
                final_prot = (total_prot / total_weight) * 100
                final_fats = (total_fats / total_weight) * 100
                final_carbs = (total_carbs / total_weight) * 100

                st.write(f"##### Результат расчета на 100 г готового блюда:")
                st.write(f"🧬 **Калорийность:** {round(final_cal)} ккал")
                st.write(f"🍗 **Белки:** {round(final_prot, 1)} г | 🥑 **Жиры:** {round(final_fats, 1)} г | 🍌 **Углеводы:** {round(final_carbs, 1)} г")
                st.write(f"⚖️ *Общий вес готового блюда: {total_weight} г*")

                payload = {
                    "name": recipe_name,
                    "calories": final_cal,
                    "proteins": final_prot,
                    "fats": final_fats,
                    "carbs": final_carbs
                }
                response = requests.post(url=f'{BACKEND_URL}/products', json=payload)
                if response.status_code in [201, 200]:
                    st.success("Блюдо занесено (´｡•ᵕ•｡`) ♡")
                    st.session_state['recipe_ingredients'] = []
                else:
                    st.error(f"Ошибка сервера ({response.status_code}) (｡•́︿•̀｡)")

        if st.button('🧹 Очистить рецепт'):
            st.session_state['recipe_ingredients'] = []
            st.success("𓎩 Миска пуста, можно собирать новое блюдо!")