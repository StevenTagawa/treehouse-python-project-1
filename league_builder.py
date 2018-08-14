# This is Project 1 for the Treehouse Python Techdegree:  Build a Soccer League

# NOTE: This script is a reconstruction.  The original working script was deleted from Workspaces
#  in the process of setting up synchronization with Github.  Due to the complexity of the script,
#  this reconstruction is probably not identical to the original.


# IMPORTS
import csv


# 'CONSTANTS' (Can be set by user but not intended to change.)
INPUT_FILE = "soccer_players.csv"
OUTPUT_FILE = "teams.txt"
TEAMS = [["Dragons"], ["Sharks"], ["Raptors"]]
# The minimum number of players per team for any age group is four (8 and under).  This can be
#  changed for other age groups.
VALID_KEYS = ["Name", "Height (inches)", "Soccer Experience", "Guardian Name(s)"]
MIN_PLAYERS_PER_TEAM = 4
PRACTICE_DATE_TIME = "Wednesday, September 12, 2018, at 3:30pm"

# -------------------------------------------------------------------------------------------------
# FUNCTIONS


# read csv file function
# Pass:  filename, delimiting character (optional, defaults to ",")
# Return:  list of dictionaries, list of keys, message if open failed
def read_csv_file(filename, delim = ","):
    # Try to open and read the file, catch the error if unsuccessful.  NOTE we only catch a
    #  FileNotFoundError--errors in the data should be caught by the data checking function.
    try:
        with open(filename, newline = "") as csvfile:
            # First, read all of the data into a list of dictionaries.
            player_data = list(csv.DictReader(csvfile, delimiter = delim))
        # end with (closes file)
        
        # Since DictReader does not preserve the key fields separately, we need to re-open the file
        #  and get the keys.
        with open(filename, newline = "") as csvfile:
            key_list = next(csv.reader(csvfile, delimiter = delim))
        # end with (closes file)
        return player_data, key_list, ""
    except FileNotFoundError:
        return [], [], "The input file couldn't be found."
    # end try
    # end function


# write txt file function
# Pass:  filename, output (a list of strings, each representing a logical line), optional new line
#  character
# Return:  message if the write failed (doesn't specify the error)
def write_txt_file(filename, output, new_line = "\n"):
    msg = ""
    try:
        # Overwrite any previous version of the file.
        with open(filename, "w") as txtfile:
            for line in output:
                txtfile.write(line + new_line)
            # end for
        # end with (closes file)
    except:
        msg = "Error writing output file."
    # end try
    return msg
    # end function
        

# copy list function
# Pass:  old list (list of objects)
# Return:  new list
def list_copy(old_list):
    new_list = []
    for item in old_list:
        # In order for this to work on both lists of dictionaries and lists of lists, we need to
        #  use the list() function on lists, but not on dictionaries.
        if type(item) == list:
            new_item = list(item)
        else:
            new_item = item
        # end if
        new_list.append(new_item)
    # end for
    return new_list
    # end function


# check data function
# Pass:  input data (a list of dictionaries)
# Return:  True if the data passes all checks, False otherwise
def valid_data(player_data, keys, VALID_KEYS):
    # Initialize.
    valid = True
    # The function calls two subfunctions, one which checks to make sure that the key fields in the
    #  input file matches what is expected, and one which runs validity checks on the data.
    
    # First check the key fields.
    valid = check_keys(VALID_KEYS, keys)
    # Only check the data if the keys are valid.
    if valid:
        valid = check_data(player_data)
    # end if
    return valid
    # end function


# check keys function
# Pass:  a list of expected key fields, the actual key fields from the input file
# Return:  True if the keys are present
def check_keys(VALID_KEYS, keys):
    # Initialize (will be flipped if anything fails).
    valid = True
    # Iterate through the expected keys.
    for valid_key in VALID_KEYS:
        if not valid_key in keys:
            print("The input file does not contain expected", valid_key, "data.")
            valid = False
        # end if
    # end for
    return valid
    # end function


