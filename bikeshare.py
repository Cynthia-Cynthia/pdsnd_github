import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    invalid_message = '\nSorry, we cannot recognise what you have entered. Please type {}'

    city = input('\nPlease enter a city (Chicago, New York City or Washington) you are interested in: \n')
    while city.lower() not in ['chicago', 'new york city', 'washington']:
        print(invalid_message.format('Chicago, New York City or Washington'))
        city = input('Which city are you interested in? Chicago, New York City or Washington?\n')

    month = input('\nPlease enter a month (January, February, March, April, May, June or All) you are interested in: \n')
    while month.lower() not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
        print(invalid_message.format('January, February, March, April, May, June or All'))
        month = input('Which month are you interested in? January, February, March, April ,May, June or All?\n')

    day = input('\nPlease enter a day of week (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All) you are interested in: \n')
    while day.lower() not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
        print(invalid_message.format('Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All'))
        day = input('Which day of week are you interested in? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All\n')

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city.lower()])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month.lower() != 'all':
        df = df[df['month'] == month.title()]

    if day.lower() != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')

    message = input('Type "skip" to jump to the next part or anything else to continue: \n')
    if message.lower() == 'skip':
        print('-'*40)
    else: 
        start_time = time.time()

        df['Start Time'] = pd.to_datetime(df['Start Time'])

        df['month'] = df['Start Time'].dt.month_name()
        common_month = df['month'].mode()[0]
        print('Most common month: {}'.format(common_month))

        df['day_of_week'] = df['Start Time'].dt.day_name()
        common_day_of_week = df['day_of_week'].mode()[0]
        print('Most common day of week: {}'.format(common_day_of_week))

        df['start_hour'] = df['Start Time'].dt.hour
        common_start_hour = df['start_hour'].mode()[0]
        print('Most common start hour: {}'.format(common_start_hour))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    
    message = input('Type "skip" to jump to the next part or anything else to continue: \n')
    if message.lower() == 'skip':
        print('-'*40)
    else:
        start_time = time.time()

        common_start_station = df['Start Station'].mode()[0]
        print('Most commonly used start station: {}'.format(common_start_station))

        common_end_station = df['End Station'].mode()[0]
        print('Most commonly used end station: {}'.format(common_end_station))

        df['station_combination'] = df['Start Station'] + ' - ' + df['End Station']
        common_station_combination = df['station_combination'].mode()[0]
        print('Most frequent combination of start station and end station trip: {}'.format(common_station_combination))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')

    message = input('Type "skip" to jump to the next part or anything else to continue: \n')
    if message.lower() == 'skip':
        print('-'*40)
    else:
        start_time = time.time()

        total_travel_time = df['Trip Duration'].sum()
        print('Total travel time: {} seconds'.format(total_travel_time))

        mean_travel_time = df['Trip Duration'].mean()
        print('Mean travel time: {} seconds'.format(mean_travel_time))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')

    message = input('Type "skip" to jump to the next part or anything else to continue: \n')
    if message.lower() == 'skip':
        print('-'*40)
    else:
        start_time = time.time()

        user_type = df['User Type'].value_counts()
        print('Counts of user types: \n{}\n'.format(user_type))

        try:
            gender = df['Gender'].value_counts()
            print('Counts of gender: \n{}\n'.format(gender))
        except:
            return None

        try:
            earliest = int(df['Birth Year'].min())
            most_recent = int(df['Birth Year'].max())
            common_year = int(df['Birth Year'].mode()[0])
            print('Earliest year of birth: {}\nMost recent year of birth: {}\nMost common year of birth: {}'.format(earliest, most_recent, common_year))
        except:
            return None

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def data_view(df):
    """Displays the data rows of dataframe."""

    message = input('\nWould you like to view the first 5 rows of data? Enter yes or no.\n')
    i = 0
    while message.lower() == 'yes':
        if df.iloc[i:i+5].empty:
            print('There are now more rows to display.')
            break
        else:
            print(df.iloc[i:i+5])
            i += 5
            message = input('\nWould you like to view the next 5 rows of data? Enter yes or no.\n')

    print('-'*40)    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data_view(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()