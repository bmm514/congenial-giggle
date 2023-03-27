from os import path, makedirs
import json

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
                with open(self.tracker_file, 'a') as jsonin:
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
            self.tracker_json = OrderedDict(json.load(jsonin))
            print('Opened without JSONDecodeError')
        except json.decoder.JSONDecodeError:
            self.tracker_json = OrderedDict()
            print('Opened with JSONDecoreError')
    def _save_json(self):
        with open(self.tracker_file, 'w') as jsonout:
            json.dump(self.tracker_json, jsonout, indent = 2)

    def _clear_tracker(self):
        try:
            open(self.tracker_file, 'w').close()
        except OSError:
            print('Failed clearing the file')
        finally:
            print('Successfully cleared the file')

    def update_xp(self, xp, date, accept_all = False):
        '''Add the XP on a date specified in the format DD/MM/YY'''
        try:
            #tracker_json = OrderedDict(json.load(open(self.tracker_file)))
            if date in self.tracker_json.keys():
                raise AlreadyInDict
            self.tracker_json.update({date : xp})
        #except json.decoder.JSONDecodeError:
            #self.tracker_json = OrderedDict({date : xp})
        except AlreadyInDict:
            current_xp = self.tracker_json[date]
            if not accept_all:
                replace_xp = input(f'Replace the current xp, {current_xp}, with {xp}? y/n?')
            else:
                replace_xp = 'y'

            if replace_xp == 'y':
                self.tracker_json[date] = xp
                print(f'Updated xp for {date}')
            else:
                print('Not updated')

        self._save_json()
        
    def delete_record(self, date):
        '''Delete a record from the database'''
        del self.tracker_json[date]
        self._save_json()

def update_main(args):
    tracker_file = args.tracker_json
    xp = args.xp
    date = args.date
    accept_all = args.force_yes

    pokeGOtracker = pokemonGOtracker(tracker_file) 
    pokeGOtracker.update_xp(xp, date, accept_all)

def delete_main(args):
    tracker_file = args.tracker_json
    date = args.date

    pokeGOtracker = pokemonGOtracker(tracker_file) 
    pokeGOtracker.delete_record(date)

def main():
    from argparse import ArgumentParser

    parser = ArgumentParser(description = 'PokemonGo tracker for xp, ...')
    parser.add_argument('tracker_json', help = 'Path to the tracker JSON file')
    parser.add_argument('--force_yes', help = 'Always answer yes to questions', action = 'store_true')

    subparser = parser.add_subparsers(title = 'command', description = 'Choose mode to run in:', dest = 'command', required = True)
    update_parser = subparser.add_parser('update', help = 'Update XP for a date')
    update_parser.add_argument('xp', help = 'Xp value to add to the data storage for the date specified')
    update_parser.add_argument('--date', help = 'Date for the Xp value to be added to. Default to current date')
    update_parser.set_defaults(func=update_main)

    delete_parser = subparser.add_parser('delete', help = 'Delete a date record')
    delete_parser.add_argument('--date', help = 'Date for the Xp value to be deleted.')
    delete_parser.set_defaults(func=delete_main)

    args = parser.parse_args()

    args.func(args)


if __name__ == '__main__':
    main()