# check data function
# Pass:  master list of player data
# Return:  True if the data is valid, False otherwise
def check_data(player_data):
    # This function type-checks the actual data.  It would be nice to have the function loop once
    #  through the player data and check all conditions simultaneously, but since we don't want to
    #  keep checking after a condition has failed once, it would get complicated having the loop
    #  check some conditions but not others for some iterations.
    
    # << The valid_data function was originally one long function combining a project-specific
    #  version of the check_keys function and this function.  After peer review it was suggested
    #  that valid_data be broken into two separate functions.  In the process I re-imagined the
    #  piece of code that specifically checked for the four key names as a generic function that
    #  can accept any list of key names and check them against the fields in a csv file.  I also
    #  had ideas about generalizing the code below as a set of functions that would check (and,
    #  if desired, convert) a particular type--one for ints, one for bools, one for strings, etc.
    #  But in the interest of moving forward (and since I've tested this code and it works) I opted
    #  not to go completely insane with the refactoring. >>
    
    #Initialize.
    valid = True
    # Since the height data is inputted as strings, convert them to integers.  An error ends
    #  checking.
    for player in player_data:
        try:
            player["Height (inches)"] = int(player["Height (inches)"])
        except ValueError:
            print("The input file contains invalid height data.")
            valid = False
            break
        # end try
    # end for
    
    # Check that the entries under "Soccer Experience" are either "YES" or "NO".  (Without this,
    #  the script would treat anything that is not "YES" as "NO"...but this also ensures that no
    #  entry is empty or has nonsense.)
    for player in player_data:
        if (player["Soccer Experience"].upper() != "YES") and (player["Soccer Experience"].upper() != "NO"):
            print("The input file contains invalid experience data.")
            valid = False
            break
        # end if
    # end for
    
    # The script cannot verify that the name fields contain actual names, but it can verify that
    #  they are:  1) not empty, and 2) not purely numeric.
    # Loop through the list, checking player names.
    for player in player_data:
        # Check if it's empty.
        if len(player["Name"]) == 0:
            print("The input file contains invalid player name data.")
            valid = False
            break
        # end if
        # If it isn't, try to convert it into an int.  The string passes if the attempt DOESN'T
        # work.
        try:
            x = int(player["Name"])
            print("The input file contains invalid player name data.")
            valid = False
            break
        # If the try block throws an error, the data is good.  Do nothing.
        except ValueError:
            pass
        # end try
    # end for
    # Do the same for guardian name(s).
    for player in player_data:
        if len(player["Guardian Name(s)"]) == 0:
            print("The input file contains invalid guardian name data.")
            valid = False
            break
        # end if
        # If it isn't, try to convert it into an int.  The string passes if the attempt DOESN'T
        # work.
        try:
            x = int(player["Guardian Name(s)"])
            print("The input file contains invalid guardian name data.")
            valid = False
            break
        # If the try block throws an error, the data is good.  Do nothing.
        except ValueError:
            pass
        # end try
    # end for
    # If any of the conditions failed, end checking
    if valid == False:
        return False
    # end if (function exits)
    
    # End if there aren't enough children listed to distribute between the number of
    #  teams.
    if (len(TEAMS) * MIN_PLAYERS_PER_TEAM) > len(player_data):
        print("There aren't enough children to distribute between the specified number of teams.")
        return False
    # end if (function exits)
    
    # And finally, if the list of teams is empty, report that.
    if len(TEAMS) == 0:
        print("There are no teams defined.")
        return False
    # end if (function exits)
    
    # If everything passed, return True.
    return True
    # end function


