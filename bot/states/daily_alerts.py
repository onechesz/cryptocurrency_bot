from aiogram.fsm.state import StatesGroup, State


class DailyAlerts(StatesGroup):
    daily_alerts = State()
