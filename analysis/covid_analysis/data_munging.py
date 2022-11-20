import pandas as pd
import argparse
import constants


# input data
df_confirmed = pd.read_csv('covid_confirmed.csv')
df_recovered = pd.read_csv('covid_recovered.csv')
df_continents = pd.read_csv('countries_to_continent.csv')


def analysis(date, continent_name=None, country=None, province=None):
    """
    To get analytical data on covid related data
    positional argument
    :param date:
    keyword argument
    :param continent_name:
    :param country:
    :param province:
    :return None:
    """
    if date not in df_confirmed.columns:
        raise KeyError("Enter proper data format(m/d/y), like 1/11/20")

    # a) global confirmed and recovered
    confirmed=df_confirmed[date].sum()
    recovered=df_recovered[date].sum()

    # Changing the column name in both dataframe to have a similar mapping
    df_confirmed_dup = df_confirmed.rename(columns = {'Country/Region':'Country', 'Province/State': "Province"})
    df_recovered_dup = df_recovered.rename(columns = {'Country/Region':'Country', 'Province/State': "Province"})

    # merging the dataframes
    df_confirmed_merge = pd.merge(df_confirmed_dup, df_continents, on="Country")
    df_recovered_merge = pd.merge(df_recovered_dup, df_continents, on="Country")

    # storing the continents
    continents = df_confirmed_merge['Continent'].unique()
    continent_covid_confirmed = {}
    continent_covid_recovered = {}

    # b) continent wise confirmed and recovered cases
    for continent in continents:
        confirmed_continent = df_confirmed_merge[(df_confirmed_merge['Continent']== continent)]
        recovered_continent = df_recovered_merge[(df_recovered_merge['Continent'] == continent)]
        continent_covid_confirmed[continent] = confirmed_continent[date].sum()
        continent_covid_recovered[continent] = recovered_continent[date].sum()

    # c) ratio
    recovery_ratio = abs(recovered/confirmed)

    # d) dynamic filtering on confirmed and recovered based on input value
    confirmed_cases_res_obj = df_confirmed_merge[(df_confirmed_merge.Province == province) | (df_confirmed_merge.Country == country) | \
        (df_confirmed_merge.Continent == continent_name)]
    confirmed_cases_count = confirmed_cases_res_obj[date_inp].sum()

    
    recovered_cases_res_obj = df_recovered_merge[(df_recovered_merge.Province == province) | (df_recovered_merge.Country == country) | \
        (df_recovered_merge.Continent == continent_name)]
    recovered_cases_count = recovered_cases_res_obj[date_inp].sum()
    
    print(confirmed)
    print(recovered)
    print(recovery_ratio)
    print(continent_covid_confirmed)
    print(continent_covid_recovered)
    print(confirmed_cases_count)
    print(recovered_cases_count)
    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help=constants.DATE_FORMAT_MESSAGE, required=True)
    parser.add_argument('-con', '--continent', help=constants.CONTINENT_MESSAGE, required=False)
    parser.add_argument('-cou', '--country', help=constants.COUNTRY_MESSAGE, required=False)
    parser.add_argument('-pro', '--province', help=constants.PROVINCE_MESSAGE, required=False)

    args = parser.parse_args()

    date_inp = args.date
    continent_inp = args.continent or None
    country_inp = args.country or None
    province_inp = args.province or None

    analysis(date_inp, continent_inp, country_inp, province_inp)
