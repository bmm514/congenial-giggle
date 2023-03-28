from os import path, makedirs
import json
import datetime

from collections import OrderedDict

class AlreadyInDict(Exception):
    '''A key is aleady present in the dictionary'''

class pokemonGOtracker:
    def __init__(self, tracker_file):
        self.tracker_file = tracker_file
        self.directory = path.split(self.tracker_file)[0]
        self.__initialise_tracker()

    def __initialise_tracker(self):
        if not path.isfile(self.tracker_file):
            if not path.isdir(self.directory):
                makedirs(self.directory)
            
            try:
                with open(self.tracker_file, 'a+') as jsonin:
                    self._open_json(jsonin)
            except OSError:
                print('Failed creating the file')
            finally:
                print('Successfully initialised the file')
        else:
            with open(self.tracker_file) as jsonin:
                self._open_json(jsonin)
            print('Successfully opened the file')

    def _open_json(self, jsonin):
        try:
            self.tracker_dict = OrderedDict(json.load(jsonin))
        except json.decoder.JSONDecodeError:
            self.tracker_dict = OrderedDict()

    def _save_json(self):
        with open(self.tracker_file, 'w') as jsonout:
            json.dump(self.tracker_dict, jsonout, indent = 2)

    def _clear_tracker(self):
        '''Reset the tracker to an empty OrderedDict'''
        try:
            with open(self.tracker_file, 'w') as jsonin:
                self._open_json(jsonin)
                self._save_json()
        except OSError:
            print('Failed clearing the file')
        finally:
            print('Successfully cleared the file')

    def update_xp(self, xp, date, accept_all = False):
        '''Add the XP on a date specified in the format DD/MM/YY'''
        try:
            if date in self.tracker_dict.keys():
                raise AlreadyInDict
            self.tracker_dict.update({date : xp})
            print(f'Updated {xp} xp on {date}')
        except AlreadyInDict:
            current_xp = self.tracker_dict[date]
            if not accept_all:
                replace_xp = input(f'Replace the current xp, {current_xp}, on {date} with {xp}? y/n?')
            else:
                replace_xp = 'y'

            if replace_xp == 'y':
                self.tracker_dict[date] = xp
                print(f'Updated {xp} xp on {date}')
            else:
                print('Not updated')

        self._save_json()
        
    def delete_record(self, date):
        '''Delete a record from the database'''
        del self.tracker_dict[date]
        self._save_json()

    def _get_isoday(self, day, loc):
        '''Get the day in datetime format and the dict key associated with it.
        Only day (DD/MM/YYY) or loc are required.'''
        if day is None:
            day_key = sorted(self.tracker_dict)[loc]
        else:
            day_key = handle_date(day)

        day = datetime.date.fromisoformat(day_key)

        return day, day_key

    def _xp_delta(self, end_day_key, start_day_key):
        try:
            xp_delta = int(self.tracker_dict[end_day_key]) - int(self.tracker_dict[start_day_key])
        except KeyError:
            try:
                self.tracker_dict[end_day_key]
            except KeyError as e:
                print(f'{e} is not found for the end_day')
                raise
            try:
                self.tracker_dict[start_day_key]
            except KeyError as e:
                print(f'{e} is not found for the start_day')
                raise

        return xp_delta

    def calculate_avg_daily(self, start_day = None, end_day = None):
        '''Calcualte the avg daily xp between two dates. start_day and end_day default to newest and oldest dates'''
        start_day, start_day_key = self._get_isoday(start_day, 0)
        end_day, end_day_key = self._get_isoday(end_day, -1)

        days = end_day - start_day
        xp_delta = self._xp_delta(end_day_key, start_day_key)
        
        avg_daily_xp = xp_delta / days.days

        return avg_daily_xp, (start_day_key, end_day_key) 
    
    def latest_xp(self):
        _, latest_day = int(self._get_isoday(None, -1))
        return self.tracker_dict[latest_day]

def update_main(args):
    '''Function to run update for argparser'''
    tracker_file = args.tracker_dict
    xp = args.xp
    date = handle_date(args.date)
    accept_all = args.force_yes

    pokeGOtracker = pokemonGOtracker(tracker_file) 
    pokeGOtracker.update_xp(xp, date, accept_all)

def delete_main(args):
    '''Function to run delete for argparser'''
    tracker_file = args.tracker_dict
    date = handle_date(args.date)

    pokeGOtracker = pokemonGOtracker(tracker_file) 
    pokeGOtracker.delete_record(date)

def avg_xp_main(args):
    tracker_file = args.tracker_dict
    start_date = args.start_date
    end_date = args.end_date

    pokeGOtracker = pokemonGOtracker(tracker_file) 
    avg_daily_xp, (start_day_key, end_day_key) = pokeGOtracker.calculate_avg_daily(start_date, end_date)

    print(f'Average XP gained between {start_day_key} and {end_day_key}: {avg_daily_xp}')

def handle_date(date):
    '''Convert date from DD/MM/YYYY to a datetime.date object if not already in the correct format'''
    if not isinstance(date, datetime.date):
        day, month, year = date.split('/')
        if len(year) != 4:
            raise ValueError('Year input is not YYYY, likely only YY')
        date = datetime.date(int(year), int(month), int(day))

    return date.isoformat()

def main():
    from argparse import ArgumentParser

    parser = ArgumentParser(description = 'PokemonGo tracker for xp, ...')
    parser.add_argument('tracker_dict', help = 'Path to the tracker JSON file')
    parser.add_argument('--force_yes', help = 'Always answer yes to questions', action = 'store_true')

    subparser = parser.add_subparsers(title = 'command', description = 'Choose mode to run in:', dest = 'command', required = True)
    update_parser = subparser.add_parser('update', help = 'Update XP for a date')
    update_parser.add_argument('xp', help = 'Xp value to add to the data storage for the date specified')
    update_parser.add_argument('--date', help = 'Date for the Xp value to be added to in format DD/MM/YYYY. Default t  current date',
            default = datetime.date.today())
    update_parser.set_defaults(func=update_main)

    delete_parser = subparser.add_parser('delete', help = 'Delete a date record')
    delete_parser.add_argument('--date', help = 'Date for the Xp value to be deleted.')
    delete_parser.set_defaults(func=delete_main)

    avg_xp_parser = subparser.add_parser('avg_xp', help = 'Calculate the average XP between two dates')
    avg_xp_parser.add_argument('--start_date', help = 'Date for the start xp value to be used (DD/MM/YYYY). Default earliest',
            default = None)
    avg_xp_parser.add_argument('--end_date', help = 'Date for the end xp value to be used (DD/MM/YYY). Default latest',
            default = None)
    avg_xp_parser.set_defaults(func=avg_xp_main)

    args = parser.parse_args()

    args.func(args)


if __name__ == '__main__':
    main()
