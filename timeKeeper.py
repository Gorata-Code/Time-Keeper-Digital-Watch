import os
import sys
import pytz
import datetime
from tkinter import *
from tkinter import ttk
from tzlocal import get_localzone, get_localzone_name


local_time: datetime = datetime.datetime.now(tz=pytz.timezone(f'{get_localzone()}'))


def time() -> None:
    # Making sure locale time is always LOCAL.
    time_local_time: datetime = datetime.datetime.now(tz=pytz.timezone(f'{get_localzone()}'))

    string_of_time: str = time_local_time.strftime('%H:%M:%S')

    today: str = local_time.strftime('%A')
    weekday_day_number: str
    month: str = local_time.strftime('%B')

    if time_local_time.strftime('%d').startswith('0'):
        weekday_day_number = time_local_time.strftime('%d')[-1]  # If day starts with zero then strip the zero off.
    else:
        weekday_day_number = '%d'

    time_label.config(text=string_of_time)

    string_of_date: str = time_local_time.strftime(f'{today} {weekday_day_number} {month}, %Y')

    month_label.config(text=string_of_date)

    window.after(100, time)  # Update every tenth of a second


def season() -> None:

    global current_season

    local_timezone_name: str = get_localzone_name()

    summer_matte: PhotoImage = PhotoImage(file=f'{resource_path("")}Summer.png')
    autumn_matte: PhotoImage = PhotoImage(file=f'{resource_path("")}Autumn.png')
    winter_matte: PhotoImage = PhotoImage(file=f'{resource_path("")}Winter.png')
    spring_matte: PhotoImage = PhotoImage(file=f'{resource_path("")}Spring.png')

    southern_hemisphere: [str] = ['Africa/Cairo', 'Australia/Sydney', 'NZ']
    northern_hemisphere: [str] = ['Europe/London', 'US/Eastern', 'US/Pacific', 'Asia/Shanghai', 'Asia/Tokyo']

    month_string: int = int(datetime.datetime.now(tz=pytz.timezone(f'{get_localzone()}')).strftime('%m'))

    ''' 
    Matching month number and timezone to corresponding season. One limitation with this approach is using only a
    few timezones out of the more than 500 that pytz has, listed! The seasons are reversed between the hemispheres.
    '''
    if month_string == 12 or month_string == 1 or month_string == 2:
        if local_timezone_name in southern_hemisphere:
            current_season = summer_matte
        elif local_timezone_name in northern_hemisphere:
            current_season = winter_matte

    elif month_string == 3 or month_string == 4 or month_string == 5:
        if local_timezone_name in southern_hemisphere:
            current_season = autumn_matte
        elif local_timezone_name in northern_hemisphere:
            current_season = spring_matte

    elif month_string == 6 or month_string == 7 or month_string == 8:
        if local_timezone_name in southern_hemisphere:
            current_season = winter_matte
        elif local_timezone_name in northern_hemisphere:
            current_season = summer_matte

    elif month_string == 9 or month_string == 10 or month_string == 11:
        if local_timezone_name in southern_hemisphere:
            current_season = spring_matte
        elif local_timezone_name in northern_hemisphere:
            current_season = autumn_matte

    season_label.config(image=current_season)

    window.after(100, season)


def day_hourly_countdown() -> None:
    # Tracking the number of hours (minutes & seconds) remaining in a day.

    day_countdown_local_time: datetime = datetime.datetime.now(tz=pytz.timezone(f'{get_localzone()}'))

    string_of_remaining_time: str = f'{23 - int(day_countdown_local_time.strftime("%H"))}:' \
                                    f'{59 - int(day_countdown_local_time.strftime("%M"))}:' \
                                    f'{60 - int(day_countdown_local_time.strftime("%S"))} '

    '''
    Splitting the string on the colon so that I can convert it to a list; get the last number (the second),
    and a zero if it is less than 10. This is so the alternating time string lengths do not affect Tkinter widget
    layouts.
    '''
    string_of_remaining_time_split: [str] = list(string_of_remaining_time.split(':'))

    new_string_of_remaining_time: [str] = []

    for time_digit in string_of_remaining_time_split:
        if int(time_digit) < 10:
            new_time_digit: str = str(0) + time_digit
            new_string_of_remaining_time.append(new_time_digit)
        else:
            new_string_of_remaining_time.append(time_digit)

    hour_digits_label.config(text=f'{new_string_of_remaining_time[0]}:{new_string_of_remaining_time[1]}:'
                                  f'{new_string_of_remaining_time[2]}')

    window.after(100, day_hourly_countdown)


