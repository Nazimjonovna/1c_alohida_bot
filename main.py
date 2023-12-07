import datetime
import logging
from buttons import *
from buttons import tel
from aiogram import Bot, Dispatcher, executor, types
import requests
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

api_url = 'http://5.182.26.180:55565/telegramsam/hs/hl/gd'
login = 'HILOL'
password = '0ut0fb0unD'

headers = {
            'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
            'User-Agent': 'PostmanRuntime/7.35.0',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }

API_TOKEN = '6293716593:AAFaFRDPx3LwppaxKsbytBTHAOZcPVRhoAU'

# Configure logging
logging.basicConfig(level=logging.INFO)
# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot,storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

class Input(StatesGroup):
    sery = State()
    end_time = State()
    contracts = State()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("1c_botingiznga xush kelibsz!: ", reply_markup=lang1)

@dp.message_handler(text = "🇺🇿")
async def lang(message: types.Message):
    await message.answer("Assalomu alaykum, OOO APPLOAD CRM botiga xush kelibsiz!\nIdentifikatsiyadan o’tish uchun telefon raqamingizni ulashing.", reply_markup=tel)

    @dp.message_handler(content_types=types.ContentType.CONTACT)
    async def tel1(message: types.Message):
        params = {
            "type": "contracts",
            "chat_id": 901569590
        }
        response = requests.get(api_url, params=params, headers=headers)
        global ta
        ta = []
        if response:
            data = response.json()
            if data:
                buttons = []
                for contract_info in data['contracts']:
                    button_text = str(contract_info['contractID'])
                    ta.append(str(contract_info['contractID']))
                    button = KeyboardButton(text=button_text)
                    buttons.append([button])

                reply_markup = ReplyKeyboardMarkup(keyboard=buttons)
                await message.answer("Choose which one of them", reply_markup=reply_markup)
                await Input.contracts.set()
        else:
            await message.answer("Quyidagilardan tanlang: ", reply_markup=menu)

        @dp.message_handler(state=Input.contracts)
        async def act(message: types.Message, state: FSMContext):
            global contract_id
            contract_id = message.text
            await state.finish()
            await message.answer("Quyidagilardan tanlang: ", reply_markup=menu)

        @dp.message_handler(text = "Qarzdorlikni tekshirish")
        async def tel2(message: types.Message):
            params = {
                "type": "debt",
                "chat_id": 901569590
            }
            response = requests.get(api_url, params=params, headers=headers)
            if response:
                global summ
                summ = response.json()['allsumm']
                await message.answer(f'{response.json()}')
                await message.answer("Quyidagilardan tanlang: ", reply_markup=kop)

                @dp.message_handler(text = 'Xa')
                async def tel3(message: types.Message):
                    date = str(datetime.datetime.today().date())+"T00:00:00"
                    params = {
                        "type": "debt_check",
                        "chat_id": 901569590,
                        "contract_id":contract_id,
                        "check":"true",
                        'summ':summ,
                        'date':date
                    }
                    print('lalala')
                    print("params", params)
                    response = requests.get(api_url, params=params, headers=headers)
                    print(response)
                    if response:
                        print(response.status_code)
                        await message.answer(f"{response.json()}")

                @dp.message_handler(text="Yo'q")
                async def tel4(message: types.Message):
                    date = str(datetime.datetime.today().date()) + "T00:00:00"
                    params = {
                        "type": "debt_check",
                        "chat_id": 901569590,
                        "contract_id": contract_id,
                        "check": "true",
                        'summ': summ,
                        'date': date
                    }
                    response = requests.get(api_url, params=params, headers=headers)
                    if response:
                        await message.answer(f"{response.json()}")

                @dp.message_handler(text="Orqaga")
                async def tel4(message: types.Message):
                    await message.answer("ok", reply_markup=menu)

        @dp.message_handler(text="Seriya bo'yicha izlash")
        async def tel4(message: types.Message):
            await message.answer("Seriya raqamini kiriting:")
            await Input.sery.set()

        @dp.message_handler(state=Input.sery)
        async def act(message: types.Message, state: FSMContext):
            global sery
            sery = message.text
            params = {
                "type": "search_by_series",
                "sery": sery
            }
            response = requests.get(api_url, params=params, headers=headers)
            print(response.status_code)
            if response:
                print(response.json())
                await message.answer(f"{response.json()}")









        # global ta
        # ta = []
        # data = response.json()
        # if data:
        #     buttons = []
        #     for contract_info in data['contracts']:
        #         button_text = str(contract_info['contract'])
        #         ta.append(str(contract_info['contract']))
        #         button = KeyboardButton(text=button_text)
        #         buttons.append([button])
        #
        #     reply_markup = ReplyKeyboardMarkup(keyboard=buttons)
        #     await message.answer("Choose which one of them", reply_markup=reply_markup)
        #     await Input.contracts.set()
        # else:
        #     await message.answer("Quyidagilardan tanlang: ", reply_markup=menu)
        #
        # @dp.message_handler(state=Input.contracts)
        # async def act(message: types.Message, state: FSMContext):
        #     global contract_id
        #     contract_id = message.text
        #     print(datetime.UTC)
        #     params = {
        #         "type": "debt",
        #         "chat_id": 901569590
        #     }
        #     response = requests.get(api_url, params=params, headers=headers)
        #     if response:
        #     await message.answer("Qarzdorlikni tasdiqlayszmi? : ", reply_markup=kop)
        #
        #     @dp.callback_query_handlers(text="Xa")
        #     async def xa(message:types.Message):
        #         params = {
        #             'type': 'debt_check',
        #             'chat_id': 901569590,
        #             "contract_id":contract_id,
        #             "check":'true',
        #             'date':datetime.UTC
        #         }
        #         await message.answer("Right")
        #
        # #     if selected_contract in ta:
        #
        # #         headers = {
        # #             'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
        # #             'User-Agent': 'PostmanRuntime/7.35.0',
        # #             'Accept': '*/*',
        # #             'Accept-Encoding': 'gzip, deflate, br',
        # #             'Connection': 'keep-alive'
        # #         }
        # #
        # #         try:
        # #             response = requests.get(api_url, params=params, headers=headers)
        # #             if response.ok:
        # #                 if 'application/json' in response.headers.get('Content-Type', ''):
        # #                     data = response.json()
        # #                     result = response.text
        # #                 else:
        # #                     result = f"Response is not in JSON format: {response.text}"
        # #             else:
        # #                 result = f"Request failed with status code {response.status_code}: {response.reason}"
        # #             await message.answer(f"{data.get('UZ')}", reply_markup=kop)
        # #
        # #         except requests.exceptions.RequestException as e:
        # #             result = f"Request failed: {e}"
        # #             await message.answer(f"{data.get('UZ')}")
        # #         await state.finish()
        # #
        # #
        # # @dp.message_handler(text = 'Qarzdorlikni tekshirish')
        # # async def t_list(message: types.Message):
        # #
        # #
        # #
        # #
        # # @dp.message_handler(text="Seriya bo'yicha izlash")
        # # async def seriya(message: types.Message):
        # #     selected_contract = message.text
        # #     params = {
        # #         'type': 'search_by_series',
        # #         "sery": 353742533112405
        # #
        # #     }
        # #     headers = {
        # #         'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
        # #         'User-Agent': 'PostmanRuntime/7.35.0',
        # #         'Accept': '*/*',
        # #         'Accept-Encoding': 'gzip, deflate, br',
        # #         'Connection': 'keep-alive'
        # #     }
        # #
        # #     try:
        # #         response = requests.get(api_url, params=params, headers=headers)
        # #         if response.ok:
        # #             if 'application/json' in response.headers.get('Content-Type', ''):
        # #                 data = response.json()
        # #                 # if data
        # #                 print("sasa", data)  # ! bug shu joyda
        # #                 result = response.text
        # #             else:
        # #                 result = f"Response is not in JSON format: {response.text}"
        # #         else:
        # #             result = f"Request failed with status code {response.status_code}: {response.reason}"
        # #         await message.answer(f"{data}")
        # #
        # #     except requests.exceptions.RequestException as e:
        # #         result = f"Request failed: {e}"
        # #         await message.answer(f"{data}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)