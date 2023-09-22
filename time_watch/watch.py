"""
            ***----------------------------------------------------------------------------------------***
                ***------------------------ DUMELANG means GREETINGS! ~ G-CODE -----------------------***
                     ***------------------------------------------------------------------------***

            "TIME-KEEPER APP" Version 1.0.0
"""

import os
import sys
import pytz
import sqlite3
import datetime
import customtkinter
from tkinter import StringVar
from tkcalendar import Calendar
from tzlocal import get_localzone
from babel import numbers  # For Nuitka Bundling to override a ModuleNotFoundError
from sqlite3 import Connection, Cursor


class Watch(customtkinter.CTk):
    """
    Our main class for setting up the toplevel window object, the tab container and invoking the other classes.
    """
    # MODE + THEME Settings
    customtkinter.set_appearance_mode("SYSTEM")
    customtkinter.set_default_color_theme("dark-blue")
    _ = numbers  # Using an unused import

    def __init__(self):
        super(Watch, self).__init__()

        # OUR WINDOW OBJECT
        self.iconbitmap(resource_path('..\\timeKeeper-icon.ico'))
        self.title('Time Keeper')
        self.geometry("812x336")
        self.resizable(height=False, width=False)

        # A MASTER FRAME
        self.master_frame = customtkinter.CTkFrame(master=self, fg_color=None)
        self.master_frame.pack(side="top", fill="both", expand=True)

        # MODE COLOUR SETTINGS
        self.darker_gray_white = {'Dark': '#343434', 'Light': '#FFFFFF'}
        self.darker_gray_lighter_gray = {'Dark': '#232323', 'Light': '#A5A5A5'}
        self.mid_gray_lighter_gray = {'Dark': '#444444', 'Light': '#787878'}
        self.white_darker_gray = {'Dark': '#FFFFFF', 'Light': '#444444'}
        self.dark_gray_lighter_gray = {'Dark': '#232323', 'Light': '#F2F2F2'}
        self.light_gray_white = {'Dark': '#565656', 'Light': '#FFFFFF'}
        self.light_gray_dark_white = {'Dark': '#565656', 'Light': '#888888'}

        # OUR TABS
        self.tabs_container = customtkinter.CTkTabview(
            master=self.master_frame,
            corner_radius=9,
            width=812,
            height=336)

        self.tabs: [str] = ['TIME', 'MONTH', 'DAY WATCH', 'MONTH WATCH', 'SEASON', 'YEAR WATCH', 'GLOBAL TIME']

        [self.tabs_container.add(f'   {tab_name}   ') for tab_name in self.tabs]  # Spacing to stretch the seg.btn
        self.tabs_container.pack(fill='y', anchor='center', pady=(0, 8), padx=8)

        # INVOKING OUR TAB CLASSES
        TimeTab(self)
        CalendarTab(self)
        DayWatchTab(self)
        MonthWatchTab(self)
        YearWatchTab(self)
        SeasonTab(self)
        GlobalTimeTab(self)

        self.tab_widgets_colour_settings()

    def tab_widgets_colour_settings(self) -> None:
        """
        Keeping the tab widgets in sync with the current colour mode, for when the user switches system colour modes
        while the app is running.
        :return:
        """
        self.tabs_container.configure(segmented_button_fg_color=
                                      f'{self.darker_gray_white[customtkinter.get_appearance_mode()]}'
                                      , segmented_button_selected_hover_color=
                                      f'{self.darker_gray_white[customtkinter.get_appearance_mode()]}',
                                      segmented_button_unselected_color=
                                      f'{self.darker_gray_lighter_gray[customtkinter.get_appearance_mode()]}',
                                      segmented_button_unselected_hover_color=
                                      f'{self.mid_gray_lighter_gray[customtkinter.get_appearance_mode()]}'
                                      )

        self.after(100, self.tab_widgets_colour_settings)


class TimeTab(customtkinter.CTkFrame):
    """
    For rendering the local date and time (user's clicked_location / system clock).
    """

    def __init__(self, parent):
        customtkinter.CTkFrame.__init__(self, parent)

        self.parent = parent  # a reference to the window object class i.e. 'Watch'
        self.master: customtkinter.CTkTabview = parent.tabs_container.tab('   TIME   ')

        self.time_of_day_colour_codes: [str] = ['#009640', '#EA5B0C', '#BE1622', '#023049']

        self.month_label_colour_code = {'Dark': '#141414', 'Light': '#F2F2F2'}

        # SETTING UP OUR WIDGETS
        self.time_label = customtkinter.CTkLabel(master=self.master, text=f'00:00:01', font=('Arial', 200))
        self.time_label.grid()

        self.month_label = customtkinter.CTkLabel(master=self.master, text=f'Wednesday 2 1989',
                                                  font=('Arial', 38), corner_radius=10)

        self.month_label.grid(sticky='nsew', ipady=5)

        # CALLING THE FUNCTION TO PERIODICALLY UPDATE THE WIDGETS ABOVE
        self.time()

    def time(self) -> None:

        """
        Render the current time and update every second. Also render the widgets with colours corresponding to every 1/4
        of the day starting at midnight.
        :return: 
        """

        time_tab_local_time = datetime.datetime.now(tz=pytz.timezone(f'{get_localzone()}'))

        string_of_time: str = time_tab_local_time.strftime('%H:%M:%S')

        weekday_day_number: str
        today: str = time_tab_local_time.strftime('%A')
        month: str = time_tab_local_time.strftime('%B')

        time_of_day_colour_code: str = ''

        if string_of_time.startswith(('00', '01', '02', '03', '04', '05')):
            time_of_day_colour_code = self.time_of_day_colour_codes[0]
        elif string_of_time.startswith(('06', '07', '08', '09', '10', '11')):
            time_of_day_colour_code = self.time_of_day_colour_codes[1]
        elif string_of_time.startswith(('12', '13', '14', '15', '16', '17')):
            time_of_day_colour_code = self.time_of_day_colour_codes[2]
        elif string_of_time.startswith(('18', '19', '20', '21', '22', '23')):
            time_of_day_colour_code = self.time_of_day_colour_codes[3]

        if time_tab_local_time.strftime('%d').startswith('0'):
            weekday_day_number = time_tab_local_time.strftime('%d')[
                -1]  # If day starts with zero then strip the zero off.
        else:
            weekday_day_number = '%d'

        string_of_date: str = time_tab_local_time.strftime(f'{today} {weekday_day_number} {month}, %Y')

        self.time_label.configure(text=string_of_time, fg_color=time_of_day_colour_code, text_color='white')

        self.month_label.configure(text=string_of_date,
                                   text_color=time_of_day_colour_code,
                                   fg_color=f'{self.month_label_colour_code[customtkinter.get_appearance_mode()]}',
                                   bg_color=time_of_day_colour_code,
                                   )

        self.parent.tabs_container.configure(fg_color=time_of_day_colour_code,
                                             segmented_button_selected_color=time_of_day_colour_code,
                                             )

        self.after(100, self.time)