def month_daily_countdown() -> None:
    # Counting down the days of the month.

    month_countdown_local_time: datetime = datetime.datetime.now(tz=pytz.timezone(f'{get_localzone()}'))

    string_of_remaining_days: str = ''

    month_number: int = int(month_countdown_local_time.strftime("%m"))
    day_number: int = int(month_countdown_local_time.strftime("%d"))
    hour_number: int = int(month_countdown_local_time.strftime("%H"))

    # Matching current month decimal to its length & subtracting current day decimal to determine the remaining days.
    if month_number == 1 or month_number == 3 or month_number == 5 or month_number == 7 or month_number == 8 or month_number == 10 or month_number == 12:  # For 31 Day Months
        string_of_remaining_days = str(31 - day_number)

    elif month_number == month_number == 4 or month_number == 6 or month_number == 9 or month_number == 11:  # For 30 Day Months
        string_of_remaining_days = str(30 - day_number)

    elif month_number == 2:  # Accounting for Year length variations: Ordinary Years & Leap Years [Yay! 2024 ;)]
        if datetime.date.today().year % 4 == 0:
            string_of_remaining_days = str(29 - day_number)  # Leap Year
        else:
            string_of_remaining_days = str(28 - day_number)  # Ordinary Year

    days_label.config(text=string_of_remaining_days)

    if int(string_of_remaining_days) < 10:  # Dealing with a misalignment issue for single digits
        days_in_month_frame.config(padx=119)

    # Accounting for the hours. We 'count' a time fraction only after it has lapsed.
    if hour_number < 12:  # Before 12 Noon - we have about 3/4 of day remaining.
        day_fraction_lapsed_label.config(text='& THREE QUARTERS (3/4)')
    elif hour_number >= 18:
        day_fraction_lapsed_label.config(text='& A QUARTER (1/4)')
    elif hour_number >= 12:
        day_fraction_lapsed_label.config(text='& A HALF (1/2)')

    window.after(60000, month_daily_countdown)  # Updates every minute.


def year_daily_countdown() -> None:
    # Tracking the number of days till year's end.

    year_countdown_local_time: datetime = datetime.datetime.now(tz=pytz.timezone(f'{get_localzone()}'))

    # Last Day of the year minus today.
    days_left: str = f'{str(datetime.date(int(year_countdown_local_time.strftime("%Y")), 12, 31) - datetime.date.today()).split(",")[0][:-4].strip()} '
    hours_left: str = f'HOURS {23 - int(year_countdown_local_time.strftime("%H"))}:{59 - int(year_countdown_local_time.strftime("%M"))}:{60 - int(year_countdown_local_time.strftime("%S"))} '

    if days_left.startswith('0'):
        days_left: str = '0'

    year_type: int
    if datetime.date.today().year % 4 == 0:  # Leap Year
        year_type = 365  # Shorting the day to account for the hours.
    else:
        year_type = 364  # A day short. # Ordinary year

    days_passed: str = f'{year_type - int(days_left)}'
    hours_passed: str = f'HOURS {year_countdown_local_time.strftime("%H:%M:%S")}'

    '''
    We grid dot forget before we grid dot config to avoid Tkinter widget overlay issues. Other ideas I tried failed.
    We also made one label widget for the same reason (instead of one for each, I had originally done that).
    We use colour variations to draw distinctions between the buttons, I didn't want to make the buttons stand out.
    '''
    if left_or_passed_days.get() == 'left':
        day_count_label.grid_forget()
        hour_count_label.grid_forget()
        day_count_label.config(text=days_left, fg='red')
        hour_count_label.config(text=hours_left, fg='red')

    elif left_or_passed_days.get() == 'passed':
        day_count_label.grid_forget()
        hour_count_label.grid_forget()
        day_count_label.config(text=days_passed, fg='green')
        hour_count_label.config(text=hours_passed, fg='green')

    day_count_label.grid(row=0, column=0, columnspan=2)
    hour_count_label.grid(row=1, column=0)

    window.after(100, year_daily_countdown)


