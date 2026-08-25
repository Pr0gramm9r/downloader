from aiogram.fsm.state import State, StatesGroup

class DownloadStates(StatesGroup):
    waiting_for_link = State() #статус ожидания ссылки
    waiting_for_quality = State() #статус ожидания качества (видео)