# sort players function
# Pass:  player data (list of dictionaries), rosters (list of lists)
# Return:  Notes if any are generated (rosters is modified directly)
def sort_players(player_data, rosters):
    # Required:  distribute experienced players between teams as evenly as possible.
    # Preferred:  distribute players by height as evenly as possible.
    
    # Initialize counters, flags, etc.
    number_of_experienced_players = 0
    pick_experienced_players = True
    pick_tallest = True
    height = 0
    number_of_teams = len(rosters)
    next_team = 0
    last_team = number_of_teams - 1
    counter = 1
    notes = ""
    
    # If the number of children playing will not divide evenly between the teams, generate a
    #  warning.
    extra_players = len(player_data) % number_of_teams
    # Anything over zero will evaluate as True.
    if extra_players:
        print("Warning: ", str(extra_players), "teams will have an additional player.")
        notes += str(extra_players) + " teams have an additional player.\n"
    # end if
    
    # Count the number of experienced players.
    for player in player_data:
        if player["Soccer Experience"].upper() == "YES":
            number_of_experienced_players += 1
        # end if
    # end for
    # If there are no experienced players, flip the pick_experienced_players flag.
    if number_of_experienced_players == 0:
        pick_experienced_players = False
    # end if
    
    # If the number of experienced players will not divide evenly between the teams, generate a
    #  warning.
    extra_experienced_players = number_of_experienced_players % number_of_teams
    # Anything over zero will evaluate as True.
    if extra_experienced_players:
        print("Warning: ", str(extra_experienced_players), "teams will have an additional experienced player.")
        notes += str(extra_experienced_players) + " teams have an additional experienced player.\n"
    # end if
       
    # Main sorting loop.  The loop begins by searching through the list for the tallest child,
    #  assigning him/her to the first team, and removing him/her from the list.  The loop
    #  continues to assign the tallest children remaining until each team has one player.  The loop
    #  then shifts to searching for the shortest children.  The loop continues in this fashion as
    #  long as there are enough children left to put at least one more on each team.
    
    # Loop until player list is empty.
    while len(player_data) > 0:
        # We use enumerate here because we use the index number to track the chosen child.
        for index, player in enumerate(player_data):
            # Set the first child's height as the default to compare against.
            if index == 0:
                height = player["Height (inches)"]
            # end if
            # The complex if statement below returns True if:  1) the current child is the tallest
            #  encountered so far AND we are picking tall children; OR 2) the current child is the
            #  shortest encountered so far AND we are picking short children.  This allows the
            #  code inside to be used for picking both tall and short children.  Using >= and <=
            #  results in the last of multiple children with the same height to be picked first,
            #  but this has no effect on the distribution, and keeps the function operating
            #  correctly when all the remaining children are the same height (or there is only one
            #  child left).
            if ((player["Height (inches)"] >= height) and (pick_tallest == True)) or ((player["Height (inches)"] <= height) and (pick_tallest == False)):
                # If we are picking experienced players, the child can be picked only if he/she is
                #  experienced.
                if (pick_experienced_players and (player["Soccer Experience"].upper() == "YES")) or (not pick_experienced_players):
                    # Store this player's index as a potential pick.
                    next_pick = index
                    # Set this player's height as the new bar to compare the remaining children
                    # against.
                    height = player["Height (inches)"]
                # end if
            # end if
        # end for
        
        # Now that the loop has identified the child to be assigned, retrieve his/her information
        #  and add him/her to a team.
        rosters[next_team].append(player_data[next_pick]["Name"])
        # Remove that player from the list.
        del player_data[next_pick]
        # If we are picking experienced players, reduce the number of them by one.
        if pick_experienced_players:
            number_of_experienced_players -= 1
            # If the number of experienced players left is zero, flip the pick_experienced_players
            #  flag.
            if number_of_experienced_players == 0:
                pick_experienced_players = False
            # end if
        # end if
        # If more teams need a player, increment the counter and continue.
        if next_team != last_team:
            next_team += counter
        # If all teams now have the same number of players, and there are enough players left to
        #  assign at least one more to each team, OR if there aren't but there were not any exta
        #  experienced players--
        elif (len(player_data) >= number_of_teams) or ((len(player_data) < number_of_teams) and (not extra_experienced_players)):
            # --reset the team counter--
            next_team = 0
            # --and flip the pick_tallest flag.
            if pick_tallest:
                pick_tallest = False
            else:
                pick_tallest = True
            # end if
        else:
            # This obscure bit of code runs ONLY when the total number of children cannot be evenly
            #  divided between the teams, AND the number of experienced players also could not be
            #  evenly divided between the teams.  In order to prevent teams from receiving both an
            #  additional experienced player and an additional player overall, this code, for only
            #  the final partial run through the player list, REVERSES the order of assignment.
            
            # For example:  Assume a five-team league, with 22 children, 12 of whom are
            #  experienced.  This function would distribute 10 experienced players among the teams,
            #  then assign the two remaining experienced players to Teams 1 and 2.  The function
            #  would then continue assigning children to teams until there were five players on
            #  each team.  If allowed to finish normally, the function would then assign the final
            #  two children to Teams 1 and 2, giving those two teams both six members instead of
            #  five, and three experienced players instead of two.  With this code in place, the
            #  function would instead assign the last two children to Teams 5 and 4, resulting in
            #  two teams with three experienced players instead of two, and two DIFFERENT teams
            #  with six players instead of five.
            
            # To reverse the order of assignment, set last_team to the beginning of the list
            #  instead of the end...
            last_team = 0
            # ...and set the incrementer to count backwards.
            counter = -1
        # end if
    # end while (loop exits when player_data is empty)
    return notes
    # end function


