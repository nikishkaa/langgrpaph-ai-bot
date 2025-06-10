import asyncio
from aiogram import Bot, Dispatcher

from src.config import SettingsSingleton, Settings
from aiogram import types
from aiogram import Router
from aiogram import F
from aiogram.filters import Command

from src.core.domain.document_service import DocumentService
from src.core.domain.ask_question import ask_question


router = Router()


@router.message(F.text, Command('start'))
async def start(message: types.Message):
    print(f'[BOT]: <{message.chat.id}> - /start')
    await message.answer("Привет! Отправь мне документ для загрузки или задай вопрос.")


@router.message(F.text)
async def question(message: types.Message):
    thread_id = message.chat.id
    print(f'[BOT]: <{thread_id}> - {message.text}')
    answer = ask_question(message.text, str(thread_id))

    await message.answer(str(answer))


@router.message(F.document)
async def upload_document(message: types.Message):
    print(f'[BOT]: <{message.chat.id}> - file loaded')
    doc_file = await bot.get_file(message.document.file_id)
    doc_file_bytes = await bot.download_file(doc_file.file_path)

    content = doc_file_bytes.read().decode()
    service = DocumentService()
    service.upload_from_text(content)

    await message.answer('Документ загружен!')

dp = Dispatcher()
dp.include_router(router)

if __name__ == '__main__':
    settings: Settings = SettingsSingleton.get_instance()
    service = DocumentService()
    path: str = settings.langgraph.default_doc_file_path
    service.upload_from_file(path)
    print(f'[LOADED FILE]: {path}')

    token: str = settings.bot.token
    bot = Bot(token=token)
    asyncio.run(dp.start_polling(bot))
