"""This module handles non-object-specific input/output functions.
    
    External functions:
    - clear_screen:  Clears the screen
    - get_string:  Prints a prompt and returns user's text.
    - input_from_menu:  Creates a menu and returns the user's choice(s).
    - print_string:  Prints introductory text and a string.
    - welcome_screen:  Clears the screen and prints introductory text.
    - yes_no:  Prompts user to answer a yes or no question.
    
    Internal functions:
    - _build_options_list:  Builds one- or two-character equivalents for
       a list of options
    - _evaluate_response:  Checks user response for validity and takes
       appropriate action
"""

import os

LINE_LENGTH = 70

def clear_screen():
    """Clears the screen.
    
        Arguments:  None.
        
        Returns:  Nothing.
    """
    os.system("cls" if os.name == "nt" else "clear")
# end function


def get_string(prompt="Enter text:  ", clear=False):
    """Prints a prompt and returns user's text.
    
    - Named arguments:
    - clear -- Clears the screen before displaying the prompt.
    - prompt -- Prompt to display (default generic prompt).
        
    Returns:  A string with the user's response, or an empty string.
    """
    text = ""
    if clear:
        clear_screen()
    text = input(prompt)
    return text
# end function


def input_from_menu(
    options, option_type="options", confirm=False, allow_keystroke=False,
    keystroke_list=[], can_choose_multiple=False, can_show_help=False,
    help_text=""):
    """Builds a menu of choices and returns the user's choice(s).
        
        Arguments:
        - options -- a list of choices, must be a simple list
        
        Keyword arguments:
        - option_type -- label for the thing(s) being chosen (default
         "options").
        - confirm -- Displays the user's choice(s) for confirmation
         before returning (Default False).
        - allow_keystroke -- allows user to make choice(s) with one- or
         two-letter entries (Default False)
        - keystroke_list -- allows caller to override the menu-building
         function by supplying a list of one- or two-letter keystrokes
         to represent each option.  Ignored if allow_keystroke is
         False.  See _build_options_list fucntion for formatting
         specifications (Default empty list).
        - can_choose_multiple -- user can make more than one choice
         (default False).
        - can_show_help -- user can choose "H" to see explanations of
         each choice (default False; also disabled if caller fails to
         supply help_text).
        - help_text -- Contextual help to be displayed if the user
         chooses, can/must be formatted as the caller wishes (default
         empty string; ignored if can_show_help is False).
    
        Returns:  a tuple consisting of: a bool indicating whether or
         not the user made a choice; and a list containing the user's
         choice(s), if any.
    """
    # Initialize.
    output = ["Please select "]
    # Build prompt.
    if can_choose_multiple:
        output[0] += "one or more of the following " + option_type + ":"
    else:
        output[0] += "from the following " + option_type + ":"
    # Build options list.
    options_list, options_dict = _build_options_list(
        options, allow_keystroke, keystroke_list)
    output.append(options_list)
    if can_choose_multiple:
        output.append(
            "Separate multiple " + option_type + " with commas (,).")
    # Build non-list options.
    if can_show_help and (help_text != ""):
        output.append(
            "Type [H] for Help, or " + "[Q] to go back.")
    else:
        output.append("Type [Q] to go back.")
    output.append("Press [ENTER] to submit.")
    # Main response loop.
    valid = False
    # Loop until valid selection is made.
    while valid == False:
        # Print the menu text and prompt.
        for line in output:
            print(line)
        response = input(">>  ")
        if response == "":
            # User just hit Enter.
            print("You did not make a choice.")
            continue
        # _evaluate_response returns:
        #  False and an empty list if user entered "H" or an invalid
        #   response;
        #  True and a list of responses if the user entered one or more
        #   valid responses;
        #  True and an empty list if the user entered "Q".
        valid, choice = _evaluate_response(
            response, options_dict, confirm, can_choose_multiple,
            can_show_help, help_text)
    # If the user entered "Q", return False, else return True and the
    #  response list.
    if len(choice) == 0:
        return False, choice
    else:
        return True, choice
# end function