class CalendarTab(customtkinter.CTkFrame):
    """
    For rendering the calendar and week number count.
    """

    def __init__(self, parent):
        customtkinter.CTkFrame.__init__(self, parent)

        self.parent = parent
        self.master: customtkinter.CTkTabview = parent.tabs_container.tab('   MONTH   ')

        # MODES COLOUR MANAGEMENT
        self.frame_background = {'Dark': '#181818', 'Light': '#F2F2F2'}
        self.cal_background = {'Dark': '#FFFFFF', 'Light': '#232323'}
        self.headers_foreground = {'Dark': '#343434', 'Light': '#FFFFFF'}
        self.border_color = {'Dark': '#232323', 'Light': '#232323'}
        self.weekend_foreground = {'Dark': '#232323', 'Light': '#FFFFFF'}
        self.other_month_foreground = {'Dark': '#FFFFFF', 'Light': '#999999'}

        self.tab_month_frame = customtkinter.CTkFrame(
            master=self.master,
            bg_color=f'{self.frame_background[customtkinter.get_appearance_mode()]}')
        self.tab_month_frame.grid()

        self.week_number_count = customtkinter.CTkLabel(
            self.tab_month_frame,
            text='WEEK #\n 1',
            text_color=f'{self.parent.white_darker_gray[customtkinter.get_appearance_mode()]}',
            font=('Arial', 40, 'bold'),
            corner_radius=10)

        self.week_number_count.grid(row=0, column=0, padx=(85, 0), ipadx=5)

        # CALENDAR
        self.month_date_cal = Calendar(
            self.tab_month_frame,
            selectmode='none',
            font=("Arial", 18),
            background=f'{self.cal_background[customtkinter.get_appearance_mode()]}',
            foreground=f'{self.parent.darker_gray_white[customtkinter.get_appearance_mode()]}',
            firstweekday='sunday',
            showweeknumbers=False,
            headersforeground=f'{self.headers_foreground[customtkinter.get_appearance_mode()]}',
            bordercolor=f'{self.border_color[customtkinter.get_appearance_mode()]}',
            selectbackground_color=f'{self.parent.white_darker_gray[customtkinter.get_appearance_mode()]}',
            selectforeground_color=f'{self.parent.darker_gray_lighter_gray[customtkinter.get_appearance_mode()]}',
            normalforeground=f'{self.parent.darker_gray_white[customtkinter.get_appearance_mode()]}',
            normalbackground=f'{self.parent.white_darker_gray[customtkinter.get_appearance_mode()]}',
            weekendforeground=f'{self.weekend_foreground[customtkinter.get_appearance_mode()]}',
            othermonthforeground=f'{self.other_month_foreground[customtkinter.get_appearance_mode()]}',
            othermonthweforeground=f'{self.other_month_foreground[customtkinter.get_appearance_mode()]}',
        )

        self.month_date_cal.grid(column=1, row=0, padx=(108, 0), pady=(5, 10))

        self.month()

    def month(self) -> None:
        """
        Calculate week number and render it.
        :return: 
        """

        calendar_tab_local_time: datetime = datetime.datetime.now(tz=pytz.timezone(f'{get_localzone()}'))

        week_number = datetime.datetime.isocalendar(calendar_tab_local_time)[1]
        self.week_number_count.configure(text=f'WEEK #\n{week_number}')

        self.after(100, self.month)


