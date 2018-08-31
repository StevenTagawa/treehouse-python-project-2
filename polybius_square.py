import i_o

from ciphers import Cipher

ALPHANUM = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


class PolybiusSquare(Cipher):
    
    """This class implements the Polybius Square Cipher."""
    
    def __init__(self, mode, text):
        """At initialization, the mode of the object is set and the
        appropriate attribute is set to the original text.
        """
        self.mode = mode
        self.name = "Polybius Square"
        if mode == "Encrypt":
            self.plaintext = text
            self.ciphertext = ""
        else:
            self.ciphertext = text
            self.plaintext = ""
        # end if
    # end method
    
    def __str__(self):
        """Sets plain name for the cipher."""
        return "Polybius Square Cipher"
    
    def decrypt(self):
        """This is the decrypt method.
        
        Arguments:  none.
        
        Returns:  nothing.
        """
        # Before doing anything with the ciphertext, strip it of any
        #  spaces or non-numeric characters, and turn it into a list of
        #  numbers.
        working_list = self._block_input()
        # Loop through the list and decrypt each number.
        for char in working_list:
            num = ((int(char[0]) - 1) * 6) + int(char[1]) - 1
            # Look up the plaintext character and add it.
            self.plaintext += ALPHANUM[num]
        # end for
        # Finally, allow for a one-time pad.
        self._one_time_pad()
        self._intelligent_decrypt()
        return
    # end method
    
    def encrypt(self):
        """This is the encrypt method.
        
        Arguments:  none.
        
        Returns:  nothing.
        """
        # Present the option to perform intelligent encryption.
        self._intelligent_encrypt()
        # Format the plaintext for processing.
        self._format_plaintext()
        # Present the option to use a one-time pad.
        self._one_time_pad()
        # The plaintext is encrypted using the a number substitution.
        working_list = []
        for char in self.plaintext:
            # The assignment can be made in one statement, but for
            #  readability it is broken down here.  Unlike other ciphers
            #  the ciphertext is better stored as a list of numbers.
            index = ALPHANUM.index(char)
            num = (index // 6 * 10) + (index % 6)
            # Finally, add 1 to each digit to eliminate any zeroes.
            working_list.append(num + 11)
        # end for
        # Separate into ten-number lines if the user
        #  chooses.  (This method is overridden by this class.)
        self._block_output(working_list)
        return
    # end method
    
    def _block_input(self):
        """Internal method that overrides the base class method.
        Strips out spaces, non-numeric characters, and breaks the
        input apart into a series of two-digit numbers.
        
        Called by the decrypt method.
        
        Arguments:  none.
        
        Returns:  a list of numbers.
        """
        new_list = []
        held = None
        for char in self.ciphertext:
            # Discard any space and any non-alphanumeric characters.
            if char in ALPHANUM[26:]:
                if held:
                    new_list.append(held + char)
                    held = None
                else:
                    held = char
                # end if
            # end if
        # end for
        return new_list
    # end method
    
    def _block_output(self, working_list):
        """Internal method that overrides the base class method.
        Formats the ciphertext in groups of 25 two-digit numbers
        on each line.
        
        Called by the encrypt method.
        
        Named arguments:
        - working_list -- the list of numbers constituting the
            ciphertext.
        
        Returns:  nothing.
        """
        # Clear the screen.
        i_o.clear_screen()
        working_string = ""
        # If yes, insert a new line every ten numbers.
        if i_o.yes_no(
                "Would you like the encrypted text to be printed in\n" +
                "25-number lines for immproved readability?"):
            # Build an output string, inserting a newline character after
            #  every tenth number.
            working_string = "\n"
            num = 1
            while len(working_list) > 0:
                # Pop numbers off the list one at a time until empty.
                working_string += str(working_list.pop(0)) + " "
                if num < 25:
                    num += 1
                else:
                    working_string += "\n"
                    num = 1
                # end if
            # end while
            self.ciphertext = working_string
            return
        # end method
