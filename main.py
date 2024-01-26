import logging
import asyncio
import datetime
from aiogram import Bot, Dispatcher, executor, types
from buttons import *
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import re
import io
import requests
import sqlite3
import os
from aiogram.types import CallbackQuery

API_TOKEN = "6293716593:AAH8dR8RNDf6Sv67Bjo9aPwla7zXb8-ihqk"

api_url = 'http://5.182.26.180:55565/telegram/hs/hl/gd'
login = 'Hilol'
password = '0ut0fb0unD'

headers = {
            'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }
conn = sqlite3.connect('Baza_User.db')
sql = conn.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS User(chat_id, tel_nomer)""")
conn.commit()

class Input(StatesGroup):
    sery = State()
    end_time = State()
    contracts = State()

class TimeInput(StatesGroup):
    start_time = State()
    end_time = State()

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot,storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    chat_id = message.from_user.id
    uses = (sql.execute("""SELECT * FROM User"""))
    users = uses.fetchall()
    conn.commit()
    for user in users:
        if user[0] == chat_id:
            await message.answer("Botga xush kelibsiz!", reply_markup=user_uz)
    await message.reply("Tilni tanlang\n\nВыберите язык\n\nSelect language", reply_markup=lang)



@dp.message_handler(text = "🇺🇿 O'zbek tili")
async def uzb(message: types.Message):
    global lan
    lan = message.text
    params = {
        'type':"comment"
    }
    try:
        response = requests.get(api_url, params=params, headers=headers)
        if response.ok:
            if 'application/json' in response.headers.get('Content-Type', ''):
                data = response.json()
                result = response.text
            
            else:
                result = f"Response is not in JSON format: {response.text}"
        else:
            result = f"Request failed with status code {response.status_code}: {response.reason}"
        await message.answer(f"{data.get('UZ')}"+"\nIdentifikatsiyadan o’tish uchun telefon raqamingizni ulashing.", reply_markup=contact_uz)

    except requests.exceptions.RequestException as e:
        result = f"Request failed: {e}"
        await message.answer(f"sizdagi xatolik{result}")


#mana biror narsa commentdagi
#gitni to'g'rilash
#cheking

    @dp.message_handler(content_types=types.ContentType.CONTACT)
    async def uzb_baza(message: types.Message):
        global phone_number, chat_id
        phone_number = message.contact.phone_number
        chat_id =  message.from_user.id
        params = {
            'type': 'phone',
             'chat_id': chat_id,
            'phone_number': phone_number,
            'language':lan
        }
        try:
            response = requests.get(api_url, params=params, headers=headers)
            if response.ok:
                if 'application/json' in response.headers.get('Content-Type', ''):
                    data = response.json()
                    p = data.get("UZ")
                    if p is not None:
                        result = response.text
                        sql.execute("""INSERT INTO User(chat_id, tel_nomer) VALUES (?,?,?)""", (chat_id, phone_number))
                        conn.commit()
                        await message.answer(f"{p}", reply_markup=user_uz)
                    else:
                        await message.answer(f"Uzr xurmatli mijoz siz haqingizda ma'lumot topilmadi.\nAdminlarimizga murojaat etishingizni so'rab qolamiz|@pm_hilol", reply_markup=start_t)
                else:
                    result = f"Response is not in JSON format: {response.text}"
            else:
                result = f"Request failed with status code {response.status_code}: {response.reason}"
            # await message.answer(f"{data.get('UZ')}", reply_markup=user_uz)

        except requests.exceptions.RequestException as e:
            result = f"Request failed: {e}"
            await message.answer(f"{data.get('UZ')}")



    @dp.message_handler(text="Qarzdorlikni tekshirish") 
    async def tel1(message: types.Message):
        params = {
            "type": "debt",
            "chat_id": message.from_user.id
        }
        response = requests.get(api_url, params=params, headers=headers)
        global ta
        ta = {}
        if response:
            data = response.json()
            summ = data['allsumm']
            val = data['currency']
            for i in range(len(data['contracts'])):
                    contract_id = data['contracts'][i]['contract']
                    contractsumm = data['contracts'][i]['contractsumm']
                    contractcurrency = data['contracts'][i]['contractcurrency']
                    contractekvivalent = data['contracts'][i]['contractekvivalent']
            if contractsumm is not None:
                message_text = f"Sizning jammi qarzdorligingiz: {summ} {val},\n va ushbu {contract_id}-shartnomasi bo'yicha ma'lumotlar:\n{contractsumm} {contractcurrency}\n ekvvivaletligi: {contractekvivalent}"
            if data is not None and 'contracts' in data and data['contracts']:
                buttons = []
                row = []
                for index, contract_info in enumerate(data['contracts'], start=1):
                    button_text = str(contract_info['contract'])
                    callback_text = str(contract_info['contract'])
                    ta[str(contract_info['contract'])] = str(contract_info['contract'])
                    button = InlineKeyboardButton(text=button_text, callback_data = callback_text)
                    row.append(button)
                    if index % 2 == 0:
                        buttons.append([button])
                        row = []
                if row:
                    buttons.append(row)
                back_button = InlineKeyboardButton(text="Orqaga", callback_data='Orqaga')
                buttons.append([back_button])
                reply_markup = InlineKeyboardMarkup(inline_keyboard = buttons)
                await message.answer(text = message_text, reply_markup=reply_markup)
                await Input.contracts.set()
            else:
                await message.answer("data yoq sizda", reply_markup=user_uz)
        else:
            await message.answer("Quyidagilardan tanlang: ", reply_markup=user_uz)

        @dp.callback_query_handler(state=Input.contracts)
        async def tel2(call: types.CallbackQuery, state: FSMContext):
            global messa
            messa = call.data
            if messa != "Orqaga":
                params = {
                    "type": "debt",
                    "chat_id": message.from_user.id
                }
                response = requests.get(api_url, params=params, headers=headers)
                if response:
                    data = response.json()
                    for i in range(0, len(data['contracts'])):
                        if data['contracts'][i]['contract'] == messa:
                            contract_id = data['contracts'][i]['contract']
                            contractsumm = data['contracts'][i]['contractsumm']
                            contractcurrency = data['contracts'][i]['contractcurrency']
                            contractekvivalent = data['contracts'][i]['contractekvivalent']
                            message_text = f'Shartnoma - {contract_id}:\nQarzdorlik - {contractsumm} {contractcurrency} {contractekvivalent}'
                            await bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=kop)
                            await state.finish()
            else:
                await bot.edit_message_reply_markup(chat_id=chat_id,
                                                    message_id=call.message.message_id,
                                                    reply_markup=None)
                await bot.send_message(message.chat.id, 'Orqaga', reply_markup=user_uz)

                

        @dp.callback_query_handler(text='Xa')
        async def tel3(callback_query: types.CallbackQuery):
            messa = callback_query.data
            user_id = callback_query.from_user.id
            date = str(datetime.datetime.today().date()) + "T00:00:00"
            params = {
                "type": "debt_check",
                "chat_id": callback_query.from_user.id,
                "contract_id": messa,
                "check": "true",
                'summ': summ,
                'date': date
            }
            response = requests.get(api_url, params=params, headers=headers)
            if response.ok:
                data = response.json()
                await bot.send_message(user_id, f"{data['succed_text']}")
                await bot.edit_message_reply_markup(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    reply_markup=None
                )
                await bot.send_message(user_id, "Quyidagilardan birini tanlang: ", reply_markup=user_uz)


        @dp.callback_query_handler(text="Yo'q")
        async def tel4(callback_query: types.CallbackQuery):
            user_id = callback_query.from_user.id
            date = str(datetime.datetime.today().date()) + "T00:00:00"
            params = {
                "type": "debt_check",
                "chat_id": message.from_user.id,
                "contract_id": messa,
                "check": "true",
                'summ': summ,
                'date': date
            }
            response = requests.get(api_url, params=params, headers=headers)
            if response:
                await bot.send_message(user_id, f"{data['succed_text']}")
                await bot.edit_message_reply_markup(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    reply_markup=None
                )
                await bot.send_message(user_id, "Quyidagilardan birini tanlang: ", reply_markup=user_uz)

        @dp.callback_query_handler(text="Orqaga")
        async def tel4(callback_query: types.CallbackQuery):
            chat_id = callback_query.from_user.id
            await bot.answer_callback_query(callback_query.id)
            await bot.edit_message_reply_markup(chat_id=chat_id,
                                                message_id=callback_query.message.message_id,
                                                reply_markup=None)



    @dp.message_handler(text = 'Biz bilan bog’lanish')
    async def admin(message: types.Message):
        await message.answer("Admin: @pm_hilol")


    @dp.message_handler(text='Akt sverka olish') # qayta qayta bossa bo'lishi kk forga o'xshab
    async def start_handler(message: types.Message, state: FSMContext):
        params = {
            "type": "contracts",
            "chat_id": message.from_user.id
        }
        response = requests.get(api_url, params=params, headers=headers)
        global ta, calback
        ta =[]
        calback = []
        data = response.json()
        print("ctla", data['contracts'])
        buttons = []
        for contract_info in data['contracts']:
            button_text = str(contract_info['contract'])
            cal_back = str(contract_info['contractID'])
            ta.append(str(contract_info['contract']))
            calback.append(str(contract_info['contractID']))
            button = InlineKeyboardButton(text=button_text, callback_data=cal_back)
            buttons.append([button])
        hammasi = InlineKeyboardButton(text="Hammasi", callback_data="Hammasi")
        orqaga = InlineKeyboardButton(text="Orqaga", callback_data="Orqaga")
        buttons.append([hammasi])
        ta.append('Hammasi')
        calback.append('Hammasi')
        buttons.append([orqaga])
        ta.append('Orqaga')
        calback.append('Orqaga')

        reply_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
        await message.answer("Shartnomalar", reply_markup=reply_markup)
        await state.set_state("waiting_for_contract")

    @dp.callback_query_handler(state = 'waiting_for_contract') # ishlasi kk to'xtivsz
    async def act(callback_query: CallbackQuery, state: FSMContext):
        global msgcall
        msgcall = callback_query.data
        print(msgcall)
        if msgcall != "Orqaga":
            await state.finish()
            await TimeInput.start_time.set()
            await callback_query.message.answer("Boshlang'ich sanani kiriting(masalan: Yil-OY-Kun): ")
        elif msgcall == "Hammasi":
            await state.finish()
            await TimeInput.start_time.set()
            await callback_query.message.answer("Boshlang'ich sanani kiriting(masalan: Yil-OY-Kun): ")
        else:
            await callback_query.message.edit_reply_markup(reply_markup=None)


    @dp.message_handler(state=TimeInput.start_time)
    async def start_time_handler(message: types.Message, state: FSMContext):
        if re.match(r'\d{4}-\d{2}-\d{2}', message.text):
            async with state.proxy() as data:
                data['start'] = message.text
                global start_t
                start_t = message.text
                await TimeInput.next()
                await message.answer("Tugash sanani kiriting(masalan: Yil-OY-Kun): ")
        else:
            await message.answer("To'g'ri formatda sanani kiriting(masalan: Yil-OY-Kun): ")


    @dp.message_handler(state=TimeInput.end_time)
    async def end_time_handler(message: types.Message, state: FSMContext):
        if re.match(r'\d{4}-\d{2}-\d{2}', message.text):
            async with state.proxy() as data:
                data['finish'] = message.text
                global start_t
                start = start_t + 'T00:00:00'
                finish = message.text + 'T00:00:00'
                chat_id = message.from_user.id
                if msgcall == 'Hammasi':
                    if start_t < message.text:
                        params = {
                            "type": "reconciliation_act",
                            "chat_id": chat_id,
                            "start": start,
                            "finish": finish
                        }
                if start_t < message.text:
                    params = {
                        "type": "reconciliation_act",
                            "chat_id": chat_id,
                            "start":start,
                            "finish":finish,
                            'contract_id':msgcall
                    }
                    response = requests.get(api_url, params=params, headers=headers)
                    try:
                        if response.ok:
                            content_type = response.headers.get('Content-Type', '')
                            if 'application/json' in content_type:
                                data = response.json()
                                if data.get('allsumm') is None:
                                    await message.answer("Sizda hozircha mablag' yo ")
                                else:
                                    await message.answer(f"{data['allsumm']}----{data['contracts']}")
                                await message.answer(f"Start time: {data['start']}, Finish time: {data['finish']}")
                            elif 'application/octet-stream' in content_type or 'application/vnd.ms-excel' in content_type:
                                bio = io.BytesIO(response.content)
                                bio.name = 'received_file.xlsx'
                                await message.answer_document(document=bio)
                            else:
                                result = f"Unknown Content-Type: {content_type}"
                                await message.answer(f"Sizdagi xatolik {result}")
                        else:
                            result = f"Request failed with status code {response.status_code}: {response.reason}"
                            # print("error", result)
                            await message.answer(f"Sizdagi xatolik {result}")

                    except requests.exceptions.RequestException as e:
                        result = f"Request failed: {e}"
                        await message.answer(f"Sizdagi xatolik exepdan {result}")
                    await message.answer(f"Start time: {data['start']}, Finish time: {data['finish']}")
                    await state.finish()
                else:
                    await message.answer("Boshlanish sanasi Tugash sanasidan  katta!")
                    await TimeInput.start_time.set()
                    await message.answer("Boshlang'ich sanani kiriting(masalan: Yil-OY-Kun): ")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    conn.close()
