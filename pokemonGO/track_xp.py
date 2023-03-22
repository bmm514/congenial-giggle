from os import path, makedirs
import json

from collections import OrderedDict
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

    def update_xp(self, xp, date):
        '''Add the XP on a date specified in the format DD/MM/YY'''
        try:
            tracker_json = OrderedDict(json.load(open(self.tracker_file)))
            tracker_json.update({date : xp})
        #except JSONDecodeError:
        except json.decoder.JSONDecodeError:
            tracker_json = OrderedDict({date : xp})

        with open(self.tracker_file, 'w') as jsonout:
            json.dump(tracker_json, jsonout, indent = 2)
        
        return(tracker_json)




if __name__ == '__main__':
    tracker_file = 'test/bmm.json'

    pokeGOtracker = pokemonGOtracker(tracker_file) 

    print(pokeGOtracker.tracker_file)
    print(pokeGOtracker.directory)
    print(pokeGOtracker.update_xp(5924750, '20/03/23'))
    print(pokeGOtracker.update_xp(5976650, '21/03/23'))
    print(pokeGOtracker.update_xp(6118500, '22/03/23'))