class DayWatchTab(customtkinter.CTkFrame):
    """
    Tracking the number of hours, minutes & seconds remaining in a day.
    """

    def __init__(self, parent):
        customtkinter.CTkFrame.__init__(self, parent)

        self.master: customtkinter.CTkTabview = parent.tabs_container.tab('   DAY WATCH   ')

        self.hours_remaining_label = customtkinter.CTkLabel(master=self.master,
                                                            text=f'HOURS\nREMAINING\nFOR TODAY',
                                                            font=('Arial', 30))

        self.hours_remaining_label.grid(row=0, column=0, padx=(5, 0), pady=(25, 0))

        self.hour_frame = customtkinter.CTkFrame(master=self.master)

        self.hour_frame.grid(row=0, column=1, padx=(10, 0), pady=(40, 0))

        self.time_digits_label = customtkinter.CTkLabel(self.hour_frame,
                                                        text=f'00:00:01',
                                                        font=('Arial', 150))

        self.time_digits_label.grid(row=0, column=0, columnspan=3)

        self.hours_sub_label = customtkinter.CTkLabel(self.hour_frame,
                                                      text='HOURS',
                                                      font=('Arial', 11),
                                                      padx=15)
        self.hours_sub_label.grid(row=1, column=0)

        self.minutes_sub_label = customtkinter.CTkLabel(self.hour_frame,
                                                        text='MINUTES',
                                                        font=('Arial', 11), )
        self.minutes_sub_label.grid(row=1, column=1)

        self.seconds_sub_label = customtkinter.CTkLabel(self.hour_frame,
                                                        text='SECONDS',
                                                        font=('Arial', 11),
                                                        padx=17)
        self.seconds_sub_label.grid(row=1, column=2)

        self.day_hourly_countdown()

    def day_hourly_countdown(self) -> None:
        """
        Subtracting the current time from the time of a complete day and rendering the difference as a countdown.
        :return:
        """

        day_watch_local_time = datetime.datetime.now(tz=pytz.timezone(f'{get_localzone()}'))

        string_of_remaining_time = f'{23 - int(day_watch_local_time.strftime("%H"))}:' \
                                   f'{59 - int(day_watch_local_time.strftime("%M"))}:' \
                                   f'{60 - int(day_watch_local_time.strftime("%S"))} '

        #  Splitting the string on the colon ':' so that I can convert it to a list; get the last number (the second),
        #  add a zero if it is less than 10. This is so the alternating time string lengths do not affect Tkinter
        #  widget layouts.

        string_of_remaining_time_split = list(string_of_remaining_time.split(':'))

        new_string_of_remaining_time = []

        for time_digit in string_of_remaining_time_split:
            if int(time_digit) < 10:
                new_time_digit = str(0) + time_digit
                new_string_of_remaining_time.append(new_time_digit)
            else:
                new_string_of_remaining_time.append(time_digit)

        self.time_digits_label.configure(text=f'{new_string_of_remaining_time[0]}:{new_string_of_remaining_time[1]}:'
                                              f'{new_string_of_remaining_time[2]}')

        self.after(100, self.day_hourly_countdown)


class MonthWatchTab(customtkinter.CTkFrame):
    """
    Counting down the current month's days.
    """

    def __init__(self, parent):
        customtkinter.CTkFrame.__init__(self, parent)

        self.master: customtkinter.CTkTabview = parent.tabs_container.tab('   MONTH WATCH   ')

        self.month_remaining_days_label = customtkinter.CTkLabel(master=self.master,
                                                                 text=f'DAYS REMAINING\nFOR THIS MONTH',
                                                                 font=('Arial', 55))

        self.month_remaining_days_label.grid(row=0, column=0, pady=(0, 40), padx=(5, 0))

        self.days_in_month_frame = customtkinter.CTkFrame(master=self.master)

        self.days_in_month_frame.grid(row=0, column=1, padx=(32, 0))

        self.days_label = customtkinter.CTkLabel(self.days_in_month_frame, text='29',
                                                 font=('Arial', 220),
                                                 width=256)

        self.days_label.grid(row=0, column=0, padx=5)

        self.day_fraction_lapsed_label = customtkinter.CTkLabel(self.days_in_month_frame,
                                                                text=f'& LEKETLO (1/4)\n',  # 'LEKETLO' -> 'QUARTER'
                                                                font=('Arial', 20))

        self.day_fraction_lapsed_label.grid(row=1, column=0, pady=(0, 20), ipadx=10)

        self.month_daily_countdown()

    def month_daily_countdown(self) -> None:

        """
        Calculate the month's days and day fractions.
        :return:
        """

        month_countdown_local_time = datetime.datetime.now(tz=pytz.timezone(f'{get_localzone()}'))

        string_of_remaining_days: str = ''

        month_number: int = int(month_countdown_local_time.strftime("%m"))
        day_number: int = int(month_countdown_local_time.strftime("%d"))
        hour_number: int = int(month_countdown_local_time.strftime("%H"))

        # Matching current month decimal to its length & subtracting current day decimal to determine the
        # number of days remaining.
        if month_number in [1, 3, 5, 7, 8, 10, 12]:  # For 31 Day Months
            string_of_remaining_days = str(31 - day_number)

        elif month_number in [4, 6, 9, 11]:  # For 30 Day Months
            string_of_remaining_days = str(30 - day_number)

        elif month_number == 2:  # Accounting for Year length variations: [Wink wink! 2024 ;)]
            string_of_remaining_days = str(
                29 - day_number) if datetime.date.today().year % 4 == 0 else str(28 - day_number)

        self.days_label.configure(text=string_of_remaining_days)

        # Accounting for the hours. We 'count' a time fraction only after it has lapsed.
        if hour_number < 12:  # Before 12 Noon - we have about 3/4 of day remaining.
            self.day_fraction_lapsed_label.configure(text='& THREE QUARTERS (3/4)')
        elif hour_number >= 18:
            self.day_fraction_lapsed_label.configure(text='& A QUARTER (1/4)')
        elif hour_number >= 12:
            self.day_fraction_lapsed_label.configure(text='& A HALF (1/2)')

        self.after(60000, self.month_daily_countdown)  # Updates every minute.