def international_time() -> None:
    # Tracking international time within 8 Timezones only. Three of the timezones trail UTC while the other 5 lead by up
    # to 12 Hours!

    international_local_time: datetime = datetime.datetime.now(tz=pytz.timezone(f'{get_localzone()}'))

    # Current Time at each timezone including current timezone, so expect duplication.
    time_localtime_label.config(text=international_local_time.strftime('%H:%M:%S'))
    time_london_label.config(text=datetime.datetime.now(tz=pytz.timezone('Europe/London')).strftime('%H:%M:%S'))
    time_new_york_label.config(
        text=datetime.datetime.now(tz=pytz.timezone('US/Eastern')).strftime('%H:%M:%S'))
    time_los_angeles_label.config(
        text=datetime.datetime.now(tz=pytz.timezone('US/Pacific')).strftime('%H:%M:%S'))
    time_shanghai_label.config(
        text=datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime('%H:%M:%S'))
    time_tokyo_label.config(text=datetime.datetime.now(tz=pytz.timezone('Asia/Tokyo')).strftime('%H:%M:%S'))
    time_sydney_label.config(
        text=datetime.datetime.now(tz=pytz.timezone('Australia/Sydney')).strftime('%H:%M:%S'))
    time_wellington_label.config(text=datetime.datetime.now(tz=pytz.timezone('NZ')).strftime('%H:%M:%S'))

    time_zones: [str] = ['Africa/Cairo', 'Europe/London', 'US/Eastern', 'US/Pacific', 'Asia/Shanghai', 'Asia/Tokyo',
                         'Australia/Sydney', 'NZ']

    all_the_days: [str] = []
    day_num: [str] = []
    month_abbreviations: [str] = []
    time_of_day_colour_codes: [str] = []

    # Getting the day name abbreviation, day's date and month name abbreviation.
    for timezone in time_zones:
        today: str = datetime.datetime.now(tz=pytz.timezone(timezone)).strftime('%a')
        all_the_days.append(today.upper())

        current_month_day: str = datetime.datetime.now(tz=pytz.timezone(timezone)).strftime('%d')
        if current_month_day.startswith('0'):
            current_month_day.replace('0', '', 1)  # If day starts with zero then strip the zero off
        day_num.append(current_month_day)

        current_month = datetime.datetime.now(tz=pytz.timezone(timezone)).strftime('%b')
        month_abbreviations.append(current_month.upper())

        # Assigning colour codes to time of day on a 6-hour basis.
        if int(datetime.datetime.now(tz=pytz.timezone(timezone)).strftime('%H')) < 6:
            time_of_day_colour_codes.append('blue')
        elif int(datetime.datetime.now(tz=pytz.timezone(timezone)).strftime('%H')) < 12:
            time_of_day_colour_codes.append('orange')
        elif int(datetime.datetime.now(tz=pytz.timezone(timezone)).strftime('%H')) < 18:
            time_of_day_colour_codes.append('green')
        elif int(datetime.datetime.now(tz=pytz.timezone(timezone)).strftime('%H')) < 24:
            time_of_day_colour_codes.append('red')

    place_localtime_time_label.config(bg=time_of_day_colour_codes[0])
    place_london_label.config(bg=time_of_day_colour_codes[1])
    place_new_york_label.config(bg=time_of_day_colour_codes[2])
    place_los_angeles_label.config(bg=time_of_day_colour_codes[3])
    place_shanghai_label.config(bg=time_of_day_colour_codes[4])
    place_tokyo_label.config(bg=time_of_day_colour_codes[5])
    place_sydney_label.config(bg=time_of_day_colour_codes[6])
    place_wellington_label.config(bg=time_of_day_colour_codes[7])

    day_localtime_time_label.config(text=f'{all_the_days[0]} {day_num[0]}, {month_abbreviations[0]}')
    day_london_label.config(text=f'{all_the_days[1]} {day_num[1]}, {month_abbreviations[1]}')
    day_new_york_label.config(text=f'{all_the_days[2]} {day_num[2]}, {month_abbreviations[2]}')
    day_los_angeles_label.config(text=f'{all_the_days[3]} {day_num[3]}, {month_abbreviations[3]}')
    day_shanghai_label.config(text=f'{all_the_days[4]} {day_num[4]}, {month_abbreviations[4]}')
    day_tokyo_label.config(text=f'{all_the_days[5]} {day_num[5]}, {month_abbreviations[5]}')
    day_sydney_label.config(text=f'{all_the_days[6]} {day_num[6]}, {month_abbreviations[6]}')
    day_wellington_label.config(text=f'{all_the_days[7]} {day_num[7]}, {month_abbreviations[7]}')

    window.after(100, international_time)


