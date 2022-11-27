from array import array
import pandas as pd
import numpy as np
import jdatetime as jdt
import requests
from datetime import date as dt
from hijri_converter import Hijri, Gregorian
from persiantools.characters import ar_to_fa


WEEKDAYS = {
    0 : [
        'دوشنبه',
        2,
        'روزکاری'
    ],
    1 : [
        'سه شنبه',
        3,
        'روزکاری'
    ],
    2 : [
        'چهارشنبه',
        4,
        'روزکاری'
    ],
    3 : [
        'پنج شنبه',
        5,
        'آخر هفته'
    ],
    4 : [
        'جمعه',
        6,
        'آخر هفته'
    ],
    5 : [
        'شنبه',
        0,
        'روزکاری'
    ],
    6 : [
        'یکشنبه',
        1,
        'روزکاری'
    ]
}

MONTHS = {
    1 : [
        'فروردین',
        'بهار',
        1
    ],
    2 : [
        'اردیبهشت',
        'بهار',
        1
    ],
    3 : [
        'خرداد',
        'بهار',
        1
    ],
    4 : [
        'تیر',
        'تابستان',
        2
    ],
    5 : [
        'مرداد',
        'تابستان',
        2
    ],
    6 : [
        'شهریور',
        'تابستان',
        2
    ],
    7 : [
        'مهر',
        'پاییز',
        3
    ],
    8 : [
        'آبان',
        'پاییز',
        3
    ],
    9 : [
        'آذر',
        'پاییز',
        3
    ],
    10 : [
        'دی',
        'زمستان',
        4
    ],
    11 : [
        'بهمن',
        'زمستان',
        4
    ],
    12 : [
        'اسفند',
        'زمستان',
        4
    ]
}

HIJRI_MONTHS = {
    1 : 'محرم',
    2 : 'صفر',
    3 : 'ربیع الاول',
    4 : 'ربیع الثانی',
    5 : 'جمادی الاول',
    6 : 'جمادی الثانی',
    7 : 'رجب',
    8 : 'شعبان',
    9 : 'رمضان',
    10 : 'شوال',
    11 : 'ذیقعده',
    12 : 'ذیحجه'
}

JWeekDay = {
    "روزکاری" : 1,
    "نیمه کاری" : 0.5,
    "آخر هفته" : 0
}

DAYOFF = {
    False : 1,
    True : 0
}
 

def create_date_table(min_range, max_range):
    df = pd.DataFrame({"gregDate": pd.date_range(min_range, max_range, freq='D')})
    df['gregDateInt'] = df['gregDate'].apply(lambda x : int(str(x).replace('-', '').split(' ')[0]))
    df["gregDayInMonthNo"] = df.gregDate.dt.day
    df['gregDayInYearNo'] = df.gregDate.dt.day_of_year
    df["gregDayInWeekNo"] = df.gregDate.dt.weekday
    df['gregDayName'] = df.gregDate.dt.day_name()
    df['gregDayInWeekStatus'] = np.where((df.gregDayInWeekNo>4) & (df.gregDayInWeekNo<7), 'Weekend', 'Workday')
    df['gregISOWeekOfYear'] = df.gregDate.dt.isocalendar().week
    df['gregMonthNo'] = df.gregDate.dt.month
    df['gregMonthName'] = df.gregDate.dt.month_name()
    df['gregFirstOfMonth'] = df.gregDate + pd.offsets.MonthEnd(0) - pd.offsets.MonthBegin(1)
    df['gregEndOfMonth'] = df.gregDate + pd.offsets.MonthEnd(0)
    df['gregQuarterNo'] = df.gregDate.dt.quarter
    df['gregYear'] = df.gregDate.dt.year
    df['gregYearMonth'] = df.gregDate.dt.to_period('M')
    df['gregYearQuarter'] = df[['gregYear', 'gregQuarterNo']].apply(lambda x: '-'.join(x.astype(str)), axis=1)
    df['JDate'] = df.gregDate.apply(lambda x: jdt.date.fromgregorian(date=x))
    df['JDateInt'] = df['JDate'].apply(lambda x : int(str(x).replace('-', '')))
    df['JDayInMonthNo'] = df['JDate'].apply(lambda x : x.day)
    df['JMonthNo'] = df['JDate'].apply(lambda x : x.month)
    df['JYear'] = df['JDate'].apply(lambda x : x.year)
    df['JDayInWeekNo'] = df.gregDayInWeekNo.apply(lambda x: WEEKDAYS[x][1])
    df['JDayName'] = df.gregDayInWeekNo.apply(lambda x: ar_to_fa(WEEKDAYS[x][0]))
    df['JWeekDayStatus'] = df.gregDayInWeekNo.apply(lambda x: ar_to_fa(WEEKDAYS[x][2]))
    df['JMonthName'] = df.JMonthNo.apply(lambda x: ar_to_fa(MONTHS[x][0]))
    df['JQuarterNo'] = df.JMonthNo.apply(lambda x: MONTHS[x][2])
    df['JQuarterName'] = df.JMonthNo.apply(lambda x: ar_to_fa(MONTHS[x][1]))
    df['JYearMonth'] = df[['JYear', 'JMonthNo']].apply(lambda x: '-'.join(x.astype(str)), axis=1)
    df['JYearQuarter'] = df[['JYear', 'JQuarterNo']].apply(lambda x: '-'.join(x.astype(str)), axis=1)
    holidays = pd.read_pickle('exp_data/holiday_dates.pickle')
    df['JDayOffStatus'] = df['JDate'].apply(lambda x: True if str(x) in list(holidays.Holiday_Date) else False)
    df['HijriMonthName'] = df.gregDate.apply(lambda x: ar_to_fa(HIJRI_MONTHS[Gregorian(x.year, x.month, x.day).to_hijri().month]))
    return df

def main():
    df = create_date_table("2006-03-21", "2027-03-20")
    df.to_pickle('exp_data/dim_date.pickle')


if __name__ == "__main__":
    main()
