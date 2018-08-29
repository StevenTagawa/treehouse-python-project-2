"""This is the script file for Project 2 of the Treehouse Python
Techdegree, Secret Messages.
-----------------------------------------------------------------------
"""

import i_o

from adfgvx import Adfgvx
from affine import Affine
from alberti import Alberti
from atbash import Atbash
from bifid import Bifid
from caesar import Caesar
from hill import Hill
from keyword_ import Keyword_
from polybius_square import PolybiusSquare
from transposition import Transposition

CIPHER_CLASS = {
    "Caesar": Caesar, "Alberti": Alberti, "Affine": Affine, "Atbash":
    Atbash, "Polybius Square": PolybiusSquare, "Transposition":
    Transposition, "ADFGVX": Adfgvx, "Bifid": Bifid, "Keyword": 
    Keyword_, "Hill": Hill}
IMPLEMENTED_CIPHERS = [
    "ADFGVX", "Affine", "Alberti", "Atbash", "Bifid", "Caesar", "Hill", 
    "Keyword", "Polybius Square", "Transposition"]
CIPHER_KEYSTROKES = ["A", "F", "L", "S", "B", "C", "I", "K", "P", "T"]


def main():
    
    """The main script function.
    
    Arguments:  none.
        
    Returns:  nothing.
    """
    
    # Opening screen.
    i_o.welcome_screen()
    running = True
    # Runs until user quits.
    while running:
        # User chooses to encrypt or decrypt here.
        a_choice, action = i_o.input_from_menu(
            ["Encrypt", "Decrypt"], option_type="actions",
            allow_keystroke=True, keystroke_list=["E", "D"], confirm=True)
        # Runs only if user doesn't quit.
        if a_choice:
            action = action[0]
            print("You have chosen to " + action + ".\n")
            # User chooses a cipher here.
            c_choice, chosen_cipher = i_o.input_from_menu(
                IMPLEMENTED_CIPHERS, option_type="ciphers",
                allow_keystroke=True, keystroke_list=CIPHER_KEYSTROKES,
                confirm=True)
            # Runs only if user doesn't quit.
            if c_choice:
                chosen_cipher = chosen_cipher[0]
                print("You have selected " + chosen_cipher + ".\n")
                # User enters text here.
                text = i_o.get_string(
                    "Please enter your text, or [ENTER] to go back:\n>>  ")
                # Runs only if user enters something
                if len(text) > 0:
                    # Create an object of the appropriate cipher class.
                    #  Then call the object's encrypt or decrypt method
                    #  with the user's text.
                    cipher = CIPHER_CLASS[chosen_cipher](action, text)
                    if action == "Encrypt":
                        cipher.encrypt()
                        output = cipher.ciphertext
                    else:
                        cipher.decrypt()
                        output = cipher.plaintext
                    # end if
                    # If the method set nothing, the user aborted.
                    if len(output) == 0:
                        print("Process aborted.")
                    # Else print the result.
                    else:
                        i_o.print_string(output, "Here is your result:  ")
                    # end if
                    # Finished with the instance, so delete it.
                    del cipher
                # end if
            # end if
            repeat = i_o.yes_no("Run again?")
            if not repeat:
                print("Thank you for using Secret Messages!")
                running = False
            # end if
        else:
            print("Thank you for using Secret Messages!")
            running = False
        # end if
    # end while
    # end function


if __name__ == "__main__":
    main()
