from aiogram import Bot, Dispatcher, executor, types
import logging
from aiogram.dispatcher import FSMContext
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from config import TOKEN, CHANELID
from states import Post
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    channel_url = InlineKeyboardButton(text='КАНАЛ',url='https://t.me/prostoykurs')
    btn = InlineKeyboardMarkup(row_width=1).add(channel_url)
    await message.answer('Привет! Перейди в канал для выбора!', reply_markup=btn)

@dp.message_handler(commands='add')
async def add(message: types.Message):
    await message.answer('Отправьте фото')
    await Post.photo.set()

@dp.message_handler(state = Post.photo, content_types='photo')
async def get_photo(message: types.Message, state: FSMContext):
    await state.update_data(photo_id = message.photo[0].file_id)
    await message.answer('Отправьте описание')
    await Post.caption.set()

@dp.message_handler(state = Post.caption, content_types='text')
async def get_caption(message: types.Message, state: FSMContext):
    await state.update_data(caption=message.text)
    await message.answer('Отправьте ссылку')
    await Post.url.set()

@dp.message_handler(state=Post.url, content_types='text')
async def get_url(message: types.Message, state: FSMContext):
    await state.update_data(url=message.text)
    data = await state.get_data()
    url_btn = InlineKeyboardButton(text= 'СМОТРЕТЬ',url=data['url'])
    btn = InlineKeyboardMarkup(row_width=1).add(url_btn)
    await bot.send_photo(chat_id= CHANELID, photo=data['photo_id'], caption=data['caption'], reply_markup=btn)
    await message.answer('Готово')
    await state.finish()
    


if __name__ == '__main__':
    executor.start_polling(dp)