# build league list function
# Pass:  master list of player data (list of dictionaries), rosters (list of lists of names),
#  notes (if any)
# Return:  a final output file to be written
def build_league_list(player_data, rosters, notes):
    # Start with an empty list.  The final output will be a list of strings, each representing a
    #  line.
    output = []
    blank_line = ""
    # First add any notes that were generated.
    if notes != "":
        output.append(notes)
    # end if
    # Loop through each team.
    for team in rosters:
        # Add team name.
        output.append(team[0])
        # Loop through player names.
        for player in team[1:]:
            # Since we can't access a dictionary entry by value, we will just have to look
            #  through the list until we find the right player.
            for player_info in player_data:
                if player_info["Name"] == player:
                    # When we have the right player, build the string with his/her info.
                    output.append(player + ", " + player_info["Soccer Experience"] + ", " + player_info["Guardian Name(s)"])
                    # ...and stop looking.
                    break
                # end if
            # end for
        # end for
        # Add a blank line between teams.
        output.append(blank_line)
    # end for
    return output
    # end function


# generate player letters function
# Pass:  master list of player data (list of dictionaries), rosters (list of lists of names)
# Return:  nothing (function will write all necessary files)
def generate_player_letters(player_data, rosters):
    blank_line = ""
    msg = ""
    # Loop through the teams.
    for team in rosters:
        # ...and through each player.
        for player in team[1:]:
            # Empty output list each time.
            output = []
            # Although the final league list has all of the necessary information, it is not
            #  formatted so that individual player data can be easily extracted.  So we will just
            #  look through the master player list again to get the guardian names.
            for entry in player_data:
                if entry["Name"] == player:
                    # Build the letter output.  This could all be done in one complex statement,
                    #  but it's less readable that way.
                    output.append("Dear " + entry["Guardian Name(s)"] + ",")
                    output.append(blank_line)
                    output.append("Congratulations!  " + player + " will be playing for the " + team[0] + " next season.  The first practice will be on " + PRACTICE_DATE_TIME + ".")
                    # Stop looking.
                    break
                # end if
            # end for
            # Write the letter file.
            filename = ("_".join(player.split())).lower() + ".txt"
            msg = write_txt_file(filename, output)
            if msg != "":
                print(filename + ":  " + msg)
            # end if
        # end for
    # end for
    # end function


# -------------------------------------------------------------------------------------------------
# SCRIPT BEGINS HERE:

# Do not auto-run if loaded into another script.
if __name__ == "__main__":
    
    # First, read in the data file.
    player_data, key_list, msg = read_csv_file(INPUT_FILE)
    # If msg is not empty, the read csv file routine threw an error.  Print the message and skip
    #  the rest of the script.
    if msg != "":
        print(msg)
    else:
        # Now check that the data read in is valid.  Rest of the script runs only if True.
        if valid_data(player_data, key_list, VALID_KEYS):
            
            # Make working copies of the player_data list and the TEAMS list for the sort players
            #  function to modify.
            players = list_copy(player_data)
            rosters = list_copy(TEAMS)
            
            # Sort the players into teams by experience and height.  If there are any notes, the
            #  function will pass them back.
            notes = sort_players(players, rosters)
            
            # Now that the players for each team have been selected, build the final output list.
            #  and write it out.
            league_list = build_league_list(player_data, rosters, notes)
            write_txt_file(OUTPUT_FILE, league_list)
            
            # Finally, generate the individual player letters.
            generate_player_letters(player_data, rosters)
        # end if
    # end if
# end if

# SCRIPT ENDS HERE:
#--------------------------------------------------------------------------------------------------