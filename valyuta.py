from aiogram import types
from states.state import Menu, Valyuta, Edit
from keyboards.default.key_board import markup, menu_markup, control
from keyboards.inline.in_key_board import uni_calc
from aiogram.dispatcher import FSMContext
from loader import dp
from datetime import datetime
from data.utils import get_type, every_three

# Yordomchi o'zgaruvchila
now = datetime.now().date()
#########################
from datetime import datetime
from states.state import Menu, Valyuta, Edit
from keyboards.default.key_board import menu_markup, markup
from data.get_api import get_type
from aiogram.dispatcher import FSMContext
from loader import dp

# Yordamchi o'zgaruvchila ##############
now = datetime.now().date()
########################################



@dp.message_handler(state="*", text="Asosiy menyu 🏠")
async def go_menu(message: types.Message):
    await message.reply("Siz asosiy menyudasiz 😊", reply_markup=menu_markup)
    await Menu.menu.set()

@dp.message_handler(state=Valyuta, text="Orqaga ↩️")
async def go_back(message: types.Message):
    await message.reply("Siz asosiy menyudasiz 😊", reply_markup=menu_markup)
    await Menu.menu.set()
###############################   Control   ###############################################

@dp.message_handler(state=Menu.menu, text="🇺🇿Valyuta UZS(So'm)🇺🇿")
async def bot_direct(message: types.Message):
    await message.answer("Quyidagi valyutalardan birini tanlang...", reply_markup=markup)
    await Valyuta.valyuta.set()
@dp.message_handler(state=Menu.menu, text="💸Valyuta kurslari💸")
async def get_type_of_money(message: types.Message, state: FSMContext):
    await message.answer("Valyuta kurslari bo'limiga xush kelibsiz😁", reply_markup=control)
    await message.answer("<i><b>Asosiy valyuta turini tanlang...</b></i>", reply_markup=uni_calc, parse_mode="html")
    await Edit.first.set()
@dp.message_handler(state=Valyuta, text="Orqaga ↩️")
async def go_back(message: types.Message):
    await message.reply("Siz asosiy menyudasiz 😊", reply_markup=menu_markup)
    await Menu.menu.set()


#############################   Currencies   ############################################
@dp.message_handler(state=Edit.calc, text="Orqaga ↩️")
async def go_back1(message: types.Message):
    await message.reply("Siz valyuta turini tanlash bo'limidasiz")
    await message.answer("<i><b>Asosiy valyuta turini tanlang...</b></i>", reply_markup=uni_calc, parse_mode="html")
    await Edit.first.set()

@dp.message_handler(state=Edit.second, text="Orqaga ↩️")
async def go_back2(message: types.Message):
    await message.answer("<i><b>Asosiy valyuta turini tanlang...</b></i>", reply_markup=uni_calc, parse_mode="html")
    await Edit.first.set()
@dp.message_handler(state=Edit.first, text="Orqaga ↩️")
async def go_back3(message: types.Message):
    await message.reply("Siz asosiy menyudasiz 😊", reply_markup=menu_markup)
    await Menu.menu.set()
##############################################
@dp.callback_query_handler(text=["uzs_🇺🇿", "usd_🇺🇸", "eur_🇪🇺", "rub_🇷🇺", "try_🇹🇷", "cny_🇨🇳", "kzt_🇰🇿", "aed_🇦🇪", "krw_🇰🇷", "btc_💎"], state=Edit.first)
async def first_type_of_money(call: types.CallbackQuery, state: FSMContext):
    type = call.data
    await call.message.delete()
    type1 = type.split("_")
    await state.update_data({"type1" : type1[0]})
    await state.update_data({"flag1" : type1[1]})
    await call.message.answer("<i><b>Xisobchi valyutani turini tanlang...</b></i>", reply_markup=uni_calc, parse_mode="html")
    await Edit.second.set()