def print_string(string, intro="Output:  ", clear=False):
    """Prints some introductory text and a string.
    
        - Arguments:
        string -- the string to print.
        
        - Keyword arguments:
        intro -- Text to print before the string (default generic text).
        clear -- Clear the screen before printing (default False).
        
        Returns:  Nothing.
    """
    if clear:
        clear_screen()
    print(intro, string)
# end function


def welcome_screen():
    """Clears the screen and prints introductory text.
    
        Arguments: None
        
        Returns:  Nothing
    """
    
    clear_screen()
    print("Welcome to Treehouse Python Techdegree Project 2:")
    print("Secret Messages!\n")
    print("Implemented by Steven Tagawa\n")
# end function


def yes_no(prompt, clear=False):
    """Prompts the user to answer a yes or no question.
    
    - Arguments:
    prompt -- The question to be answered.
    clear -- Clear the screen first (default False).
    
    - Returns:  True if the user answers yes, False if no.
    """
    
    if clear:
        clear_screen()
    valid = False
    while valid == False:
        response = input(prompt + " [Y]/[N] >>")
        if "Y" in response.upper():
            return True
        elif "N" in response.upper():
            return False
        else:
            print("That wasn't a 'yes' or a 'no'...\n")
        # end if
    # end while
# end function


def _build_options_list(options, allow_keystroke, keystroke_list):
    """Takes a list of options and creates equivalent responses.

    Arguments:
    - options -- a list of options.
    - allow_keystroke -- allows user to make choice(s) with one-letter
       entries.  (If False, all options are mapped to their full names,
       and the list of options is returned unchanged for display.)
    - keystroke_list -- a list of keystroke equivalents.  Ignored if
       allow_keystroke is False.
       
      keystroke_list formatting:
       Each entry in keystroke_list must be unique.  "H" and "Q" are
       reserved and may not be used.  Entries are not case-sensitive;
       upper-case letters will be displayed.  Keystroke shortcuts are
       inserted in the first place they appear; if the character(s) is
       not in the option name, it will be prefixed to the option.  To
       skip over an option, pass None in keystroke_list for that option.
       To require the user to select options by number, pass ## as the
       first item in keystroke_list.  The remainder of the list will be
       ignored and the options mapped to numbers.
              
    Returns:  a string containing the list of options, formatted for
     display, and a dictionary mapping each option to its keystroke
     equivalent.
    """
    # Initialize.
    output_string = ""
    output_dict = {}
    
    # If allow_keystroke is False, just build the dictionary with
    #  values equal to keys, and build the output string from the list.
    if not allow_keystroke:
        output_string = ", ".join(options)
        for option in options:
            output_dict[option.upper()] = option
        # end for
        output_string = break_string(output_string, LINE_LENGTH)
        return output_string, output_dict
    # end if (function exits)
    # If keystroke_list exists and its first item is "##", just assign
    #  all options to numbers.
    if keystroke_list and keystroke_list[0] == "##":
        for key, option in enumerate(options):
            output_string += "[" + str(key + 1) + "]" + option
            if key < (len(options) - 1):
                output_string += ", "
            output_dict[str(key + 1)] = option
        # end for
        output_string = break_string(output_string, LINE_LENGTH)
        return output_string, output_dict
    # end if (function exits)
    # Otherwise, loop through the options, assigning keystroke shortcuts
    #  for each and mapping them.
    # Iterate through the options
    for key, option in enumerate(options):
        # If we haven't reached the end of keystroke_list, get the entry
        #  for this option, otherwise set to None.
        if key <= len(keystroke_list):
            keystroke = keystroke_list[key].upper()
        else:
            keystroke = None
        # end if
        if keystroke:
            # Look for the keystroke within the option:
            found = option.upper().find(keystroke)
            if found >= 0:
                # If found, insert the keystroke.
                display = (
                    option[0:found] + "[" + keystroke.upper() + "]" + 
                    option[found + len(keystroke):])
            else:
                # If not found, append to the beginning of the option.
                display = "[" + keystroke + "]" + option
            # end if
        else:
            # If there is no keystroke for option...
            display = option
            key = option.upper()
        # end if
        output_string += display
        if key < (len(options) - 1):
            output_string += ", "
        output_dict[keystroke] = option
    # end for        
    output_string = break_string(output_string, LINE_LENGTH)
    return output_string, output_dict
# end function
           

