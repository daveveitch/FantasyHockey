"""
Create a multidimensional graph of fantasy hockey players
David Veitch 2016
"""

import csv
import matplotlib.pyplot as plt
import operator

# Default size of dots in graph
DOT_SIZE = 20

# Key that points to what header is for CSV file for players name
CSV_NAME_KEY = 'Name'
CSV_GAMES_PLAYED_KEY = 'GP'

# Class to represent each individual player
class Player:

    def __init__(self, player_data_dictionary):
        # A dictionary with stats and keys to find the stats
        self.stats = player_data_dictionary
        
    def __str__(self):
        return self.stats[CSV_NAME_KEY]

    # gets the name of a player from the player object
    def get_name(self):
        # something is weird with the data, so it omits the first letter 
        # which is currently a weird character
        return str(self.stats[CSV_NAME_KEY])[1:]
        
    # returns the pergame stat in a specified category
    def per_game(self, category):
        return int(self.stats[category])/ int(self.stats[CSV_GAMES_PLAYED_KEY])

    #  returns a stat in a specified category
    def get_stat(self, category, per_game):
        # sends back 0 if player hasn't played any games
        if per_game:
            if self.stats[CSV_GAMES_PLAYED_KEY] == 0:
                return 0
            else:
                return float(self.stats[category]) / float(self.stats[CSV_GAMES_PLAYED_KEY])
        else:
            return float(self.stats[category])

# Class to represent a group of players
class Player_Group:

    def __init__(self):
        self.players = {}

    def __str__(self):
        return "List of players with " + str(len(self.players)) + " players"

    def add_player(self, player):
        self.players[player.get_name()] = player

    # returns a list of players
    def get_players(self):
        return self.players
    
    # gets a query and returns a dictionary of key distributional values of players' stats
    def get_stat_range(self, category, per_game):
        #uses minimum stat of first player as placeholder
        min = self.players.values()[0].get_stat(category, per_game) 
        max = 0
        sum = 0
        average = 0
        range = 0
        num = 0 # placeholder for the stat we are extracting for each player
        
        # iterates through players, and calculates max/sum/average
        for player in self.players:
            num = self.players[player].get_stat(category, per_game)
            # checks if it is the max
            if num > max:
                max = num
            
            if num < min:
                min = num
            
            # adds number to sum (for calculating average)
            sum += num
        
        average = sum / len(self.players)
        range = abs(max - min)
        
        
        return {"min":min,"max":max,"average":average,"range":range}
    
    # takes the player group and spits out a new player group based on a filter
    def filter_players(self, category, per_game, comparison, cutoff):
        new_player_group = Player_Group()
        
        # filters based on if stats GREATER THAN cutoff
        if comparison == ">":
            for player in self.players:
                if self.players[player].get_stat(category, per_game) > cutoff:
                    new_player_group.add_player(self.players[player])
        
        # filters based on if stats LESS THAN cuttoff
        if comparison == "<":
            for player in self.players:
                if self.players[player].get_stat(category, per_game) < cutoff:
                    new_player_group.add_player(self.players[player])
        
        return new_player_group
        
def import_data(csv_filename):
    
    # Takes CSV file and returns a Player_Group from it

    csv_data_dump = [] # dump of the data from excel
    column_dict = {} # legend for what each column represents
    player_list = Player_Group()

    # Opens CSV and adds lines to csv_data_dump list
    csv_file = open(csv_filename)
    for line in csv.reader(csv_file):
        csv_data_dump.append(line)

    
    # Pop's the first element from player_list which is headers
    # Creates a dictionary of what column represents what stat
    stat_categories = (csv_data_dump.pop(0))

    for category in stat_categories:
        column_dict[category]= stat_categories.index(category)

    # Takes csv_data_dump and extracts players from it
    # Creates a dictionary of each players stats
    # Adds players to a player group
    for player in csv_data_dump:
        player_stat_dictionary = {}

        for key, value in column_dict.items():
            player_stat_dictionary[key] = player[value]    


        player_list.add_player(Player(player_stat_dictionary))

    return player_list

