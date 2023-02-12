import requests
from bs4 import BeautifulSoup
import CONFIG
import datetime


def write_dnevnik_parse_results():
    today = datetime.datetime.today()
    ThisWeekStarsFromDate = datetime.datetime.now().strftime(f"{today.day - today.weekday()}.%m.%Y")

    # LOG IN START
    user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' \
                     ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'

    LOGIN_URL = 'https://login.dnevnik.ru/login'
    CHEDULES_URL = f'https://dnevnik.ru/currentprogress/result/1000021717462/1000011419657/2022/{ThisWeekStarsFromDate}?userComeFromSelector=True'

    session = requests.Session()
    r = session.get(LOGIN_URL, headers={
        'User-Agent': user_agent_val
    })

    session.headers.update({'Referer': LOGIN_URL})
    session.headers.update({'User-Agent': user_agent_val})
    session.headers.update({'User-Agent': user_agent_val})
    _xsrf = session.cookies.get('_xsrf', domain='.dnevnik.ru')

    post_request = session.post(LOGIN_URL, {
        'backUrl': 'https://dnevnik.ru/',
        'login': f'{CONFIG.DN_RU_LOG}',
        'password': f'{CONFIG.DN_RU_PAS}',
        '_xsrf': _xsrf,
        'remember': 'yes',
    })
    # LOG IN END

    request_result = session.get(CHEDULES_URL)

    # write results
    with open("chedules_content_succes.html", "w") as file:
        file.write(request_result.text)


def get_schedules_from_dnevnik_html(offset=1):
    with open('chedules_content_succes.html') as file:
        dnevnik_html = file.read().encode('UTF8')

    soup = BeautifulSoup(dnevnik_html, 'lxml')
    schedule = soup.find_all('li', class_='current-progress-schedule__item')

    if len(schedule) == 0:
        return 'RESULTS DO NOT FOUND'

    # {'пн': 0, 'вт': 1, 'ср': 2, 'чт': 3, 'пт': 4, 'сб': 5, 'вс': 6}
    lessons_today = schedule[datetime.date.today().weekday() + offset].text.capitalize()

    return lessons_today


def add_date_to_text(text, to_start=False, to_end=False, offset=0):
    date_pattern = '%d-%m-%Y'
    date = datetime.date.today() + datetime.timedelta(days=offset)
    new_date = str(text)

    if to_start:
        new_date = date.strftime(date_pattern) + '\n' + new_date

    if to_end:
        new_date = new_date + '\n' + date.strftime(date_pattern)

    return new_date


write_dnevnik_parse_results()
