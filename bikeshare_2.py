import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

valid_months = ['All', 'January', 'February', 'March', 'April', 'May', 'June']
valid_days = ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    while True:
        city = input('Which city are you interested in: Chicago, New York City or Washington?\n\n> ').title()
        if city in CITY_DATA:
            print('\nYou chose {} for analysis.\n'.format(city))
            break
        else:
            print('\nYour input does not match any of the three cities. Please try again.\n')
    
    # get user input for month (all, january, february, ... , june)

    while True:
        month = input('Which month do you want to look into? Please enter any month between January and June, or All for all months.\n\n> ').title()
        if month in valid_months:
            print('\nYou entered {} to filter the data by month.\n'.format(month))
            break
        else:
            print('\nYou input does not match any of the six months nor all. Please try again.\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        day = input('Which day of week do you want to look into? Please enter any day from Monday to Friday, or All.\n\n> ').title()
        if day in valid_days:
            print('\nYou entered {} to filter the data by day of week.\n'.format(day))
            break
        else:
            print('\nYou input does not match any of the days of week nor all. Please try again.\n')
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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if month != 'All':
        month = valid_months.index(month)
        df = df[df['month'] == month]
    if day != 'All':
        df = df[df['day_of_week'] == day]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    popular_month = df['month'].mode()[0]
    print('Most Popular Start Month:', valid_months[popular_month])

    # display the most common day of week

    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Start Day:', popular_day)

    # display the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print()
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)

    # display most commonly used end station

    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip

    df['route'] = df['Start Station'] + ' - ' + df['End Station']
    popular_route = df['route'].mode()[0]
    print('Most Popular Route:', popular_route)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print()
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['travel_time'] = df['End Time'] - df['Start Time']
    print('Total Travel Time:', df['travel_time'].sum())

    # display mean travel time
    print('Mean Travel Time:', df['travel_time'].mean())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print()
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print()
        print(gender)
    except:
        print('\nThere is no gender data for the city.')

    # Display earliest, most recent, and most common year of birth
    try:
        print()
        print('Earlist Year of Birth:', df['Birth Year'].min())
        print('Most Recent Year of Birth:', df['Birth Year'].max())
        print('Most Common Year of Birth:', df['Birth Year'].mode()[0])
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except:
        print('There is no data on year of birth for the city.')

def print_data(df):
    print_data = input('\nWould you like to print the first 5 lines of raw data? Please enter yes or no.\n\n> ').lower()
    while print_data not in ['yes', 'no']:
        print_data = input('\nYour input is not valid. Please enter yes or no.\n\n> ')
    if print_data == 'yes':
        print('\nPrinting Raw Data...')
        row_number = 0
        for row in df.iterrows():
            print()
            print(row)
            row_number += 1
            print_more = ''
            if row_number % 5 == 0:
                print_more = input('\nWould you like to print additional 5 lines? Please enter yes or no.\n\n> ').lower()
                while print_more not in ['yes', 'no']:
                    print_more = input('\nYour input is not valid. Please enter yes or no.\n\n> ').lower()
            if print_more == 'no':
                break
    else:
        print('\nYou chose not to print raw data.')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        print_data(df)        

        restart = input('\nWould you like to restart? Please enter yes or no.\n\n> ').lower()
        while restart not in ['yes', 'no']:
            restart = input('\nYour input is not valid. Please enter yes or no.\n\n> ').lower()
        if restart == 'no':
            break

if __name__ == "__main__":
	main()