def create_graph(player_group, x_coordinate, y_coordinate, z_coordinate, per_game):
    # z category (size of circle) find range of values
    z_stat_range = player_group.get_stat_range(z_coordinate, per_game)
    z_category_range = z_stat_range["range"]
    z_category_max = z_stat_range["max"]
    z_category_min = z_stat_range["min"]
    
    for player in player_group.get_players().values():
        x = player.get_stat(x_coordinate, per_game)
        y = player.get_stat(y_coordinate, per_game)
        z = player.get_stat(z_coordinate, per_game)
        # label name
        lbl = str(player.get_name())
        
        # determines size of dot based on where it is in z distribution    
        plt.scatter(x,y,s=(DOT_SIZE + DOT_SIZE*5*((z-z_category_min)/(z_category_range))))
        
        # Titles axis based on whether PG being used or not
        if per_game:
            plt.xlabel(x_coordinate + "PG")
            plt.ylabel(y_coordinate + "PG")
            plt.title("X-" + x_coordinate + "pg" + \
            ", Y-" + y_coordinate + "pg" + ", Bubble Size-" + z_coordinate + "pg")
            
        else:
            plt.xlabel(x_coordinate)
            plt.ylabel(y_coordinate)
            plt.title("X-" + x_coordinate + ", Y-" + y_coordinate + ", Bubble Size-" + z_coordinate)
            
        plt.annotate(lbl, xy=(x,y), xytext=(x,y))
    
    plt.show()

def compare_player_groups(player_group_recent, player_group_old):
    # creates a new_player group that will have compared
    # players in a variety of stat categories
    new_player_group = Player_Group()

    # Finds the stat categories that exist which can be compared and creates a list
    example_player = player_group_recent.get_players().values()[0]
    stat_categories = []
    
    # Check which stat categories contain digits 
    for stat_category in example_player.stats:
        if example_player.stats[stat_category].isdigit():
            stat_categories.append(stat_category)
    
    # goes through player_group_recent, and checks if player_group_old
    # contains same player, if so does a comparison based on PG stats
    # and creates a new player with these compared stats as stats
    # and adds to new_player_group
    
    for player_name in player_group_recent.get_players():
        player_data_dictionary = {}
        
        if player_name in player_group_old.get_players().keys():
            for stat in stat_categories:
                player_data_dictionary[stat] = (player_group_recent.get_players()[player_name].get_stat(stat,True) - player_group_old.get_players()[player_name].get_stat(stat,True))
            
            # adds player name category to the player data dictionary
            player_data_dictionary[CSV_NAME_KEY] = player_group_recent.get_players()[player_name].stats[CSV_NAME_KEY]
            
            # adds the player to new_player_group
            new_player_group.add_player(Player(player_data_dictionary))            
        
    return new_player_group
    
def player_ranking_system(player_group, categories, per_game):
        # Will assign a numerical value to each player for comparison
        # is passed a player group, a list including categories and their weights
        
        # creates a list of stat categories with their min/max values and weights
        # stat part of list includes dictionary with min/max/average/range
        print categories
        print player_group.get_stat_range("G", False)
        
        stat_categories = []
        player_rankings = []
        
        for category in categories:
            stat_categories.append([category[0], category[1], player_group.get_stat_range(category[0], per_game)])
            
        player_score = 0
        
        for player in player_group.get_players().values():
            for category in stat_categories:
                player_score += category[1]*((player.get_stat(category[0],per_game) - category[2]["min"])/category[2]["range"])
    
            player_rankings.append([player.get_name(), player_score])
            player_score = 0
        
        player_rankings.sort(key=lambda x: x[1])
        
        # appends ranking # to player group
        max_rank = len(player_rankings)
        rank = max_rank
        
        for player in player_rankings:
            player.insert(0,rank)
            rank -= 1
        
        return player_rankings
            

# Imports two CSV files as the groups of players to compare            
old_test_group = import_data('STATS20161120.csv')
recent_test_group = import_data('STATS20170115.csv')

# Filters test groups, based on absolute amounts (False) or per game amounts (True)
old_test_group = old_test_group.filter_players("GP",False,">",5)
recent_test_group = recent_test_group.filter_players("GP",False,">",5)
recent_test_group = recent_test_group.filter_players("Pts",True,">",0.5)
compared_group = compare_player_groups(recent_test_group, old_test_group)

# Creates a graph
create_graph(compared_group,"G","A","SOG",False)    

# Pulls players rankings based on categories & weights
player_rankings = player_ranking_system(recent_test_group,[["Hits",1],["SOG",1],["G",1],["A",1],["PPG",0.5],["PPA",0.5]],True)

# Prints player rankings to the cmd line
for player in player_rankings:
    print player

# Allows user to search player rankings for a specific player
while True:
    search_player = raw_input("What player would you like to search (END to exit): ")
    if search_player == "END":
        break

    for player in player_rankings:
        if player[1]== search_player:
            print player
