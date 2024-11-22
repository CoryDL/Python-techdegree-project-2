import constants
import copy


# This function cleans the data in the constants file, by creating a deepcopy, correcting data types
def clean_data():
    players_copy = copy.deepcopy(constants.PLAYERS)
    cleaned_players = []
    for player in players_copy:
        fixed = {}
        fixed['name'] = player['name'] 
        fixed['guardians'] = ", ".join(player['guardians'].split(" and "))
        if player['experience'] == 'YES':
            fixed['experience'] = True
        else:
            fixed['experience'] = False
        fixed['height'] = int(player['height'].split()[0])
        cleaned_players.append(fixed)
    return cleaned_players


# This function prints out the title of the app here, so it only prints when the app is run the first time
def print_header():
    print("  \U0001F3C0   BASKETBALL  \U0001F3C0""\n  _ TEAM STATS TOOL _ ""\n\n")


# This function helps the balance_teams() function assign even numbers of experienced and inexperienced players.
# I separated experienced and inexperienced players into two lists to iterate through.
def experience_tiers():  
    all_players = clean_data()
    experienced_players = []
    inexperienced_players = []
    for player in all_players:
        if player['experience'] == True:
            experienced_players.append(player)
        else:
            inexperienced_players.append(player)
    return experienced_players, inexperienced_players


# This function uses the lists created by the experience_tiers() function. 
# For each team, it pops a player off of the experienced player list and adds it to the team roster.
# It loops through the teams until there are no experienced players left in that list.
# It then does the same for the inexperienced player list.
def balance_teams():
    teams_copy = copy.deepcopy(constants.TEAMS)
    number_of_teams = len(teams_copy)
    team_index = 0
    experienced, inexperienced = experience_tiers()
    balanced_team_rosters = []
    for team in teams_copy:
        balanced_team_rosters.append([])
    while experienced:
        for player in experienced:
            balanced_team_rosters[team_index].append(experienced.pop(experienced.index(player)))
            team_index += 1
            if team_index == number_of_teams:
                team_index = 0
    while inexperienced:
        for player in inexperienced:
            balanced_team_rosters[team_index].append(inexperienced.pop(inexperienced.index(player)))
            team_index += 1
            if team_index == number_of_teams:
                team_index = 0
    return balanced_team_rosters


# This function organizes the menu and handles user inputs and exceptions.
# For the first option I hard coded the choices because I don't expect those to change.
# For the team choice option I wanted to make sure it would still work if more teams are added to the data.
def menu():  
    teams_copy = copy.deepcopy(constants.TEAMS)
    team_selection_numbers = []
    team_number = 1
    print("    ---- MENU ----\n\n")
    print(" Here are your choices:\n\n  A) Display Team Stats\n  B) Quit")
    while True:
        try:
            menu_options = input("\n\n Enter an option: ")
            if menu_options.upper() not in ('A', 'B'):
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
        print("  {}) {}".format(team_number,team))
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


# This function starts the application over at the menu, dealing with any exceptions.
def replay():
    while True:
        try:
            replay = input("Press ENTER to continue: ")
            if replay != "":  # We haven't learned about any key presses yet so I just left an empty string so the enter key would trigger.
                raise ValueError("Press ENTER to continue: ")
        except ValueError as err:
                print(f"{err}")
        else:
            print("\n\n\n\n")
            menu()
            break


# This function displays all of the team stats using the oraganized data
def display_stats(team_options):  
    teams_copy = copy.deepcopy(constants.TEAMS)
    team_name = teams_copy[(team_options - 1)]
    team_rosters = balance_teams()
    player_count = len(team_rosters[team_options - 1])
    team_player_names = [player['name'] for player in team_rosters[(team_options - 1)]]
    team_guardian_names = [player['guardians'] for player in team_rosters[(team_options - 1)]]
    team_heights = [player['height'] for player in team_rosters[(team_options - 1)]]
    experienced_player_count = 0
    height_average = round(sum(team_heights) / len(team_heights),1)
    for player in team_rosters[(team_options - 1)]:
        if player['experience'] == True:
            experienced_player_count += 1
    print("Team : {} Stats\n________________\n\n".format(team_name),
        "Total Players: {}\n".format(player_count),
        "Total Experienced: {}\n".format(experienced_player_count),
        "Total Inexperienced: {}\n".format(player_count - experienced_player_count),
        "Average Height: {}\n".format(height_average),
        "\n\nPlayers on Team:  \n" , ", ".join(team_player_names),
        "\n\nGuardians:  \n" , ", ".join(team_guardian_names),
        "\n\n")
    replay()


# Dunder Main
if __name__ == "__main__":
    print_header()
    menu()