class SeasonTab(customtkinter.CTkFrame):
    """
    Determine the season based on the user's hemisphere.
    """

    def __init__(self, parent):
        customtkinter.CTkFrame.__init__(self, parent)

        self.master = parent.tabs_container.tab('   SEASON   ')

        self.month_string: int = int(datetime.datetime.now(tz=pytz.timezone(f'{get_localzone()}')).strftime('%m'))

        self.seasons_colour_codes = {'Summer': '#EF7D00', 'Autumn': '#A83C16', 'Winter': '#11477C', 'Spring': '#23681D'}

        # RADIO BUTTONS VARIABLE & SETTINGS
        self.hemisphere: [str] = ['Southern', 'Northern']
        self.southern_northern: StringVar = StringVar()
        self.southern_northern.set(self.hemisphere[0])  # Setting a default value

        self.season_frame = customtkinter.CTkFrame(master=self.master,
                                                   fg_color=self.seasons_colour_codes['Spring'],
                                                   height=276,
                                                   bg_color=self.seasons_colour_codes['Spring'])

        self.season_frame.grid(pady=(0, 15))

        self.hemisphere_switch_1 = customtkinter.CTkRadioButton(master=self.season_frame,
                                                                text='Southern Hemisphere',
                                                                text_color='#FFFFFF',
                                                                font=('Arial', 15, 'bold'),
                                                                border_width_checked=4,
                                                                border_width_unchecked=2,
                                                                fg_color='#FFFFFF',
                                                                border_color='#FFFFFF',
                                                                radiobutton_width=15,
                                                                radiobutton_height=15,
                                                                hover_color='#FFFFFF',
                                                                variable=self.southern_northern,
                                                                value=self.hemisphere[0])

        self.hemisphere_switch_1.grid(row=0, column=0, pady=(10, 0), padx=(0, 200))

        self.hemisphere_switch_2 = customtkinter.CTkRadioButton(master=self.season_frame,
                                                                text='Northern Hemisphere',
                                                                text_color='#343434',
                                                                font=('Arial', 15, 'bold'),
                                                                border_width_checked=4,
                                                                border_width_unchecked=2,
                                                                border_color='#343434',
                                                                fg_color='#FFFFFF',
                                                                radiobutton_width=15,
                                                                radiobutton_height=15,
                                                                hover_color='#FFFFFF',
                                                                variable=self.southern_northern,
                                                                value=self.hemisphere[1])

        self.hemisphere_switch_2.grid(row=0, column=0, pady=(10, 0), padx=(200, 0))

        self.season_label = customtkinter.CTkLabel(master=self.season_frame,
                                                   text='SPRING',
                                                   font=('Arial', 170, 'bold'),
                                                   text_color='#FFFFFF',
                                                   width=784)

        self.season_label.grid(ipady=5, ipadx=5, pady=(15, 50))

        self.current_season_name = ''
        self.current_season_name_color = ''
        self.current_season_colour = ''

        self.latitude = 0

        self.season()

    def season(self) -> None:

        """
        Matching month number and timezone to corresponding season. The seasons are reversed between the hemispheres.
        :return:
        """

        if self.month_string in [12, 1, 2]:
            if self.southern_northern.get() == 'Southern':
                self.current_season_name = 'SUMMER'
                self.current_season_colour = self.seasons_colour_codes['Summer']
            else:
                self.current_season_name = 'WINTER'
                self.current_season_colour = self.seasons_colour_codes['Winter']

        elif self.month_string in [3, 4, 5]:
            if self.southern_northern.get() == 'Southern':
                self.current_season_name = 'AUTUMN'
                self.current_season_colour = self.seasons_colour_codes['Autumn']
            else:
                self.current_season_name = 'SPRING'
                self.current_season_colour = self.seasons_colour_codes['Spring']

        elif self.month_string in [6, 7, 8]:
            if self.southern_northern.get() == 'Southern':
                self.current_season_name = 'WINTER'
                self.current_season_colour = self.seasons_colour_codes['Winter']
            else:
                self.current_season_name = 'SUMMER'
                self.current_season_colour = self.seasons_colour_codes['Summer']

        elif self.month_string in [9, 10, 11]:
            if self.southern_northern.get() == 'Southern':
                self.current_season_name = 'SPRING'
                self.current_season_colour = self.seasons_colour_codes['Spring']
            else:
                self.current_season_name = 'AUTUMN'
                self.current_season_colour = self.seasons_colour_codes['Autumn']

        self.season_label.configure(text=self.current_season_name)
        self.season_frame.configure(fg_color=self.current_season_colour, bg_color=self.current_season_colour)

        if self.southern_northern.get() == 'Southern':
            self.hemisphere_switch_1.configure(text_color='#FFFFFF', border_color='#FFFFFF', )
            self.hemisphere_switch_2.configure(text_color='#343434', border_color='#343434', )
        elif self.southern_northern.get() == 'Northern':
            self.hemisphere_switch_1.configure(text_color='#343434', border_color='#343434', )
            self.hemisphere_switch_2.configure(text_color='#FFFFFF', border_color='#FFFFFF', )

        self.after(1000, self.season)


