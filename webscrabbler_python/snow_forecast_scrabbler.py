from bs4 import BeautifulSoup
import urllib3
import re
import datetime
import warnings
from functools import reduce
from collections import namedtuple
# import logging

DataTable = namedtuple('DataTable', ['SCRABBLETIME', 'RESORT', 'DATE', 'LOC', 'TEMP', 'TEMPU', 'TEMPMIN', 'TEMPMAX', 'WINDSPEED', 'WINDDIR', 'WINDU', 'ALT', 'TXT', 'FREEZU', 'FREEZL', 'SNOW', 'SNOWU'])

class SnowForecastScrabbler(object):

    """Docstring for WebScrabbler. """

    # https://stackoverflow.com/questions/68645/are-static-class-variables-possible
    # altitudes = {"top": 5671, "mid": 4909, "bottom": 4147, "Tehran": 1191}

    __URL_BASE = 'https://www.snow-forecast.com/resorts/'
    # collection seems to code slow
    __COL_NAME = DataTable(
        SCRABBLETIME='scrabble_time',
        RESORT='resort',
        DATE='date',
        LOC='location',
        TEMP='temperature',
        TEMPU='temperature_unit',
        TEMPMIN='temperature_min',
        TEMPMAX='temperature_max',
        WINDSPEED='wind_speed',
        WINDDIR='wind_direction',
        WINDU='wind_unit',
        ALT='altitude',
        TXT='text',
        FREEZU='frezzing_unit',
        FREEZL='freezing_level',
        SNOW='snow',
        SNOWU='snow_unit'
    )

    def __init__(self, resort: str, level: str = 'mid'):
        """TODO: to be defined1. """
        self._resort = resort
        self._level = level
        url = self.__URL_BASE + self._resort + "/forecasts/feed/" + level + "/m"
        response = urllib3.PoolManager().request('GET', url)
        self._soup_base = BeautifulSoup(response.data, 'lxml')

    def getCurrent(self) -> dict:
        current_table = self._soup_base.select('tr[id="table-current"]')[0]

        current = {}
        current[self.__COL_NAME.SCRABBLETIME] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        current[self.__COL_NAME.RESORT] = self._resort
        current[self.__COL_NAME.DATE] = datetime.date.today().strftime('%Y-%m-%d')
        current[self.__COL_NAME.TEMP] = current_table.findNext('td').string.strip()
        pattern = re.compile(r'-?\d+\.\d+')
        current[self.__COL_NAME.TEMP] = float(re.match(pattern, current[self.__COL_NAME.TEMP]).group())
        cur_wind =  current_table.select('img')[0]['alt'].split()
        current[self.__COL_NAME.WINDSPEED] = int(cur_wind[0])
        current[self.__COL_NAME.WINDDIR] = cur_wind[1]

        station = self._soup_base.select('div[id="wf-wstation"]')[0].string.strip()
        station_level = int(re.findall(r'\d{4}', station)[0])
        station = re.sub(r'^.*from', '', station)
        station = re.sub(r',.*[.\n\t\da-zA-Z\/ ]*', '', station)
        current[self.__COL_NAME.LOC] = '{}, Elevation level: {}m'.format(station.strip(), station_level)
        current[self.__COL_NAME.ALT] = station_level
        return current


    def getLevel(self) -> dict:
        # url = self.__URL_BASE + self._resort + "/forecasts/feed/" + level + "/m"
        soup = self._soup_base
        # if level == self._level else \
        #    BeautifulSoup(urllib3.PoolManager().request('GET', url).data, 'lxml')
        location = soup.select('body > div[id="wf-location"]')
        weather_txt = soup.select('div.weathercell > img')[0]['alt']
        temperature_table = soup.select('tr[id="table-temp"]')[0]
        wind_table = soup.select('tr[id="table-wind"]')[0]

        data = {}
        data[self.__COL_NAME.RESORT] = self._resort
        data[self.__COL_NAME.SCRABBLETIME] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        date = datetime.date.today() # + datetime.timedelta(days=1)
        data[self.__COL_NAME.DATE] = date.strftime('%Y-%m-%d')
        loc_pattern = re.compile(r'\d{4}')
        data[self.__COL_NAME.ALT] = int(re.findall(loc_pattern, location[0].string.strip())[0])

        data[self.__COL_NAME.TXT] = weather_txt
        data[self.__COL_NAME.FREEZU] = 'm'
        data[self.__COL_NAME.FREEZL] = wind_table.find_next('tr').select('td')[0].string.strip()

        # https://stackoverflow.com/questions/8270092/remove-all-whitespace-in-a-string-in-python
        # temperature = self._soup.select('tr[id="table-temp"] > td')[0].string.split('|')
        data[self.__COL_NAME.TEMPU] = temperature_table.select('th')[0].string
        temperature_range = [int(temp.replace("°", "").strip()) for temp in \
                             temperature_table.select('td')[0].string.split('|')]
        data[self.__COL_NAME.TEMPMIN] = temperature_range[0]
        data[self.__COL_NAME.TEMPMAX] = temperature_range[1]

        data[self.__COL_NAME.WINDU] = wind_table.select('th')[0].string
        wind_measures = wind_table.select('img')[0]['alt'].split(" ")
        data[self.__COL_NAME.WINDSPEED] = float(wind_measures[0])
        data[self.__COL_NAME.WINDDIR] = wind_measures[1]
        data.update(self.getSnow(self._level))

        return data


    def getSnow(self, level: str = 'mid') -> dict:
        url = self.__URL_BASE + self._resort + "/6day/" + level
        response = urllib3.PoolManager().request('GET', url)
        soup = BeautifulSoup(response.data, 'lxml')

        snow_unit = soup.select('span[class=snowu]')[0].string
        snow_soup = soup.findAll('span', attrs = {'class': 'snow'})[0:3]

        # snow_fall_day = reduce(lambda x, y: int(x.string)+int(y.string), snow_soup)

        snow_fall_day = 0
        for snow in snow_soup:
            snow_val = snow.string
            snow_val = 0 if snow_val == '-' else snow_val
            snow_fall_day += int(snow_val)

        return {self.__COL_NAME.SNOWU: snow_unit, self.__COL_NAME.SNOW: snow_fall_day}


    @property
    def string(self) -> str:
        return self._soup_base.prettify()


    @property
    def print(self):
        print(self.string)


    def write(self, filename: str):
        with open(filename, 'w') as file:
            file.write(self.string)

    def db_write(self, db: str, table: str = None, db_type: str = 'csv', write_city_current: bool = False):
        mountain_fc = dict.fromkeys(self.__COL_NAME._asdict().values(), None)
        city_current = dict.fromkeys(self.__COL_NAME._asdict().values(), None)

        mountain_fc.update(self.getLevel())
        city_current.update(self.getCurrent())

        if db_type == 'csv':
            import csv
            with open(db, 'a') as file:
                csv_wr = csv.writer(file, dialect='excel')
                if write_city_current:
                    csv_wr.writerow(city_current.values())
                csv_wr.writerow(mountain_fc.values())

        elif db_type == 'mongodb':
            pass
        elif db_type == 'mysql':
            pass
        elif db_type == 'postrsql':
            pass
        else:
            # https://pyformat.info/
            warning = '{} "{}" {}'.format('database type', db_type, 'not implemented')
            # https://stackoverflow.com/questions/9595009/python-warnings-warn-vs-logging-warning
            warnings.warn(warning)
            return