@dp.callback_query_handler(text=["uzs_🇺🇿", "usd_🇺🇸", "eur_🇪🇺", "rub_🇷🇺", "try_🇹🇷", "cny_🇨🇳", "kzt_🇰🇿", "aed_🇦🇪", "krw_🇰🇷", "btc_💎"], state=Edit.second)
async def second_type_of_money(call: types.CallbackQuery, state: FSMContext):
    type = call.data
    await call.message.delete()
    type2 = type.split("_")
    await state.update_data({"type2" : type2[0]})
    await state.update_data({"flag2" : type2[1]})
    data = await state.get_data()
    res1 = data["type1"]
    flag1 = data["flag1"]
    res2 = data["type2"]
    flag2 = data["flag2"]
    res = get_type(res1, res2)
    res = every_three(res)
    type1 = res1.upper()
    type2 = res2.upper()
    await call.message.answer(f"🕔 <i>{now}</i>\n\n<b>1</b> {type1} {flag1} ➡️ {flag2} <b>{res}</b> {type2}\n\n<i>Istalgan summani kiriting</i>\n<i><b>Masalan:</b>  100</i>\n\nValyuta turini o'zgartirish uchun orqaga qayting", parse_mode="html")
    await Edit.calc.set()
@dp.message_handler(state=Edit.calc)
async def calc_type_of_money(message: types.Message, state: FSMContext):
    mes = message.text
    try:
        ban = float(mes)
    except ValueError:
        ban = 0
        await message.reply("Miqdorni sonlarda kiriting!")

    if ban < 0:
        await message.reply("Miqdorni musbat sonlarda kiriting!")
    elif ban > 0:
        data = await state.get_data()
        res1 = data["type1"]
        flag1 = data["flag1"]
        res2 = data["type2"]
        flag2 = data["flag2"]
        result = get_type(res1, res2)
        result = float(result)
        mes = float(mes)
        type1 = res1.upper()
        type2 = res2.upper()
        res = result * mes
        res = every_three(res)
        await message.answer(f"🕔 <i>{now}</i>\n\n<b>{mes}</b> {type1} {flag1} ➡️ {flag2} <b>{res}</b> {type2}\n\nValyuta turini o'zgartirish uchun orqaga qayting", parse_mode="html")

############################################################################################
#########################   CURRENCY TABLE   ###############################################
############################################################################################
# DOLLAR
@dp.message_handler(state=Valyuta, text=["🇺🇸 Dollar 🇺🇸", "DOLLAR", "Dollar", "dollar", "$", "💸", "💰", "💵", "💲", "🇺🇸", "Usd", "USD", "usd"])
async def get_dollar(message: types.Message):
    usd = "usd"
    usd2 = "uzs"
    money = get_type(usd, usd2)
    money = every_three(money)
    await message.answer(f"🕔 <i>{now}</i>\n\n<b>1</b> USD 🇺🇸 ➡️ 🇺🇿 <b>{money}</b> UZS\n\n<i>Istalgan summani kiriting</i>\n<i><b>Masalan:</b>  100</i>", parse_mode="html")
    await Valyuta.dollar.set()

@dp.message_handler(state=Valyuta, text=["🇪🇺 Euro 🇪🇺", "EURO", "Euro", "euro", "€", "💶", "Eur", "EUR", "eur", "🇪🇺"])
async def get_euro(message: types.Message):
    usd = "eur"
    usd2 = "uzs"
    money = get_type(usd, usd2)
    money = every_three(money)
    await message.answer(f"🕔 <i>{now}</i>\n\n<b>1</b> EUR 🇪🇺 ➡️ 🇺🇿 <b>{money}</b> UZS\n\n<i>Istalgan summani kiriting</i>\n<i><b>Masalan:</b>  100</i>", parse_mode="html")
    await Valyuta.euro.set()