def window_object():
    window.title('Time Keeper')
    icon = PhotoImage(file=f'{resource_path("")}whiteOnPurpleReverseIcon.png')  # Our icon image
    window.iconphoto(True, icon)  # Using our icon image
    '''
    Making our app window to always be a third (plus a width of 193 and a height of 30) of whatever screen size it 
    is displaying on.
    '''
    window.geometry(f'{int(window.winfo_screenwidth() / 3) + 193}x{int(window.winfo_screenheight() / 3) + 30}')
    window.resizable(height=False, width=False)
    window.config(background='#111111')


def tabs():
    tabs_container.add(tab_time, text='TIME')
    tabs_container.add(tab_season, text='SEASON')
    tabs_container.add(tab_day_hourly_countdown, text='DAILY COUNT DOWN')
    tabs_container.add(tab_month_daily_countdown, text='MONTHLY COUNT DOWN')
    tabs_container.add(tab_year_daily_countdown, text='YEARLY COUNT DOWN')
    tabs_container.add(tab_international_time, text='INTERNATIONAL TIME')

    tabs_container.pack(expand=True, fill='y')
    tabs_container.grid()


# OUR WINDOW OBJECT

window = Tk()

# OUR TABS

tabs_container = ttk.Notebook(window)

tab_time = Frame(tabs_container, background='#222222')
tab_season = Frame(tabs_container, bg='#222222')
tab_day_hourly_countdown = Frame(tabs_container, bg='#111111')
tab_month_daily_countdown = Frame(tabs_container, bg='#222222')
tab_year_daily_countdown = Frame(tabs_container, bg='#111111', pady=1, padx=1)
tab_international_time = Frame(tabs_container, bg='#111111', pady=23, padx=10)

# Populating Our Tabs

# Time Tab

time_label = Label(tab_time,
                   text=f'{time}',
                   font=('Arial', 124),
                   bg='#111111',
                   fg='#fff')

time_label.grid()

month_label = Label(tab_time,
                    text=f'{time}',
                    font=('Arial', 28),
                    bg='#222222',
                    fg='#fff',
                    pady=13)

month_label.grid()

# Seasons Tab

season_frame = Frame(tab_season)

season_label = Label(tab_season)
season_label.grid()

# Day Hourly Count Down Tab

hours_remaining_label = Label(tab_day_hourly_countdown,
                              text=local_time.strftime(f'HOURS\nREMAINING\nFOR TODAY'),
                              font=('Arial', 15),
                              bg='#222',
                              fg='#fff')

hours_remaining_label.grid(row=0, column=0)

hour_frame = Frame(tab_day_hourly_countdown, bg='#111111')
hour_frame.grid(row=0, column=1, pady=34, padx=4)