def _evaluate_response(
    response, options_dict, confirm, can_choose_multiple, can_show_help, help_text):
    """Takes user input and maps to one or more choices.
    
    Arguments:
    - response -- the user's input
    - options_dict -- dictionary of valid responses
    
    Returns:  True and a list of chioces if the user selected one or
    more valid choices; True and an empty list if the user selected
     Quit; False and an empty list if the user selected Help or an
     invalid choice.
    """
    
    choices = []
    # Upper-case.
    response = response.upper()
    # Split into a list of responses. (Don't use ", " because the user
    #  might not put spaces after commas.)
    response_list = response.split(",")
    # If the user made too many choices, quit immediately.
    if (len(response_list) > 1) and (not can_choose_multiple):
        print("Sorry, you can only select one from this list.")
        return False, []
    # end if (function exits)
    # Strip leading space, if any.
    for choice in range(len(response_list)):
        response_list[choice] = response_list[choice].strip()
    # If user selected "H", show help if available.
    help_ = False
    quit = False
    for choice in response_list:
        if choice == "H":
            help_ = True
            break
        elif choice == "Q":
            quit = True
            break
        # end if
    # end for
    if help_:
        if can_show_help and (help_text != ""):
            print(help_text)
            input("Press [Enter] to proceed.")
        else:
            print("Sorry, help is not available for this menu...\n")
        # end if
        return False, []
    # end if (function exits)
    # if user selected "Q", quit the menu.
    if quit:
        if confirm:
            valid = False
            while not valid:
                check = input("Are you sure you want to go back? (Y/N):  ")
                if check.upper() == "N":
                    return False, []
                elif check.upper() == "Y":
                    valid = True
                # end if
            # end while
        # end if
        return True, []
    # end if (function exits)
    # Loop through the response list and register user's choices.  Exit
    #  on any invalid choice.
    for choice in response_list:
        # Here check the choice against keystroke list (which may be the
        #  full option names in upper-case).
        if (choice.upper() in options_dict):
            choices.append(options_dict[choice.upper()])
        else:
            # User always has the option of typing out the full word
            #  (case-insensitive).  Check here to see if they did.
            #  (Need to loop through values manually to make a case-
            #  insensitive search.)
            found = False
            for value in options_dict.values():
                if choice.upper() == value.upper():
                    choices.append(value)
                    found = True
                    break
                # end if
            # end for
            if found == False:
                print("Sorry, " + choice + " is not a valid option.")
                return False, []
        # end if
    # end for
    if confirm:
        valid = False
        while not valid:
            check = input(
                "Proceed with " + ", ".join(choices) + "? (Y/N):  ")
            if check.upper() == "N":
                return False, []
            elif check.upper() == "Y":
                valid = True
            # end if
        # end while
    return True, choices
# end function
    
    
def break_string(string, length):
    """Attempts to line break a long string intelligently.
    
    Arguments:
    - string -- the string to be broken.
    - length -- the maximum length of the line.
    
    Returns:  the line broken string.
    """
    break_list = []
    # Go through the string at points of maximum length, until the
    #  string remaining is less than a line.
    while not (length > len(string)):
        # Step backwards looking for a space
        pos = length
        while string[pos] != " ":
            pos -= 1
        # end while
        # In the event that there are no spaces along the entire length
        #  of a line...
        if pos == 0:
            # Take the string up to the next to the last character in
            #  line, and slice it out of the string.
            scratch = string[:length-1]
            string = string[length-1:]
            # Add a hyphen as the last character, add a newline
            #  character, and append it to the list.
            scratch += "-\n"
            break_list.append(scratch)
        else:
            # Take the string up to (and including) the space, and slice
            #  it out of the string.
            scratch = string[:pos+1]
            string = string[pos+1:]
            # Add a newline character and append it to the list.
            scratch += "\n"
            break_list.append(scratch)
        # end if
    # end while
    # Append the remainder of the string to the list.  (If the while
    #  loop never triggered, the whole string will be the only item in
    #  the list.)
    break_list.append(string)
    # If the string was broken, reconstitute it now.  (If the string is
    #  only one line, this loop doesn't really do anything.)
    string = ""
    for line in break_list:
        string += line
    # end for
    return string
# end function