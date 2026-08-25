# -- создаём роутер и регистрируем хендлеры, которые управляют диалогом --

from aiogram import Router, F # импорт роутера и f-все текстовые соо от юзера
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton 
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from handlers.states import DownloadStates #импорт состояний(ожидание того или иного)

from downloader import download_media
import os
from aiogram.types import FSInputFile

router = Router() #создание роутера

@router.message(Command('download'))
async def download(message: Message, state: FSMContext):
    await state.set_state(DownloadStates.waiting_for_link)
    await message.answer('пришлите ссылку на видео/песню')

@router.message(DownloadStates.waiting_for_link, F.text)
async def link_process(message: Message, state: FSMContext):
    await state.update_data(link=message.text) #в дату юзера записываем ячейку link с его присланной ссылкой

    await state.set_state(DownloadStates.waiting_for_quality) # ставим статус ожидания качества

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🎬 Видео 1080p (MP4)", callback_data="video_1080_mp4")],
    [InlineKeyboardButton(text="🎬 Видео 720p (MP4)", callback_data="video_720_mp4")],
    [InlineKeyboardButton(text="🎬 Видео 1080p (MKV)", callback_data="video_1080_mkv")],
    [InlineKeyboardButton(text="🎬 Видео 720p (MKV)", callback_data="video_720_mkv")],
    [InlineKeyboardButton(text="🎵 Аудио MP3", callback_data="audio_mp3")],
    [InlineKeyboardButton(text="🎵 Аудио M4A", callback_data="audio_m4a")],
    [InlineKeyboardButton(text="🎵 Аудио FLAC", callback_data="audio_flac")],
    ])
    await message.answer("Выбери качество(если видео, то первые 4 пункта, если трек, то 5-7 пункты):", reply_markup=keyboard)

@router.callback_query(DownloadStates.waiting_for_quality, F.data.startswith('video_') | F.data.startswith('audio_'))
async def quality_process(callback: CallbackQuery, state: FSMContext):

    await callback.answer() #???

    user_data = await state.get_data()
    link = user_data.get("link")
    choice = callback.data   # например, 'video_1080_mp4' или 'audio_mp3'

    await callback.message.edit_text("Скачиваю... Пожалуйста, подождите.")

    # Запускаем загрузку в отдельном потоке
    import asyncio
    file_path, metadata = await asyncio.to_thread(download_media, link, choice)

    if file_path is None:
        await callback.message.answer("Не удалось скачать файл. Проверьте ссылку.")
        await state.clear()
        return
    
    if choice.startswith('video_'):
        await callback.message.answer_video(
                video=FSInputFile(file_path))

    else:  # audio
        # Получаем метаданные 
        await callback.message.answer_audio(
                audio=FSInputFile(file_path),
                title=metadata.get('title'),
                performer=metadata.get('artist'),
            )
    os.remove(file_path)
    
    await state.clear()