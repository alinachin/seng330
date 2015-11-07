from django.core.management.base import BaseCommand, CommandError
import importlib
from gameworld.models import Room, Door

class MapBuilder(object):

    def __init__(self):
        self.rooms = {}

    
    def connectRooms(self, roomA, roomB, direction, locked=False):
        """
        connect two rooms with a door, direction refers to the
        placement of the door in roomA!
        """
 
        # Create door connecting the two rooms
        door = Door()
        door.room_a = self.rooms.get(roomA)
        door.room_b = self.rooms.get(roomB)
        door.locked  = locked
        door.name = 'Door'
        door.examine = ''
        door.save()

        reverse = {
            'north': 'south',
            'south': 'north',
            'east': 'west',
            'west':'east',
        }

        setattr(self.rooms[roomA], 'door_'+direction, door)
        setattr(self.rooms[roomB], direction_map[direction], door)
        #self.rooms[roomA].set_door(direction, door)
        #self.rooms[roomB].set_door(reverse[direction], door)
        
        self.rooms[roomA].save()
        self.rooms[roomB].save()

    def makeRoom(self, name, title="", illuminated=True, desc="You are in a dim room."):

        try:
            room = Room.objects.get(name=name)
        except:
            room = Room()
            room.name = name

        room.title = title
        room.illuminated = illuminated
        room.desc_header = desc
        room.save()
        
        self.rooms[name] = room

    def cleanMap(self):
        rooms = Room.objects.all().delete()
        doors = Door.objects.all().delete()

class Command(BaseCommand):
    help = 'Replaces the current map stored in gameworld with a new map'
    
    def add_arguments(self, parser):
        parser.add_argument('script', nargs=1)
        
    def handle(self, *args, **options):
        for script in options['script']:
            try:
                module = importlib.import_module('.%s' % script, 
                    'gameworld.management.commands')
                module.main()
            except ImportError:
                raise CommandError('%s was not found!' % script)
            print('Success: imported map from %s' % script)
            