@dp.message_handler(state=Valyuta, text=["💎 Bitcoin 💎", "BITCOIN", "Bitcoin", "bitcoin", "₿", "💎", "Btc", "BTC", "btc"])
async def get_bitcoin(message: types.Message):
    usd = "btc"
    usd2 = "uzs"
    money = get_type(usd, usd2)
    money = every_three(money)
    await message.answer(f"🕔 <i>{now}</i>\n\n<b>1</b> BTC 💎 ➡️ 🇺🇿 <b>{money}</b> UZS\n\n<i>Istalgan summani kiriting</i>\n<i><b>Masalan:</b>  100</i>", parse_mode="html")
    await Valyuta.bitcoin.set()

@dp.message_handler(state=Valyuta, text=["🇷🇺 Rubl 🇷🇺", "RUBL", "Rubl", "rubl", "🇷🇺", "Rub", "RUB", "rub"])
async def get_rubl(message: types.Message):
    usd = "rub"
    usd2 = "uzs"
    money = get_type(usd, usd2)
    money = every_three(money)
    await message.answer(f"🕔 <i>{now}</i>\n\n<b>1</b> RUB 🇷🇺 ➡️ 🇺🇿 <b>{money}</b> UZS\n\n<i>Istalgan summani kiriting</i>\n<i><b>Masalan:</b>  100</i>", parse_mode="html")
    await Valyuta.rubl.set()

@dp.message_handler(state=Valyuta, text=["🇹🇷 Lira 🇹🇷", "LIRA", "Lira", "lira", "🇹🇷", "Try", "TRY", "try"])
async def get_lira(message: types.Message):
    usd = "try"
    usd2 = "uzs"
    money = get_type(usd, usd2)
    money = every_three(money)
    await message.answer(f"🕔 <i>{now}</i>\n\n<b>1</b> TRY 🇹🇷 ➡️ 🇺🇿 <b>{money}</b> UZS\n\n<i>Istalgan summani kiriting</i>\n<i><b>Masalan:</b>  100</i>", parse_mode="html")
    await Valyuta.lira.set()
  
@dp.message_handler(state=Valyuta, text=["🇨🇳 Yuang 🇨🇳", "YUANG", "Yuang", "yuang", "🇨🇳", "Cny", "CNY", "cny"])
async def get_yuang(message: types.Message):
    usd = "cny"
    usd2 = "uzs"
    money = get_type(usd, usd2)
    money = every_three(money)
    await message.answer(f"🕔 <i>{now}</i>\n\n<b>1</b> CNY 🇨🇳 ➡️ 🇺🇿 <b>{money}</b> UZS\n\n<i>Istalgan summani kiriting</i>\n<i><b>Masalan:</b>  100</i>", parse_mode="html")
    await Valyuta.yuang.set()

@dp.message_handler(state=Valyuta, text=["🇰🇿 Tenge 🇰🇿", "TENGE", "Tenge", "tenge", "🇰🇿", "Kzt", "KZT", "kzt"])
async def get_tenge(message: types.Message):
    usd = "kzt"
    usd2 = "uzs"
    money = get_type(usd, usd2)
    money = every_three(money)
    await message.answer(f"🕔 <i>{now}</i>\n\n<b>1</b> KZT 🇰🇿 ➡️ 🇺🇿 <b>{money}</b> UZS\n\n<i>Istalgan summani kiriting</i>\n<i><b>Masalan:</b>  100</i>", parse_mode="html")
    await Valyuta.tenge.set()

@dp.message_handler(state=Valyuta, text=["🇦🇪 Dirham 🇦🇪", "DIRHAM", "Dirham", "dirham", "🇦🇪", "Aed", "AED", "aed"])
async def get_dirham(message: types.Message):
    usd = "aed"
    usd2 = "uzs"
    money = get_type(usd, usd2)
    money = every_three(money)
    await message.answer(f"🕔 <i>{now}</i>\n\n<b>1</b> AED 🇦🇪 ➡️ 🇺🇿 <b>{money}</b> UZS\n\n<i>Istalgan summani kiriting</i>\n<i><b>Masalan:</b>  100</i>", parse_mode="html")
    await Valyuta.dirham.set()

