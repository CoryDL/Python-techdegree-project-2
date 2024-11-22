import constants
import copy



def clean_data():
    players_copy = copy.deepcopy(constants.PLAYERS)  # read the existing player data from the PLAYERS constants provided in constants.py
                                                     # cleaning the player data using copy.deepcopy()
    cleaned_players = []  # creating a new empty list to move our cleaned data into
    for player in players_copy:  # each dictionary in the list is representing a player
        fixed = {}  # creating an empty dictionary for each player called fixed, to enter our new formatted into
        fixed['name'] = player['name']  # moving the "name" keys and values from the old dictionary to the new one unchanged 
        fixed['guardians'] = ", ".join(player['guardians'].split(" and ")) # adding "guardians" as a list with each guardian as a separate item
        if player['experience'] == 'YES':
            fixed['experience'] = True  # adding key for "experience" and changing the value from a string to a boolean... here True
        else:
            fixed['experience'] = False  # ... here False
        fixed['height'] = int(player['height'].split()[0])  # adding key for "height", values as an integer instead of a string value
        cleaned_players.append(fixed)  # adding the new dictionaries to the "cleaned_players" list
    return cleaned_players  # returning the cleaned_players list to be used in other functions


def print_header():
    print("  \U0001F3C0   BASKETBALL  \U0001F3C0""\n  _ TEAM STATS TOOL _ ""\n\n")  # printing out the title of the app here so it doesn't loop


def experience_tiers():  # function to help the balance_teams() function assign players to each team with even numbers of experienced and inexperienced players
    all_players = clean_data()  # getting the cleaned data from the function clean_data()
    experienced_players = []  # empty list for the experienced
    inexperienced_players = []  # empty list for the experienced
    for player in all_players:  # looping through the players assigned to the team and adding them to the appropriate list
        if player['experience'] == True:
            experienced_players.append(player)
        else:
            inexperienced_players.append(player)
    return experienced_players, inexperienced_players  # returning each list for use in the balance_teams() function


def balance_teams():  # basically this is like each team taking turns to pick an experienced player until there are none left, and then picking an inexperienced player until all players are picked
    teams_copy = copy.deepcopy(constants.TEAMS)  # creating a copy of the teams data
    number_of_teams = len(teams_copy)  #  creating a variable that holds the number of teams (in case the data changes at some point)
    team_index = 0  # creating a variable that I'll use later to keep track of the index numbers of the teams
    experienced, inexperienced = experience_tiers()  # utilizing the lists created by the experience_tiers() function
    balanced_team_rosters = []  # creating an empty list to hold the team rosters
    for team in teams_copy:  # looping through each team
        balanced_team_rosters.append([])  # adding an empty list for each team
    while experienced:  # popping a player off of the experienced list and adding it to a team before moving on to the next until there are no more players in the list
        for player in experienced:
            balanced_team_rosters[team_index].append(experienced.pop(experienced.index(player)))
            team_index += 1
            if team_index == number_of_teams:
                team_index = 0
    while inexperienced:  # popping a player off of the inexperienced list and adding it to a team before moving on to the next until there are no more players in the list
        for player in inexperienced:
            balanced_team_rosters[team_index].append(inexperienced.pop(inexperienced.index(player)))
            team_index += 1
            if team_index == number_of_teams:
                team_index = 0
    return balanced_team_rosters  # returns a multi-dimensional list of team rosters


def menu():  # organizing the menu and handling user inputs and exceptions
    teams_copy = copy.deepcopy(constants.TEAMS)
    team_selection_numbers = []  # creating a list of acceptable inputs to check against in the exception handling
    team_number = 1  #  starting the team selection options at 1, there are only 3 but in a real-world scenario more could be added later
    print("    ---- MENU ----\n\n")
    print(" Here are your choices:\n\n  A) Display Team Stats\n  B) Quit")
    while True:
        try:
            menu_options = input("\n\n Enter an option: ")
            if menu_options.upper() not in ('A', 'B'):  # there are only 2 options in this part of the menu so I hard coded them
                raise ValueError("{} is not a valid input. Please enter either 'A' or 'B'".format(menu_options))
        except ValueError as err:
                print(f"{err}")
        else: 
            if menu_options.upper() == 'A':
                print("\n\n")
                break
            else:
                print("\nThe app is now closing.\n")
                exit()
    for team in teams_copy:
        team_selection_numbers.append(team_number)
        print("  {}) {}".format(team_number,team))  # printing the team names with a number to select them. If more teams are added to the data they will display
        team_number += 1
    while True:
        try:
            team_options = int(input("\n\n Enter an option: "))
            if team_options not in team_selection_numbers:
                raise ValueError("{} is not a valid input. Please select the number associated with your team. ".format(team_options))
        except ValueError as err:
                print(f"{err}")
        else:
            print("\n\n")
            display_stats(team_options)
            break


def replay():  # replay function to start the application over at the menu, dealing with any exceptions
    while True:
        try:
            replay = input("Press ENTER to continue: ")
            if replay != "":  # we haven't learned about any key presses yet so I just left an empty string so the enter key would trigger
                raise ValueError("Press ENTER to continue: ")
        except ValueError as err:
                print(f"{err}")
        else:
            print("\n\n\n\n")
            menu()
            break


def display_stats(team_options):  # Displaying all of the team stats using the oraganized data
    teams_copy = copy.deepcopy(constants.TEAMS)  # creating a copy of the teams data
    team_name = teams_copy[(team_options - 1)]  # getting the index of the selected team name in the teams_copy list
    team_rosters = balance_teams()  # getting the team rosters from the balance_teams() function
    player_count = len(team_rosters[team_options - 1])  # figuring out the number of players on the team and assigning it the player_count variable
    team_player_names = [player['name'] for player in team_rosters[(team_options - 1)]]  # assigning a variable to the player name values from the team roster list
    team_guardian_names = [player['guardians'] for player in team_rosters[(team_options - 1)]]  # assigning a variable to the guardian name values from the team roster list
    team_heights = [player['height'] for player in team_rosters[(team_options - 1)]]  # assigning a variable to the player height values from the team roster list
    experienced_player_count = 0  # creating a variable to hold the number of experienced players on the team
    height_average = round(sum(team_heights) / len(team_heights),1)  # calculating the average height of the players on the team, rounding it to the nearest tenth, and assigning a variable to the value
    for player in team_rosters[(team_options - 1)]:  # looping through the team roster to find the experienced players to calculate the value held by the experienced_player_count variable
        if player['experience'] == True:
            experienced_player_count += 1
    print("Team : {} Stats\n________________\n\n".format(team_name),  # using the variables we created to display all of the stats
        "Total Players: {}\n".format(player_count),
        "Total Experienced: {}\n".format(experienced_player_count),
        "Total Inexperienced: {}\n".format(player_count - experienced_player_count),
        "Average Height: {}\n".format(height_average),
        "\n\nPlayers on Team:  \n" , ", ".join(team_player_names),
        "\n\nGuardians:  \n" , ", ".join(team_guardian_names),
        "\n\n")
    replay()  # Calling the replay() function to prompt the player to continue or quit


if __name__ == "__main__":  # Dunder main, calling the print_header() function to print the header upon starting, then calling the menu() function the first time.
    print_header()
    menu()