hour_digits_label = Label(hour_frame,
                          text=f'{23 - int(local_time.strftime("%H"))}:{59 - int(local_time.strftime("%M"))}:{60 - int(local_time.strftime("%S"))}',
                          font=('Arial', 97),
                          bg='#111111',
                          fg='#fff',)

hour_digits_label.grid(row=0, column=0, columnspan=3)

hours_sub_label = Label(hour_frame, text='HOURS',
                        font=('Arial', 11),
                        bg='#111111',
                        fg='#fff',
                        padx=15)

minutes_sub_label = Label(hour_frame,
                          text='MINUTES',
                          font=('Arial', 11),
                          bg='#111111',
                          fg='#fff',
                          padx=13)

seconds_sub_label = Label(hour_frame,
                          text='SECONDS',
                          font=('Arial', 11),
                          bg='#111111',
                          fg='#fff',
                          padx=17)

hours_sub_label.grid(row=1, column=0)
minutes_sub_label.grid(row=1, column=1)
seconds_sub_label.grid(row=1, column=2)

# Month Daily Countdown Tab

month_remaining_days_label = Label(tab_month_daily_countdown,
                                   text=f'DAYS REMAINING\nFOR THIS MONTH',
                                   font=('Arial', 20),
                                   bg='#222222',
                                   fg='#fff')

month_remaining_days_label.grid(row=0, column=0)

days_in_month_frame = Frame(tab_month_daily_countdown,
                            bg='#111111',
                            padx=93,
                            pady=5)

days_in_month_frame.grid(row=0, column=1)

days_label = Label(days_in_month_frame,
                   text=f'{month_daily_countdown}',
                   font=('Arial', 148),
                   pady=-29,
                   bg='#111111',
                   fg='#fff',
                   padx=-65)

days_label.grid(row=0, column=0)

day_fraction_lapsed_label = Label(days_in_month_frame,
                                  text=f'{month_daily_countdown}',
                                  font=('Arial', 15),
                                  padx=15,
                                  bg='#111111',
                                  fg='#fff')

day_fraction_lapsed_label.grid(row=1, column=0)

# Year Daily Count Down Tab

button_values: [str] = ['left', 'passed']
left_or_passed_days: StringVar = StringVar()
left_or_passed_days.set(button_values[0])  # Setting a default value for the tab to render.

remaining_days_label = Radiobutton(tab_year_daily_countdown,
                                   text='DAYS\nREMAINING\nTHIS YEAR',
                                   font=('Arial', 25),
                                   bd='0',
                                   bg='#222222',
                                   fg='#fff',
                                   selectcolor='red',
                                   indicatoron=False,
                                   variable=left_or_passed_days,
                                   compound=LEFT,
                                   relief=SOLID,
                                   value=button_values[0],
                                   command=year_daily_countdown)

days_passed_label = Radiobutton(tab_year_daily_countdown,
                                text='DAYS\nPASSED\nTHIS YEAR',
                                font=('Arial', 27),
                                pady=2,
                                bd='0',
                                bg='#222222',
                                fg='#fff',
                                selectcolor='green',
                                indicatoron=False,
                                variable=left_or_passed_days,
                                compound=LEFT,
                                relief=SOLID,
                                value=button_values[1],
                                command=year_daily_countdown)

remaining_days_label.grid(row=0, column=0)
days_passed_label.grid(row=1, column=0)

year_daily_countdown_frame = Frame(tab_year_daily_countdown, bg='#111111', padx=25)

year_daily_countdown_frame.grid(row=0, column=1, columnspan=2, rowspan=2)

day_count_label = Label(year_daily_countdown_frame,
                        text='365',
                        font=("Arial", 125),
                        padx=50,
                        bg='#111111',
                        fg='#222222')

hour_count_label = Label(year_daily_countdown_frame,
                         text='DIOURA 00:00:00',  # "DIOURA" is a SeTswana word for "HOURS"
                         font=("Arial", 23),
                         padx=75,
                         bg='#111111',
                         fg='#222222')