@dp.message_handler(state=Valyuta, text=["🇰🇷 Von 🇰🇷", "VON", "Von", "von", "🇰🇷", "Krw", "KRW", "krw"])
async def get_von(message: types.Message):
    usd = "krw"
    usd2 = "uzs"
    money = get_type(usd, usd2)
    money = every_three(money)
    await message.answer(f"🕔 <i>{now}</i>\n\n<b>1</b> KRW 🇰🇷 ➡️ 🇺🇿 <b>{money}</b> UZS\n\n<i>Istalgan summani kiriting</i>\n<i><b>Masalan:</b>  100</i>", parse_mode="html")
    await Valyuta.von.set()

#############################################################################################
#############################   CALCULATING   ###############################################
#############################################################################################
# DOLLAR CALC
@dp.message_handler(state=Valyuta.dollar)
async def calc_dollar(message: types.Message, state: FSMContext):
    mes = message.text
    try:
        ban = float(mes)
    except ValueError:
        ban = 0
        await message.reply("Miqdorni sonlarda kiriting!")

    if ban < 0:
        await message.reply("Miqdorni musbat sonlarda kiriting!")
    elif ban > 0:
        mes = float(mes)
        money = get_type("usd", "uzs")
        money = float(money)
        res = money * mes
        res = every_three(res)
    await message.reply(f"🕔 <i>{now}</i>\n\n<b>{mes}</b> USD 🇺🇸 ➡️ 🇺🇿 <b>{res}</b> UZS\n\nIstalgan vaqtda valyuta o'zgartirishingiz mumkin", parse_mode="html")

# EURO CALC
@dp.message_handler(state=Valyuta.euro)
async def calc_euro(message: types.Message):
    mes = message.text
    try:
        ban = float(mes)
    except ValueError:
        ban = 0
        await message.reply("Miqdorni sonlarda kiriting!")

    if ban < 0:
        await message.reply("Miqdorni musbat sonlarda kiriting!")
    elif ban > 0:
        mes = float(mes)
        money = get_type("eur", "uzs")
        money = float(money)
        res = money * mes
        res = every_three(res)
        await message.reply(f"🕔 <i>{now}</i>\n\n<b>{mes}</b> EUR 🇪🇺 ➡️ 🇺🇿 <b>{res}</b> UZS\n\nIstalgan vaqtda valyuta o'zgartirishingiz mumkin", parse_mode="html")


# BITCOIN CALC
@dp.message_handler(state=Valyuta.bitcoin)
async def calc_bitcoin(message: types.Message):
    mes = message.text
    try:
        ban = float(mes)
    except ValueError:
        ban = 0
        await message.reply("Miqdorni sonlarda kiriting!")

    if ban < 0:
        await message.reply("Miqdorni musbat sonlarda kiriting!")
    elif ban > 0:
        mes = float(mes)
        money = get_type("btc", "uzs")
        money = float(money)
        res = money * mes
        res = every_three(res)
        await message.reply(f"🕔 <i>{now}</i>\n\n<b>{mes}</b> BTC 💎 ➡️ 🇺🇿 <b>{res}</b> UZS\n\nIstalgan vaqtda valyuta o'zgartirishingiz mumkin", parse_mode="html")



# RUBL CALC
@dp.message_handler(state=Valyuta.rubl)
async def calc_rubl(message: types.Message):
    mes = message.text
    try:
        ban = float(mes)
    except ValueError:
        ban = 0
        await message.reply("Miqdorni sonlarda kiriting!")

    if ban < 0:
        await message.reply("Miqdorni musbat sonlarda kiriting!")
    elif ban > 0:

        mes = float(mes)
        money = get_type("rub", "uzs")
        money = float(money)
        res = money * mes
        res = every_three(res)
        await message.reply(f"🕔 <i>{now}</i>\n\n<b>{mes}</b> RUB 🇷🇺 ➡️ 🇺🇿 <b>{res}</b> UZS\n\nIstalgan vaqtda valyuta o'zgartirishingiz mumkin", parse_mode="html")


