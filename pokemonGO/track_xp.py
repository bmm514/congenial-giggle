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
                open(self.tracker_file, 'a').close()
            except OSError:
                print('Failed creating the file')
            finally:
                print('Successfully initialised the file')
        else:
            print('Successfully opened the file')

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
            tracker_json = OrderedDict(json.load(open(self.tracker_file)))
            if date in tracker_json.keys():
                raise AlreadyInDict
            tracker_json.update({date : xp})
        #except JSONDecodeError:
        except json.decoder.JSONDecodeError:
            tracker_json = OrderedDict({date : xp})
        except AlreadyInDict:
            current_xp = tracker_json[date]
            if not accept_all:
                replace_xp = input(f'Replace the current xp, {current_xp}, with {xp}? y/n?')
            else:
                replace_xp = 'y'

            if replace_xp == 'y':
                tracker_json[date] = xp
                print(f'Updated xp for {date}')
            else:
                print('Not updated')

        with open(self.tracker_file, 'w') as jsonout:
            json.dump(tracker_json, jsonout, indent = 2)
        
        return(tracker_json)

def main():
    from argparse import ArgumentParser

    parser = ArgumentParser(description = 'PokemonGo tracker for xp, ...')
    parser.add_argument('--force_yes', help = 'Always answer yes to questions', action = 'store_true')

    subparser = parser.add_subparsers(title = 'command', description = 'Choose mode to run in:', dest = 'command', required = True)
    update_parser = subparser.add_parser('update', help = 'Update XP for a date')
    update_parser.add_argument('xp', help = 'Xp value to add to the data storage for the date specified')
    update_parser.add_argument('--date', help = 'Date for the Xp value to be added to. Default to current date')

    args = parser.parse_args()

    xp = args.xp
    date = args.date
    accept_all = args.force_yes

    print(xp, date, accept_all)

    tracker_file = 'test/bmm.json'

    pokeGOtracker = pokemonGOtracker(tracker_file) 
    pokeGOtracker.update_xp(xp, date, accept_all)


if __name__ == '__main__':
    main()
#    tracker_file = 'test/bmm.json'
#
#    pokeGOtracker = pokemonGOtracker(tracker_file) 
#
#    print(pokeGOtracker.tracker_file)
#    print(pokeGOtracker.directory)
#    print(pokeGOtracker.update_xp(5924750, '20/03/23'))
#    print(pokeGOtracker.update_xp(5976650, '21/03/23'))
#    print(pokeGOtracker.update_xp(6118500, '22/03/23'))