day_count_label.grid(row=0, column=0, columnspan=2)
hour_count_label.grid(row=1, column=0)

# International Time Tab

# Local Time

localtime_frame = Frame(tab_international_time, bg='#222222')
localtime_frame.grid(row=0, column=0, padx=5, pady=10)

time_localtime_label = Label(localtime_frame,
                             text=local_time.strftime('%H:%M:%S'),
                             font=('Arial', 14),
                             padx=12,
                             fg='#fff',
                             bg='#222222')

day_localtime_time_label = Label(localtime_frame,
                                 text='LB2 10, FIR',  # SeTswana shorthand date translating to: "Tue 10, JAN"
                                 font=('Arial', 11),
                                 padx=10,
                                 fg='#fff',
                                 bg='#222222')

place_localtime_time_label = Label(localtime_frame,
                                   text='MY TIME',
                                   font=('Arial', 15),
                                   padx=12,
                                   fg='#fff',
                                   bg='blue')

time_localtime_label.grid(row=0, column=0)
day_localtime_time_label.grid(row=1, column=0)
place_localtime_time_label.grid(row=2, column=0)

# London Time
london_time_frame = Frame(tab_international_time, bg='#222222')
london_time_frame.grid(row=0, column=1, padx=5, pady=10)

time_london_label = Label(london_time_frame,
                          text=local_time.strftime(f'%H:%M:%S'),
                          font=('Arial', 14),
                          padx=12,
                          fg='#fff',
                          bg='#222222')
day_london_label = Label(london_time_frame,
                         text='LB2 10, FIR',
                         font=('Arial', 11),
                         padx=10,
                         bg='#222222',
                         fg='#fff')
place_london_label = Label(london_time_frame,
                           text='LONDON',
                           font=('Arial', 14),
                           padx=12,
                           bg='blue',
                           fg='white')

time_london_label.grid(row=0, column=1)
day_london_label.grid(row=1, column=1)
place_london_label.grid(row=2, column=1)

# New York Time
new_york_time_frame = Frame(tab_international_time, bg='#222222')
new_york_time_frame.grid(row=0, column=2, padx=5, pady=10)

time_new_york_label = Label(new_york_time_frame,
                            text=local_time.strftime('%H:%M:%S'),
                            font=('Arial', 14),
                            padx=12,
                            fg='#fff',
                            bg='#222222')

day_new_york_label = Label(new_york_time_frame,
                           text='LB2 10, FIR',
                           font=('Arial', 11),
                           padx=10,
                           bg='#222222',
                           fg='#fff')

place_new_york_label = Label(new_york_time_frame,
                             text='NEW YORK',
                             font=('Arial', 14),
                             padx=13,
                             bg='blue',
                             fg='white')

time_new_york_label.grid(row=0, column=2)
day_new_york_label.grid(row=1, column=2)
place_new_york_label.grid(row=2, column=2)

# Los Angeles Time
los_angeles_time_frame = Frame(tab_international_time, bg='#222222')
los_angeles_time_frame.grid(row=0, column=3, padx=5, pady=10)

time_los_angeles_label = Label(los_angeles_time_frame,
                               text=local_time.strftime(f'%H:%M:%S'),
                               font=('Arial', 14),
                               padx=12,
                               bg='#222222',
                               fg='#fff')

day_los_angeles_label = Label(los_angeles_time_frame,
                              text='LB2 10, FIR',
                              font=('Arial', 11),
                              padx=10,
                              bg='#222222',
                              fg='#fff')

place_los_angeles_label = Label(los_angeles_time_frame,
                                text='LOS ANGELES',
                                font=('Arial', 14),
                                padx=13,
                                bg='blue',
                                fg='white')

time_los_angeles_label.grid(row=0, column=3)
day_los_angeles_label.grid(row=1, column=3)
place_los_angeles_label.grid(row=2, column=3)