class YearWatchTab(customtkinter.CTkFrame):
    """
    Tracking the year's passed days and remaining days.
    """

    def __init__(self, parent):
        customtkinter.CTkFrame.__init__(self, parent)

        self.parent = parent
        self.master = parent.tabs_container.tab('   YEAR WATCH   ')
        self.mid_gray_light_gray = {'Dark': '#565656', 'Light': '#777'}

        self.button_values: [str] = ['left', 'passed']
        self.left_or_passed_days: StringVar = StringVar()
        self.left_or_passed_days.set(self.button_values[0])

        self.radio_btn_master_frame = customtkinter.CTkFrame(master=self.master)
        self.radio_btn_master_frame.grid()

        self.days_remaining_button = customtkinter.CTkRadioButton(master=self.radio_btn_master_frame,
                                                                  text='DAYS\nREMAINING\nTHIS YEAR',
                                                                  font=('Arial', 39.45),
                                                                  bg_color='#A50707',
                                                                  border_width_checked=6,
                                                                  border_width_unchecked=2,
                                                                  radiobutton_width=40,
                                                                  border_color='#FFFFFF',
                                                                  hover_color='#A50707',
                                                                  variable=self.left_or_passed_days,
                                                                  value=self.button_values[0])

        self.days_passed_button = customtkinter.CTkRadioButton(master=self.radio_btn_master_frame,
                                                               text='DAYS\nPASSED\nTHIS YEAR',
                                                               font=('Arial', 42.48),
                                                               bg_color='#064723',
                                                               border_width_checked=6,
                                                               border_width_unchecked=2,
                                                               radiobutton_width=40,
                                                               hover_color='#064723',
                                                               variable=self.left_or_passed_days,
                                                               value=self.button_values[1])

        self.days_remaining_button.grid(row=0, column=0, pady=(0, 156), padx=(0, 2))
        self.days_passed_button.grid(row=0, column=0, pady=(122, 0))

        self.year_days_countdown_frame = customtkinter.CTkFrame(master=self.radio_btn_master_frame)

        self.year_days_countdown_frame.grid(row=0, column=1, pady=(0, 10))

        self.day_count_label = customtkinter.CTkLabel(master=self.year_days_countdown_frame,
                                                      text='365',
                                                      font=("Arial", 225),
                                                      width=530)

        self.hour_count_label = customtkinter.CTkLabel(master=self.year_days_countdown_frame,
                                                       text='DIOURA 00:00:01',
                                                       # "DIOURA" is a SeTswana word for "HOURS"
                                                       font=("Arial", 23),
                                                       )

        self.day_count_label.grid()
        self.hour_count_label.grid()

        self.year_daily_countdown()

    def year_daily_countdown(self) -> None:

        """
        Tracking the number of days for the year.
        :return:
        """

        year_watch_tab_local_time = datetime.datetime.now(tz=pytz.timezone(f'{get_localzone()}'))

        # Last Day of the year minus today.
        days_left = f'{str(datetime.date(int(year_watch_tab_local_time.strftime("%Y")), 12, 31) - datetime.date.today()).split(",")[0][:-4].strip()}'
        hours_left = f'HOURS {23 - int(year_watch_tab_local_time.strftime("%H"))}:' \
                     f'{59 - int(year_watch_tab_local_time.strftime("%M"))}:' \
                     f'{60 - int(year_watch_tab_local_time.strftime("%S"))} '

        if days_left.startswith('0'):
            days_left = '0'

        if datetime.date.today().year % 4 == 0:  # Leap Year
            year_type = 365  # Shorting the day to account for the hours.
        else:
            year_type = 364  # Ordinary year

        days_passed = f'{year_type - int(days_left)}'

        hours_passed = f'HOURS {year_watch_tab_local_time.strftime("%H:%M:%S")}'

        if self.left_or_passed_days.get() == 'left':
            # Days Left
            self.day_count_label.configure(text=days_left, bg_color='#E30613', text_color='#FFFFFF')
            self.hour_count_label.configure(text=hours_left, bg_color='#E30613', text_color='#FFFFFF')
            self.radio_btn_master_frame.configure(fg_color='#E30613')
            self.year_days_countdown_frame.configure(fg_color='#E30613')
            self.days_remaining_button.configure(bg_color='#A50707', fg_color='#FFFFFF', text_color='#FFFFFF')
            self.days_passed_button.configure(
                bg_color=f'{self.parent.dark_gray_lighter_gray[customtkinter.get_appearance_mode()]}',
                fg_color=f'{self.parent.light_gray_white[customtkinter.get_appearance_mode()]}',
                text_color=f'{self.parent.light_gray_dark_white[customtkinter.get_appearance_mode()]}',
                border_color=f'{self.mid_gray_light_gray[customtkinter.get_appearance_mode()]}')

        elif self.left_or_passed_days.get() == 'passed':
            # Days Passed
            self.day_count_label.configure(text=days_passed, bg_color='#026833')
            self.hour_count_label.configure(text=hours_passed, bg_color='#026833')
            self.radio_btn_master_frame.configure(fg_color='#026833')
            self.year_days_countdown_frame.configure(fg_color='#026833')
            self.days_remaining_button.configure(
                bg_color=f'{self.parent.dark_gray_lighter_gray[customtkinter.get_appearance_mode()]}',
                fg_color=f'{self.parent.light_gray_white[customtkinter.get_appearance_mode()]}',
                text_color=f'{self.parent.light_gray_dark_white[customtkinter.get_appearance_mode()]}',
                border_color=f'{self.mid_gray_light_gray[customtkinter.get_appearance_mode()]}')
            self.days_passed_button.configure(bg_color='#064723', fg_color='#FFFFFF', text_color='#FFFFFF')

        self.after(100, self.year_daily_countdown)


