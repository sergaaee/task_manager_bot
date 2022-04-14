from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import calendar
from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.types import CallbackQuery


class InlineKeyboard:
    main_menu = InlineKeyboardMarkup(row_width=3)
    data = {
        '1': 1,
        '2': 2,
        '3': 3
    }
    for key, value in data.items():
        main_menu.add(InlineKeyboardButton(text=key, callback_data=value))


calendar_callback = CallbackData('simple_calendar', 'act', 'year', 'month', 'day')


class SimpleCalendar:

    @staticmethod
    async def start_calendar(year: int = datetime.now().year,
                             month: int = datetime.now().month) -> InlineKeyboardMarkup:
        inline_kb = InlineKeyboardMarkup(row_width=7)
        ignore_callback = calendar_callback.new("IGNORE", year, month, 0)  # for buttons with no answer
        # First row - Month and Year
        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(
            "<<",
            callback_data=calendar_callback.new("PREV-YEAR", year, month, 1)
        ))
        inline_kb.insert(InlineKeyboardButton(
            f'{calendar.month_name[month]} {str(year)}',
            callback_data=ignore_callback
        ))
        inline_kb.insert(InlineKeyboardButton(
            ">>",
            callback_data=calendar_callback.new("NEXT-YEAR", year, month, 1)
        ))
        # Second row - Week Days
        inline_kb.row()
        for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
            inline_kb.insert(InlineKeyboardButton(day, callback_data=ignore_callback))

        # Calendar rows - Days of month
        month_calendar = calendar.monthcalendar(year, month)
        for week in month_calendar:
            inline_kb.row()
            for day in week:
                if day == 0:
                    inline_kb.insert(InlineKeyboardButton(" ", callback_data=ignore_callback))
                    continue
                inline_kb.insert(InlineKeyboardButton(
                    str(day), callback_data=calendar_callback.new("DAY", year, month, day)
                ))

        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(
            "<", callback_data=calendar_callback.new("PREV-MONTH", year, month, day)
        ))
        inline_kb.insert(InlineKeyboardButton(" ", callback_data=ignore_callback))
        inline_kb.insert(InlineKeyboardButton(
            ">", callback_data=calendar_callback.new("NEXT-MONTH", year, month, day)
        ))

        return inline_kb

    @staticmethod
    async def process_selection(query: CallbackQuery, data: CallbackData) -> tuple:

        return_data = (False, None)
        temp_date = datetime(int(data['year']), int(data['month']), 1)

        if data['act'] == "IGNORE":
            await query.answer(cache_time=60)

        if data['act'] == "DAY":
            await query.message.delete_reply_markup()
            return_data = True, datetime(int(data['year']), int(data['month']), int(data['day']))

        if data['act'] == "PREV-YEAR":
            prev_date = temp_date - timedelta(days=365)
            await query.message.edit_reply_markup(
                await SimpleCalendar.start_calendar(int(prev_date.year), int(prev_date.month)))

        if data['act'] == "NEXT-YEAR":
            next_date = temp_date + timedelta(days=365)
            await query.message.edit_reply_markup(
                await SimpleCalendar.start_calendar(int(next_date.year), int(next_date.month)))

        if data['act'] == "PREV-MONTH":
            prev_date = temp_date - timedelta(days=1)
            await query.message.edit_reply_markup(
                await SimpleCalendar.start_calendar(int(prev_date.year), int(prev_date.month)))

        if data['act'] == "NEXT-MONTH":
            next_date = temp_date + timedelta(days=31)
            await query.message.edit_reply_markup(
                await SimpleCalendar.start_calendar(int(next_date.year), int(next_date.month)))

        return return_data


    @staticmethod
    def simple_callback():
        return calendar_callback