# Shanghai Time
shanghai_time_frame = Frame(tab_international_time, bg='#222222')
shanghai_time_frame.grid(row=1, column=0, padx=12, pady=25)

time_shanghai_label = Label(shanghai_time_frame,
                            text=local_time.strftime('%H:%M:%S'),
                            font=('Arial', 14),
                            padx=12,
                            bg='#222222',
                            fg='#fff')

day_shanghai_label = Label(shanghai_time_frame,
                           text='LB2 10, FIR',
                           font=('Arial', 11),
                           padx=10,
                           bg='#222222',
                           fg='#fff')

place_shanghai_label = Label(shanghai_time_frame,
                             text='SHANGHAI',
                             font=('Arial', 14),
                             padx=12,
                             bg='blue',
                             fg='white')

time_shanghai_label.grid(row=0, column=0)
day_shanghai_label.grid(row=1, column=0)
place_shanghai_label.grid(row=2, column=0)

# Tokyo Time
tokyo_time_frame = Frame(tab_international_time, bg='#222222')
tokyo_time_frame.grid(row=1, column=1, padx=12, pady=25)

time_tokyo_label = Label(tokyo_time_frame,
                         text=local_time.strftime(f'%H:%M:%S'),
                         font=('Arial', 14),
                         padx=12,
                         bg='#222222',
                         fg='#fff')

day_tokyo_label = Label(tokyo_time_frame,
                        text='LB2 10, FIR',
                        font=('Arial', 11),
                        padx=10,
                        bg='#222222',
                        fg='#fff')

place_tokyo_label = Label(tokyo_time_frame,
                          text='TOKYO',
                          font=('Arial', 18),
                          padx=12,
                          bg='blue',
                          fg='white')

time_tokyo_label.grid(row=0, column=1)
day_tokyo_label.grid(row=1, column=1)
place_tokyo_label.grid(row=2, column=1)

# Sydney Time
sydney_time_frame = Frame(tab_international_time, bg='#222222')
sydney_time_frame.grid(row=1, column=2, padx=12, pady=25)

time_sydney_label = Label(sydney_time_frame,
                          text=local_time.strftime('%H:%M:%S'),
                          font=('Arial', 14),
                          padx=12,
                          bg='#222222',
                          fg='#fff')

day_sydney_label = Label(sydney_time_frame,
                         text='LB2 10, FIR',
                         font=('Arial', 11),
                         padx=10,
                         bg='#222222',
                         fg='#fff')

place_sydney_label = Label(sydney_time_frame,
                           text='SYDNEY',
                           font=('Arial', 15),
                           padx=20,
                           bg='blue',
                           fg='white')

time_sydney_label.grid(row=0, column=2)
day_sydney_label.grid(row=1, column=2)
place_sydney_label.grid(row=2, column=2)

# Wellington Time
wellington_time_frame = Frame(tab_international_time, bg='#222222')
wellington_time_frame.grid(row=1, column=3, padx=12, pady=25)

time_wellington_label = Label(wellington_time_frame,
                              text=local_time.strftime(f'%H:%M:%S'),
                              font=('Arial', 14),
                              padx=12,
                              bg='#222222',
                              fg='#fff')

day_wellington_label = Label(wellington_time_frame,
                             text='LB2 10, FIR',
                             font=('Arial', 11),
                             padx=10,
                             bg='#222222',
                             fg='#fff')

place_wellington_label = Label(wellington_time_frame,
                               text='WELLINGTON',
                               font=('Arial', 14),
                               padx=12,
                               bg='blue',
                               fg='white')

time_wellington_label.grid(row=0, column=3)
day_wellington_label.grid(row=1, column=3)
place_wellington_label.grid(row=2, column=3)


def resource_path(relative_path) -> [bytes, str]:  # Telling our app where to look for all the (5) images it needs.
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def main() -> None:
    window_object()
    tabs()
    time()
    season()
    day_hourly_countdown()
    month_daily_countdown()
    year_daily_countdown()
    international_time()

    window.mainloop()


if __name__ == '__main__':
    main()