class GlobalTimeTab(customtkinter.CTkFrame):
    """
    Keep time from several points across the world. Regions represented include Africa, America, Asia, Australia, Europe
    & Pacific. An array of timezones is represented ~ (GMT -> GMT-13).
    """

    def __init__(self, parent):
        customtkinter.CTkFrame.__init__(self, parent)

        self.master = parent.tabs_container.tab('   GLOBAL TIME   ')

        # FOR MODES SWITCHING
        self.frame_bg_color = {'Dark': '#292929', 'Light': '#D8D8D8'}
        self.place_label_mode = {'Dark': '#161616', 'Light': '#FFFFFF'}
        self.disabled_text_colour = {'Dark': '#747474', 'Light': '#888888'}
        self.enabled_text_colour = {'Dark': '#FFFFFF', 'Light': '#333333'}

        self.active_zones_frame = customtkinter.CTkFrame(
            master=self.master,
            fg_color=f'{self.frame_bg_color[customtkinter.get_appearance_mode()]}'
        )

        self.active_zones_frame.grid(row=0, column=0, padx=(25, 0), pady=(12, 10))

        self.zones_listing = customtkinter.CTkScrollableFrame(master=self.master,
                                                              label_text='SELECT TIMEZONE',
                                                              label_font=('Arial', 15, 'bold'))
        self.zones_listing.grid(row=0, column=2, padx=(35, 6), pady=10)

        # DATABASE SET-UP
        self.db_connection: Connection = sqlite3.connect(resource_path('..\\Timezones Database.db'))
        self.cursor: Cursor = self.db_connection.cursor()

        self.render_timezone_checkboxes()  # For displaying all the checkboxes for all the locations
        self.select_render_active_zones()  # For selecting & rendering the check_boxes for the locations that are active
        self.global_time()  # For periodically refreshing the displayed widgets

    def location_timezone_switch(self, clicked_location, checkbox_state) -> None:

        """
        Manage the swapping of timezone watches on the global times display panel
        :param clicked_location:  The location name from the checkbox that was just clicked
        :param checkbox_state: The state of the checkbox button after the click (0 for deselected and 1 for selected)
        :return:
        """

        all_listed_zones = self.zones_listing.winfo_children()

        if checkbox_state == 0:  # Unchecked

            # RAISE ALERT (Modified the library's CTkInputDialog to create this Message Box, might behave trippy.)
            customtkinter.CTkMessageBox(title='Remove Timezone',
                                        text='Please select the timezone you want to replace '
                                             f'\'{clicked_location.replace("_", " ")}\' with. ',
                                        )

            # Make the currently selected checkboxes in-active & make the unselected ones active for possible selection
            for zone_widget in all_listed_zones:  # for the just-unselected
                zone_widget.configure(state='disabled') if zone_widget.get() == 1 or zone_widget.cget('text') == \
                                                           clicked_location else zone_widget.configure(state='normal',
                                                                                                       text_color=
                                                                                                       self.enabled_text_colour[
                                                                                                           customtkinter.get_appearance_mode()])

            # Match the clicked location (checkbox) with its corresponding displayed timezone and remove the widget
            for child_frame in self.active_zones_frame.winfo_children():
                for sub_child in child_frame.winfo_children():
                    if '!ctklabel3' in str(sub_child) and sub_child.cget(  # '!ctklabel3' is the location label
                            'text') == clicked_location.upper().replace('_', ' '):
                        child_frame.destroy()

        elif checkbox_state == 1:  # Checked

            grid_coordinates = 0

            if clicked_location == 'Buenos_Aires':
                clicked_location = 'Argentina/' + clicked_location

            # Swap the in-active and active states of the checked & the unchecked checkboxes
            for zone in all_listed_zones:
                zone.configure(state='normal',
                               text_color=self.enabled_text_colour[customtkinter.get_appearance_mode()]) \
                    if zone.get() == 1 else zone.configure(state='disabled')

            selected_timezones = self.read_timezone(self.db_connection, status=1)

            # Get the removed location's 'grid spot' tuple and update its 'status' to zero (0) i.e. not displayed
            for check_box in all_listed_zones:
                for timezone in selected_timezones:
                    if check_box.cget('text') in timezone[0] and check_box.get() == 0:
                        grid_coordinates = timezone[1]  # grid coordinates column from the DB

                        # Update DB to reset the clicked_location (removed location) status to 0
                        removed_location = timezone[0]  # location name column from the DB
                        self.update_timezone(self.db_connection, new_status=str(0),
                                             timezone_location=removed_location)

            # Update the DB record for the newly selected (checked) timezone checkbox
            self.update_timezone(self.db_connection, new_status=checkbox_state, timezone_location=clicked_location,
                                 grid_spot=grid_coordinates)

            self.render_active_zones(clicked_location, row=grid_coordinates[0], col=grid_coordinates[-1],
                                     grid_status=False)

            customtkinter.CTkMessageBox(
                title='Done!',
                text=f'You have successfully added \'{clicked_location.split("/")[-1].replace("_", " ")}\' '
                     f'time to your global times display panel!')

    def render_active_zones(self, timezone=None, row=0, col=0, grid_status=True) -> None:

        """
        For creating all the widgets for displaying each active timezone on the global time panel.
        :param timezone: The location / timezone name from either the database or the clicked checkbox
        :param row: The row for the parent (at this level) widget to be displayed
        :param col: The column for the parent widget
        :param grid_status: A control param for distinguishing between startup widget displays and live widget updates
        :return:
        """

        global_time_tab_local_time = datetime.datetime.now(tz=pytz.timezone(f'{get_localzone()}'))

        all_zones_widgets = self.zones_listing.winfo_children()

        display_panel_timezones: [] = []

        # FILTER ~ picking what to render
        for child_zone in all_zones_widgets:
            if grid_status:  # For rendering all the active timezones at startup
                if child_zone.get() == 1:
                    display_panel_timezones.append(child_zone)
            else:  # For rendering the newly selected / activated timezone
                if child_zone.cget('text') == timezone.split('/')[-1]:
                    display_panel_timezones.append(child_zone)  # This list will always be of len() >> 1

        # RENDER
        for _ in display_panel_timezones:
            grid_zone_frame = customtkinter.CTkFrame(master=self.active_zones_frame)
            grid_zone_frame.grid(row=row, column=col, padx=5, pady=10)

            time_grid_zone_label = customtkinter.CTkLabel(master=grid_zone_frame,
                                                          text=global_time_tab_local_time.strftime('%H:%M:%S'),
                                                          text_color='#FFFFFF',
                                                          font=('Arial', 15, 'bold'),
                                                          padx=12
                                                          )

            date_grid_zone_time_label = customtkinter.CTkLabel(master=grid_zone_frame,
                                                               text='LB2 10, FIR',
                                                               text_color='#FFFFFF',
                                                               # SeTswana shorthand date translating to: "Tue 10, JAN"
                                                               font=('Arial', 10),
                                                               )

            location_grid_zone_time_label = customtkinter.CTkLabel(
                master=grid_zone_frame,
                text=timezone.upper().replace("_", ' ').split('/')[-1],
                text_color='#FFFFFF',
                font=('Arial', 12, 'bold'), padx=12,
                width=110
            )

            time_grid_zone_label.grid(row=0, column=col)
            date_grid_zone_time_label.grid(row=1, column=col)
            location_grid_zone_time_label.grid(row=2, column=col)

    def render_timezone_checkboxes(self) -> None:

        """
        Rendering each checkbox, with 5 cities from each timezone region. Rendering in an iterator causes
        problems with the checkboxes acting in unison and also returns only the last checkbox text and other issues.
        :return:
        """

        # AFRICA
        zone_accra = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "Accra")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_accra.cget('text'), zone_accra.get()))

        zone_accra.grid(pady=5, padx=2, sticky='w')

        zone_addis_ababa = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "Addis_Ababa")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_addis_ababa.cget('text'),
                                                          zone_addis_ababa.get()))

        zone_addis_ababa.grid(pady=5, padx=2, sticky='w')

        zone_cairo = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "Cairo")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_cairo.cget('text'), zone_cairo.get()))

        zone_cairo.grid(pady=5, padx=2, sticky='w')

        zone_gaborone = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "Gaborone")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_gaborone.cget('text'), zone_gaborone.get()))

        zone_gaborone.grid(pady=5, padx=2, sticky='w')

        zone_lagos = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "Lagos")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_lagos.cget('text'), zone_lagos.get()))

        zone_lagos.grid(pady=5, padx=2, sticky='w')

        # AMERICA
        zone_buenos_aires = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "Argentina/Buenos_Aires")[1].split("/")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_buenos_aires.cget('text'),
                                                          zone_buenos_aires.get()))

        zone_buenos_aires.grid(pady=5, padx=2, sticky='w')

        zone_barbados = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "Barbados")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_barbados.cget('text'),
                                                          zone_barbados.get()))

        zone_barbados.grid(pady=5, padx=2, sticky='w')

        zone_los_angeles = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "Los_Angeles")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_los_angeles.cget('text'),
                                                          zone_los_angeles.get()))

        zone_los_angeles.grid(pady=5, padx=2, sticky='w')

        zone_montserrat = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "Montserrat")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_montserrat.cget('text'),
                                                          zone_montserrat.get()))

        zone_montserrat.grid(pady=5, padx=2, sticky='w')

        zone_new_york = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "New_York")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_new_york.cget('text'),
                                                          zone_new_york.get()))

        zone_new_york.grid(pady=5, padx=2, sticky='w')

        # ASIA
        zone_bangkok = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "Bangkok")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_bangkok.cget('text'),
                                                          zone_bangkok.get()))

        zone_bangkok.grid(pady=5, padx=2, sticky='w')

        zone_hong_kong = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "Hong_Kong")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_hong_kong.cget('text'),
                                                          zone_hong_kong.get()))

        zone_hong_kong.grid(pady=5, padx=2, sticky='w')

        zone_seoul = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "Seoul")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_seoul.cget('text'), zone_seoul.get()))

        zone_seoul.grid(pady=5, padx=2, sticky='w')

        zone_shanghai = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "Shanghai")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_shanghai.cget('text'),
                                                          zone_shanghai.get()))

        zone_shanghai.grid(pady=5, padx=2, sticky='w')

        zone_tokyo = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "Tokyo")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_tokyo.cget('text'), zone_tokyo.get()))

        zone_tokyo.grid(pady=5, padx=2, sticky='w')

        # AUSTRALIA
        zone_adelaide = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "Adelaide")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_adelaide.cget('text'),
                                                          zone_adelaide.get()))

        zone_adelaide.grid(pady=5, padx=2, sticky='w')

        zone_darwin = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "Darwin")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_darwin.cget('text'),
                                                          zone_darwin.get()))

        zone_darwin.grid(pady=5, padx=2, sticky='w')

        zone_melbourne = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "Melbourne")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_melbourne.cget('text'),
                                                          zone_melbourne.get()))

        zone_melbourne.grid(pady=5, padx=2, sticky='w')

        zone_perth = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "Perth")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_perth.cget('text'), zone_perth.get()))

        zone_perth.grid(pady=5, padx=2, sticky='w')

        zone_sydney = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "Sydney")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_sydney.cget('text'),
                                                          zone_sydney.get()))

        zone_sydney.grid(pady=5, padx=2, sticky='w')

        # EUROPE
        zone_amsterdam = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "Amsterdam")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_amsterdam.cget('text'),
                                                          zone_amsterdam.get()))

        zone_amsterdam.grid(pady=5, padx=2, sticky='w')

        zone_helsinki = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "Helsinki")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_helsinki.cget('text'),
                                                          zone_helsinki.get()))

        zone_helsinki.grid(pady=5, padx=2, sticky='w')

        zone_london = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "London")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_london.cget('text'),
                                                          zone_london.get()))

        zone_london.grid(pady=5, padx=2, sticky='w')

        zone_moscow = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "Moscow")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_moscow.cget('text'),
                                                          zone_moscow.get()))

        zone_moscow.grid(pady=5, padx=2, sticky='w')

        zone_zurich = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "Zurich")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_zurich.cget('text'),
                                                          zone_zurich.get()))

        zone_zurich.grid(pady=5, padx=2, sticky='w')

        # PACIFIC
        zone_auckland = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "Auckland")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_auckland.cget('text'),
                                                          zone_auckland.get()))

        zone_auckland.grid(pady=5, padx=2, sticky='w')

        zone_fiji = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "Fiji")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_fiji.cget('text'), zone_fiji.get()))

        zone_fiji.grid(pady=5, padx=2, sticky='w')

        zone_Honolulu = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "Honolulu")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_Honolulu.cget('text'),
                                                          zone_Honolulu.get()))

        zone_Honolulu.grid(pady=5, padx=2, sticky='w')

        zone_tahiti = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "Tahiti")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_tahiti.cget('text'),
                                                          zone_tahiti.get()))

        zone_tahiti.grid(pady=5, padx=2, sticky='w')

        zone_wallis = customtkinter.CTkCheckBox(
            master=self.zones_listing,
            text=f'{self.read_timezone(self.db_connection, "Wallis")[1]}',
            font=('Arial', 14, 'bold'),
            state='DISABLED',
            text_color=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            text_color_disabled=f'{self.disabled_text_colour[customtkinter.get_appearance_mode()]}',
            command=lambda: self.location_timezone_switch(zone_wallis.cget('text'),
                                                          zone_wallis.get()))

        zone_wallis.grid(pady=5, padx=2, sticky='w')

    def select_render_active_zones(self) -> None:

        """
        Read the database records and update each check_box's selection based on its status, then render all the active
        timezones on the global time display panel.
        :return:
        """

        for full_record in self.read_timezone(self.db_connection):
            if full_record[3] == 1:
                row = full_record[-2][0]
                column = full_record[-2][2]

                for zone in self.zones_listing.winfo_children():

                    buenos_aires_zone_name = 'Argentina/' if zone.cget('text') == 'Buenos_Aires' else ''

                    if buenos_aires_zone_name + zone.cget('text') == full_record[1]:
                        zone.select()
                        zone.configure(state='normal',
                                       text_color=self.enabled_text_colour[customtkinter.get_appearance_mode()])

                self.render_active_zones(full_record[1].split('/')[-1].replace('_', ' ').upper(), row, column)

    def global_time(self) -> None:

        """
        Keeps each panel updated with the current time for its respective timezone region and the colour code to match
        time of day.
        :return:
        """

        timezones = []
        for record in self.read_timezone(self.db_connection):
            if record[-3] == 1:
                timezone = f'{record[0]}/{record[1]}'
                timezones.append(timezone)

        all_the_days: [str] = []
        day_num: [str] = []
        month_abbreviations: [str] = []
        time_of_day_colour_codes: [str] = []

        # Getting the day name abbreviation, day's date and month name abbreviation
        for timezone in timezones:
            today: str = datetime.datetime.now(tz=pytz.timezone(timezone)).strftime('%a')
            all_the_days.append(today.upper())

            current_month_day: str = datetime.datetime.now(tz=pytz.timezone(timezone)).strftime('%d')
            if current_month_day.startswith('0'):
                current_month_day.replace('0', '', 1)  # If day starts with zero then strip-off the zero
            day_num.append(current_month_day)

            current_month: str = datetime.datetime.now(tz=pytz.timezone(timezone)).strftime('%b')
            month_abbreviations.append(current_month.upper())

            # Updating colour codes to time of day on a quarterly basis starting off at 00:00:00
            if int(datetime.datetime.now(tz=pytz.timezone(timezone)).strftime('%H')) < 6:
                time_of_day_colour_codes.append('#009640')
            elif int(datetime.datetime.now(tz=pytz.timezone(timezone)).strftime('%H')) < 12:
                time_of_day_colour_codes.append('#EA5B0C')
            elif int(datetime.datetime.now(tz=pytz.timezone(timezone)).strftime('%H')) < 18:
                time_of_day_colour_codes.append('#BE1622')
            elif int(datetime.datetime.now(tz=pytz.timezone(timezone)).strftime('%H')) < 24:
                time_of_day_colour_codes.append('#023049')

        # Updating each timezone panel
        for ndx, timezone in enumerate(timezones):
            for child_frame in self.active_zones_frame.winfo_children():

                # Updating the Time
                if ':' in child_frame.winfo_children()[0].cget('text') and \
                        child_frame.winfo_children()[2].cget('text') \
                        == timezone.split('/')[1].replace('_', ' ').upper() or \
                        child_frame.winfo_children()[2].cget('text') == 'BUENOS AIRES':
                    child_frame.configure(bg_color=time_of_day_colour_codes[ndx],
                                          fg_color=time_of_day_colour_codes[ndx]
                                          )
                    child_frame.winfo_children()[0].configure(
                        text=datetime.datetime.now(tz=pytz.timezone(f'{timezones[ndx]}')).strftime('%H:%M:%S'),
                        fg_color=time_of_day_colour_codes[ndx]
                    )

                # Updating the Date
                if ',' in child_frame.winfo_children()[1].cget('text') and \
                        child_frame.winfo_children()[2].cget('text') \
                        == timezone.split('/')[1].replace('_', ' ').upper() or \
                        child_frame.winfo_children()[2].cget('text') == 'BUENOS AIRES':
                    child_frame.winfo_children()[1].configure(
                        text=f'{all_the_days[ndx]} {day_num[ndx]}, {month_abbreviations[ndx]}',
                        fg_color=time_of_day_colour_codes[ndx])

        # Updating widget colours in-case of live mode switching
        self.active_zones_frame.configure(fg_color=f'{self.frame_bg_color[customtkinter.get_appearance_mode()]}')

        for widget in self.active_zones_frame.winfo_children():
            for label in widget.winfo_children():
                if '!ctklabel3' in str(label):
                    label.configure(fg_color=f'{self.place_label_mode[customtkinter.get_appearance_mode()]}')

        for zone in self.zones_listing.winfo_children():
            if zone.get() == 1:
                zone.configure(text_color=self.enabled_text_colour[customtkinter.get_appearance_mode()])

        self.after(1000, self.global_time)  # Updates every second

    @staticmethod
    def read_timezone(db_connect, timezone_name=None, status=None):

        """
        Retrieve records based on the optional params provided depending on desired end result
        :param db_connect: Our database connection
        :param timezone_name: The location name of the record being accessed
        :param status: The display status of the record (selected / unselected)
        :return:
        """
        if not timezone_name and not status:
            timezone_record = db_connect.execute("SELECT * FROM TIMEZONES")
            return list(timezone_record)
        elif not status:
            timezone_record = db_connect.execute("SELECT * FROM TIMEZONES WHERE LOCATION LIKE (?)",
                                                 (f'%{timezone_name}%',))
            return timezone_record.fetchone()
        else:
            timezone_record = db_connect.execute("SELECT LOCATION, GRID_SPOT FROM TIMEZONES WHERE STATUS LIKE (?)",
                                                 (f'{status}',))
            return list(timezone_record)

    @staticmethod
    def update_timezone(db_connect, new_status: str, timezone_location: str, grid_spot: str = 'NULL') -> None:

        """
        Update the database at the record specified with the given arguments
        :param db_connect: The database connection
        :param new_status: The new display status with which to update the specified record / timezone
        :param timezone_location: The timezone location being updated
        :param grid_spot: The row and column information for the widget grid
        :return:
        """
        db_connect.execute(
            f"UPDATE TIMEZONES SET STATUS = '{new_status}', GRID_SPOT = '{grid_spot}' "
            f"WHERE LOCATION LIKE '{timezone_location}'")
        db_connect.commit()


def resource_path(relative_path) -> [str, bytes]:
    """
    For managing file resources.
    :param: relative_path: The relative path (relative to the script file) of the target file as a string
    :return: A list of bytes (file content) and string (file path)
    """

    base_path: [] = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