# LIRA CALC
@dp.message_handler(state=Valyuta.lira)
async def calc_lira(message: types.Message):
    mes = message.text
    try:
        ban = float(mes)
    except ValueError:
        ban = 0
        await message.reply("Miqdorni sonlarda kiriting!")

    if ban < 0:
        await message.reply("Miqdorni musbat sonlarda kiriting!")
    elif ban > 0:

        mes = float(mes)
        money = get_type("try", "uzs")
        money = float(money)
        res = money * mes
        res = every_three(res)
        await message.reply(f"🕔 <i>{now}</i>\n\n<b>{mes}</b> TRY 🇹🇷 ➡️ 🇺🇿 <b>{res}</b> UZS\n\nIstalgan vaqtda valyuta o'zgartirishingiz mumkin", parse_mode="html")


# YUANG CALC
@dp.message_handler(state=Valyuta.yuang)
async def calc_yuang(message: types.Message):
    mes = message.text
    try:
        ban = float(mes)
    except ValueError:
        ban = 0
        await message.reply("Miqdorni sonlarda kiriting!")

    if ban < 0:
        await message.reply("Miqdorni musbat sonlarda kiriting!")
    elif ban > 0:
        mes = float(mes)
        money = get_type("cny", "uzs")
        money = float(money)
        res = money * mes
        res = every_three(res)
        await message.reply(f"🕔 <i>{now}</i>\n\n<b>{mes}</b> CNY 🇨🇳 ➡️ 🇺🇿 <b>{res}</b> UZS\n\nIstalgan vaqtda valyuta o'zgartirishingiz mumkin", parse_mode="html")


# TENGE CALC

@dp.message_handler(state=Valyuta.tenge)
async def calc_tenge(message: types.Message):
    mes = message.text
    try:
        ban = float(mes)
    except ValueError:
        ban = 0
        await message.reply("Miqdorni sonlarda kiriting!")

    if ban < 0:
        await message.reply("Miqdorni musbat sonlarda kiriting!")
    elif ban > 0:

        mes = float(mes)
        money = get_type("kzt", "uzs")
        money = float(money)
        res = money * mes
        res = every_three(res)
        await message.reply(f"🕔 <i>{now}</i>\n\n<b>{mes}</b> KZT 🇰🇿 ➡️ 🇺🇿 <b>{res}</b> UZS\n\nIstalgan vaqtda valyuta o'zgartirishingiz mumkin", parse_mode="html")


# DIRHAM CALC

@dp.message_handler(state=Valyuta.dirham)
async def calc_dirham(message: types.Message):
    mes = message.text
    try:
        ban = float(mes)
    except ValueError:
        ban = 0
        await message.reply("Miqdorni sonlarda kiriting!")

    if ban < 0:
        await message.reply("Miqdorni musbat sonlarda kiriting!")
    elif ban > 0:
        mes = float(mes)
        money = get_type("aed", "uzs")
        money = float(money)
        res = money * mes
        res = every_three(res)
        await message.reply(f"🕔 <i>{now}</i>\n\n<b>{mes}</b> AED 🇦🇪 ➡️ 🇺🇿 <b>{res}</b> UZS\n\nIstalgan vaqtda valyuta o'zgartirishingiz mumkin", parse_mode="html")


# VON CALC
@dp.message_handler(state=Valyuta.von)
async def calc_von(message: types.Message):
    mes = message.text
    try:
        ban = float(mes)
    except ValueError:
        ban = 0
        await message.reply("Miqdorni sonlarda kiriting!")

    if ban < 0:
        await message.reply("Miqdorni musbat sonlarda kiriting!")
    elif ban > 0:

        mes = float(mes)
        money = get_type("krw", "uzs")
        money = float(money)
        res = money * mes
        res = every_three(res)
        await message.reply(f"🕔 <i>{now}</i>\n\n<b>{mes}</b> KRW 🇰🇷 ➡️ 🇺🇿 <b>{res}</b> UZS\n\nIstalgan vaqtda valyuta o'zgartirishingiz mumkin", parse_mode="html")

#############################################################################################