import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gamesite.settings")
import django
django.setup()

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
        door.save()

        direction_map = {
            'north': 'south',
            'south': 'north',
            'east': 'west',
            'west':'east',
        }
        
        self.rooms[roomA].doors[direction] = door
        self.rooms[roomB].doors[direction_map[direction]] = door
        self.rooms[roomA].save()
        self.rooms[roomB].save()

    def makeRoom(self, title, illuminated=True):

        try:
            room = Room.objects.get(title=title)
        except:
            room = Room()
            room.title = title

        room.illuminated = illuminated
        room.save()
        
        self.rooms[title] = room

    def cleanMap(self):
        rooms = Room.objects.all().delete()
        doors = Door.objects.all().delete()

def main():
    
    mapBuilder = MapBuilder()
    mapBuilder.cleanMap()

    # Make rooms
    mapBuilder.makeRoom('Kitchen')
    mapBuilder.makeRoom('Living Room')
    mapBuilder.makeRoom('Den')
    mapBuilder.makeRoom('Entrance Hall')

    # Connect Rooms
    mapBuilder.connectRooms('Entrance Hall', 'Kitchen', 'north')
    mapBuilder.connectRooms('Entrance Hall', 'Den', 'west')
    mapBuilder.connectRooms('Kitchen', 'Living Room', 'west')


if __name__ == '__main__':

    main()