def run():
    """TODO: Docstring for run.

    :url: TODO
    :returns: TODO

    """
    # resort = 'Damavand_mid' # Sahand-Ski-Resort
    # url_full_page = 'https://www.snow-forecast.com/resorts/Damavand_mid/6day/top'
    # url_top = 'https://www.snow-forecast.com/resorts/Damavand_mid/forecasts/feed/top/m'
    # url_mid = 'https://www.snow-forecast.com/resorts/Damavand_mid/forecasts/feed/mid/m'
    # url_bot = 'https://www.snow-forecast.com/resorts/Damavand_mid/forecasts/feed/bot/m'
    # file_name = 'damavand_wf_top.html'
    db_name = 'snowforecast.csv'

    from shutil import copyfile
    dst_file = db_name.split('.')[0] + datetime.datetime.now().strftime('%Y-%m-%d_%M%H%S') + '.csv'
    copyfile(db_name, dst_file)

    damavand_top = SnowForecastScrabbler('Damavand', 'top')
    damavand_top.db_write(db_name, write_city_current = True)
    damavand_mid = SnowForecastScrabbler('Damavand', 'mid')
    damavand_mid.db_write(db_name)
    damavand_bot = SnowForecastScrabbler('Damavand', 'bot')
    damavand_bot.db_write(db_name)
    # damavand_mid.print
    # damavand_mid.write(file_name)

    sahand_top = SnowForecastScrabbler('Sahand-Ski-Resort', 'top')
    sahand_top.db_write(db_name, write_city_current = True)
    sahand_mid = SnowForecastScrabbler('Sahand-Ski-Resort', 'mid')
    sahand_mid.db_write(db_name)
    sahand_bot = SnowForecastScrabbler('Sahand-Ski-Resort', 'bot')
    sahand_bot.db_write(db_name)


if __name__ == "__main__":
    run()


# getterExampl(self):
#        fc_class = "units-metric not-logged-in view-as-guest"
#        # for url full page
#        # forecast = self._soup.find('body', {'class': type(self).fc_class})
#        href="/resorts/Damavand/6day/top"
#        forecast = self._soup_base.find_all('a', attrs={'href': href})
#
#        # print(self._soup.find_all('p'))
#        print(forecast)
#        for fc in forecast:
#            print("Next sibling: ", fc.next_sibling)
#            print("Next element: ", fc.next_element)
#
#        print(self._soup_base.select('a > mark > span, .height'))
#        print(self._soup_base.select('a[href=' + href +'] > mark > span[class=height]')[0].string)
#
#        # morning = WeatherData()
#        # afternoon = WeatherData()
#        # night = WeatherData()


