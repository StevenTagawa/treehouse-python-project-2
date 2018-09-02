import i_o
import random

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBERS = "0123456789"
PUNCTUATION = """.,?!'":;-"""
INTEL_DICT = {
    "FQ": " ", "JX": " ", "QK": " ", "WZ": " ", "ZJ": " ", "GX": "CAP",
    "HX": ".", "JQ": ",", "PZ": "?", "QG": "!", "QY": "'", "QZ": '"',
    "WQ": ":", "XJ": ";", "ZQ": "-", "ZX": "EOM"}


class Cipher:
    
    """Base class for various cipher classes.
    
    This class exposes two methods, encrypt and decrypt, which are 
    uniquely implemented by each child class (and thus must be
    overridden).  The placeholder classes here serve only to raise an 
    exception if they are not overridden by the child class (but no
    child class that does not override these methods should be
    instantiatable).
    
    The class also contains methods which do not need to be overridden:
    
    - _block_input:  Counterpart to _block_output.  Checks the
        ciphertext for spaces and strips them out if they are present.
        Also turns the ciphertext into all upper-case.
    - _block_output:  Allows the user to encrypt plaintext into five-
        character blocks of ciphertext.  (Inapplicable to decryption:
        regardless of the format of ciphertext input, plaintext is
        outputted as a continuous string unless spaces and punctuation
        have been encrypted.)
    - _format_plaintext:  Takes a plaintext string, strips all spaces
        and converts to all upper-case.
    - _alphabet_from_keyword:  Takes a keyword and returns an alphabet
        consisting of the unique letters in the keyword, followed by the
        remainder of the regular alphabet.
    - _intelligent_decrypt:  The counterpart of _intelligent_encrypt.
        Reads escape sequences in decrypted text and inserts spaces and
        punctuation as needed.
    - _intelligent_encrypt:  Inserts escape sequences in plaintext to
        indicate spaces, capital letters and punctuation.
    - _one_time_pad:  Allows the user to encrypt/decrypt using a one-
        time pad.
    """
    
    def decrypt(self):
        """Default decryption method -- placeholder
        
        Must be overridden to be implemented.
        """
        raise NotImplementedError()
    
    def encrypt(self):
        """Default encryption method -- placeholder
        
        Must be overridden to be implemented.
        """
        raise NotImplementedError()
    
    def _alphabet_from_keyword(self, keyword, include_numbers=False):
        """Internal method that creates a code alphabet from a
        keyword.
        
        Arguments:
        - keyword -- the keyword for the cipher.
        
        Named keywords:
        - include_numbers -- whether to include numbers at the end of
            alphabet (default False)
        
        Returns:  A code alphabet.        
        """
        keyword = keyword.upper()
        # Working code alphabet in a list.
        code_alpha_list = []
        alphabet_string = ""
        # Start with the keyword.
        for letter in keyword:
            if not (letter in code_alpha_list):
                code_alpha_list.append(letter)
        # end for
        for letter in ALPHABET:
            if not (letter in code_alpha_list):
                code_alpha_list.append(letter)
        # end for
        alphabet_string = "".join(code_alpha_list)
        if include_numbers:
            alphabet_string += NUMBERS
        # end if
        return alphabet_string
    # end method
    
    def _block_input(self, make_upper=True):
        """Internal method that strips out any spaces or
        non-alphnumeric characters.
        
        Called by the decrypt method.
        
        Arguments:  none.
        
        Named arguments:
        - make_upper -- allows the caller to specify whether the
            ciphertext should be returned in upper-case (default True).
        
        Returns:  nothing.
        """
        new_text = ""
        for char in self.ciphertext:
            # Discard any space and any non-alphanumeric characters.
            if (char.upper() in ALPHABET) or (char in NUMBERS):
                if make_upper:
                    new_text += char.upper()
                else:
                    new_text += char
        # end for
        self.ciphertext = new_text
        # end if
        return
        # end method
    
    def _block_output(self):
        """Internal method that outputs encrypted text in five-
        character blocks, and can also insert newlines to keep long
        strings of blocks from running off the screen. if the user
        wishes.
        
        Called by the encrypt method.
        
        Arguments:  none.
        
        Returns:  nothing.
        """
        # Clear the screen.
        i_o.clear_screen()
        # Ask whether to break the output into 5-character blocks.
        separate = i_o.yes_no(
                "Would you like the encrypted text to be printed in" +
                "five\n-character blocks for immproved readability?")
        line_break = i_o.yes_no(
                "Would you like the output to be broken into separate" +
                'lines?\n(Warning:  This will insert line breaks or") +
                '"hard returns"\ninto the output.)')
        new_text = ""
        if separate:
            index = 0
            # Iterate over the ciphertext, five characters at a time.
            for pos in range(0, len(self.ciphertext), 5):
                # Add a five-character block, plus a space.
                new_text += self.ciphertext[pos:pos+5] + " "
                index += 1
                if index == 10:
                    index = 0
                # end if
            # end for
            # Put result in ciphertext.
            self.ciphertext = new_text
        # end if
        # Ignore if the ciphertext is too short to break into multiple
        #  lines.
        # Set line length.
        pos = 60
        if line_break and (len(self.ciphertext) > pos):
            # Start with a new line.
            new_text = "\n"
            while pos < len(self.ciphertext):
                # Work backwards from the first character after the line
                #  length, looking for a space.
                offset = 0
                while (
                        (self.ciphertext[pos + offset] != " ") and
                        (pos + offset != 0)):
                    offset -= 1
                # end while
                if offset == 0:
                    # If offset landed on 0, the first character after
                    #  the line length is a space.  In that case, take
                    #  the line, insert a newline character, and discard
                    #  the space.
                    new_text += self.ciphertext[:pos] + "\n"
                    self.ciphertext = self.ciphertext[pos+1:]
                elif pos + offset == 0:
                    # If offset landed on the negative of pos, there
                    #  were no spaces within the line.  Just take the
                    #  entire line.
                    new_text += self.ciphertext[:pos] + "\n"
                    self.ciphertext = self.ciphertext[pos:]
                else:
                    # Otherwise, take the line up to and including the
                    #  space.
                    new_text += self.ciphertext[:pos + offset + 1] + "\n"
                    self.ciphertext = self.ciphertext[pos + offset + 1:]
                # end if
            # end while
            # When there is less than a full line left, take the entire
            #  line.
            new_text += self.ciphertext
            # Put result back in self.ciphertext.
            self.ciphertext = new_text
        # end if
        return
    # end method
    
    def _format_plaintext(self):
        """Internal method that formats a plaintext string for
        encryption.
        
        NOTE that if _intelligent_encrypt has been run on the plaintext,
        this method will change nothing.
        
        Arguments:  none.
        
        Returns:  nothing.
        """
        new_string = ""
        # Iterate through plaintext.
        for char in self.plaintext:
            # Keep a character only if it is a letter or a number.
            #  Discard everything else.
            if (char.upper() in ALPHABET) or (char in NUMBERS):
                new_string += char.upper()
            # end if
        # end for
        # Put the result in plaintext.
        self.plaintext = new_string
        return
    # end method
    
    def _get_keynumber(self, prompt, keylist=None, lbound=None, ubound=None):
        """Gets a keynumber for a cipher from the unser allows the user
        to abort.
        
        Arguments:
        - prompt -- prompt for the user.
        
        Named arguments:
        - keylist -- a list of valid entries (default None).
        - lbound -- lower bound for number, inclusive (default None).
        - ubound -- upper bound for number, inlcusive (default None).
        
        Returns:  the keynumber, or None if the user aborts.
        """
        keynumber = None
        got_keynumber = False
        # Loop until a valid key is obtained, or user aborts.
        while not got_keynumber:
            # Get a string response.
            string = i_o.get_string(prompt)
            # If the user didn't enter anything...
            if len(string) == 0:
                # Ask whether to abort.
                abort = i_o.yes_no(
                    "You did not enter anything.  Do you want to abort?")
                if abort:
                    # If yes, drop out of the while loop with key =
                    #  None.
                    break
            else:
                # Test the response for validity.
                got_keynumber = True
                # First, see if it's a number.
                try:
                    keynumber = int(string)
                except ValueError:
                    # Loop back if it's not.
                    print("Sorry, that was not a number.")
                    got_keynumber = False
                    continue
                # end try
                # Check the number against the keylist (but only if
                #  keylist exists).
                if keylist and (keynumber not in keylist):
                    # Loop if there's a keylist and the number isn't in
                    #  it.
                    print("Sorry, that is not a valid keynumber for this",
                          "cipher.")
                    got_keynumber = False
                # Check against upper and lower bounds, if they exist.
                elif lbound and (keynumber < lbound):
                    print("Sorry, that number is too small.")
                    got_keynumber = False
                elif ubound and (keynumber > ubound):
                    print("Sorry, that number is too large.")
                    got_keynumber = False
                # end if
            # end if
        # end while
        return keynumber
    # end method
    
    def _get_keyword(
        self, prompt, keylist=ALPHABET, max_length=None, min_length=None):
        """Gets a keyword for a cipher from the user, allows the user to
        abort.
        
        The primary difference between _get_keyword and an ordinary 
        input method like get_string is that _get_keyword ensures 
        that no non-alphabetic characters are in the keyword (spaces
        are stripped) and that the keyword is returned in upper-case.        
        
        Arguments:
        - prompt -- prompt for the user (allows keywords to be named).
        
        Named Arguments:
        - keylist -- allows the caller to pass a non-standard alphabet
            against which to check the user's input (default ALPHABET).
        - max_length -- allows the caller to control the maximum length
            of the keyword (default None).
        - min_length -- allows the caller to control the minimum length
            of the keyword (default None).
        
        Returns:  the keyword, or an empty string if the user aborts.
        """
        keyword = ""
        got_keyword = False
        # Loop until a valid keyword is obtained, or user aborts.
        while not got_keyword:
            # Get string response.
            keyword = i_o.get_string(prompt)
            # If the user didn't enter a keyword...
            if len(keyword) == 0:
                # Ask whether to abort.
                abort = i_o.yes_no(
                    "You did not enter anything.  Do you want to abort?")
                if abort:
                    # If user aborts, drop out of the while loop with
                    #  keyword = "", which will be returned.
                    break
                # end if
            # end if
            if min_length and (len(keyword) < min_length):
                # If too short, say so and loop back to beginning.
                print(
                    "Sorry, your entry is too short.")
                continue
            # end if
            if max_length and (len(keyword) > max_length):
                # If too long, say so and loop back to beginning.
                print("Sorry, your entry is too long.")
                continue
            # end if
            # If it's the right length, check for invalid characters.
            got_keyword = True
            for letter in keyword:
                # Check each character to make sure it's a letter.
                if not (letter.upper() in keylist):
                    print(
                        "Sorry, your entry includes spaces or" +
                        "other forbidden characters.")
                    got_keyword = False
                    # Break the for loop (not the while loop).
                    break
                # end if
            # end for
        # end while
        return keyword.upper()
    # end method
    
    def _intelligent_decrypt(self):
        """Internal method that decodes flags in encrypted text.
        
        Arguments:  none.
        
        Returns:  nothing.        
        """
        # First check to see if Intelligent Decryption needs to be used;
        #  if not, do nothing.  The first two characters of an
        #  intelligently encrypted text will always be "ZX".
        if self.plaintext[0 : 2] != "ZX":
            return
        else:
            # Parse plaintext for special sequences.
            new_text = ""
            pos = 2
            # Go through the text one two-character slice at a time,
            #  looking for special sequences.
            while pos < (len(self.plaintext) - 1):
                # Grab a two-character slice.
                text_slice = self.plaintext[pos:pos + 2]
                # Test against special sequences
                if text_slice in INTEL_DICT:
                    # Find out which one.
                    # If it's the end of the message...
                    if INTEL_DICT[text_slice] == "EOM":
                        # The message has ended; break the loop.
                        break
                    # If it's for a capital letter...
                    elif INTEL_DICT[text_slice] == "CAP":
                        # Just add the next character (it's already
                        #  upper-case).
                        new_text += self.plaintext[pos+2:pos + 3]
                        # Discard the special sequence and the capital
                        #  letter.
                        pos += 3
                    else:
                        # Any special sequence that isn't the end of the
                        #  message or an upper-case inidicator is a
                        #  space or punctuation mark; just add the
                        #  appropriate character from INTEL_DICT.
                        new_text += INTEL_DICT[text_slice]
                        # Discard the special sequence.
                        pos += 2
                    # end if
                # Anything not an special sequence is an ordinary
                #  character.
                else:
                    # Add the lower-case version of the character.
                    new_text += text_slice[0].lower()
                    # Discard the character.
                    pos += 1
                # end if
            # end while
            # end if
            # Put the result in plaintext.
            self.plaintext = new_text
        # end if
        return
    # end method
    
    def _intelligent_encrypt(self):
        """Internal method that inserts flags for decryption.
        
        If the user opts for intelligent encryption, this method will
        insert special sequences for spaces, capital letters, basic
        punctuation (and itself), using bigrams (2-letter combinations)
        that rarely occur in English.
        
        Arguments:  none.
        
        Returns:  nothing.
        """
        # Clear the screen first.
        i_o.clear_screen()
        # Print summary info.
        print("Cipher: ", self.__str__())
        print("Action: ", self.mode, "\n")
        # Print explanation of intelligent encryption.
        print(
            "Intelligent Encryption/Decryption:  Under ordinary\n",
            "circumstances, when a message is encrypted it is turned into\n",
            "a single string of upper-case text, with all spacing,\n",
            "punctuation and capitalization removed.  Secret Messages!\n",
            "can encrypt your message so that flags are inserted to\n",
            "indicate spacing, punctuation and capitalization, which can\n",
            "then be restored upon decryption.\n")
        print(
            "Note that Intelligent Encryption/Decryption uses the\n",
            "following letter combinations, which do not occur in\n",
            "most Roman-alphabet-based languages:  [FQ], [GX], [HX],\n",
            "[JQ], [JX], [PZ], [QG], [QK], [QY], [QZ], [WQ], [WZ], [XJ],\n",
            "[ZJ], [ZQ], [ZX].  If your messages contains abbreviations,\n",
            "code words, model numbers, map coordinates, etc., which may\n",
            "contain these letter combinations, you should NOT select\n",
            "Intelligent Encryption/Decryption.\n")
        # Get the user's choice.
        use_intel = i_o.yes_no("Use Intelligent Encryption?")
        if not use_intel:
            # If no, just exit.
            return
        else:
            # If yes, The first two characters of the decrypted text
            # will be "ZX", which will trigger _intelligent_decrypt when
            # it is called.
            space_sequences = ["FQ", "JX", "QK", "WZ", "ZJ"]
            new_text = "ZX"
            # Go through the message one character at a time.
            for char in self.plaintext:
                # Check for space.
                if char == " ":
                    # Because spaces are so common, encoding them with a
                    #  single escape sequence could expose the sequence
                    #  to detection, thereby exposing the lengths of
                    #  individiual words.  To counter this, the method
                    #  randomly selects one of five special sequences,
                    #  any of which can mark a space.
                    new_text += space_sequences[random.randint(0, 4)]
                # First a series of tests for punctuation marks.  Each
                #  of these inserts a two-character sequence in place of
                #  the character.
                elif char == ".":
                    new_text += "HX"
                elif char == ",":
                    new_text += "JQ"
                elif char == "?":
                    new_text += "PZ"
                elif char == "!":
                    new_text += "QG"
                elif char == "'":
                    new_text += "QY"
                elif char == '"':
                    new_text += "QZ"
                elif char == ":":
                    new_text += "WQ"
                elif char == ";":
                    new_text += "XJ"
                elif char == "-":
                    new_text += "ZQ"
                # If it's not punctuation, check for a capital letter.
                elif char in ALPHABET:
                    new_text += "GX" + char
                else:
                    # If all else fails, it's just an ordinary letter/
                    #  number.
                    new_text += char.upper()
                # end if
            # end for
            # The message also ends with "ZX".  Any characters added
            #  by the encryption method are nulls and should be
            #  discarded by _intelligent_decrpyt.
            new_text += "ZX"
            self.plaintext = new_text
        # end if
        return
    # end method
    
    def _one_time_pad(self):
        """Internal method that implements a one-time pad at the
        user's option.
        
        Called by both encrypt and decrypt methods.
        
        Arguments:  none.
        
        Returns:  nothing.
        """
        # Clear the screen.
        i_o.clear_screen()
        # Print summary info.
        print("Cipher: ", self.__str__())
        print("Action: ", self.mode, "\n")
        # Print explanation of the one-time pad.
        if self.mode == "Encrypt":
            print(
                "One-Time Pad:  In addition to encrypting your message\n",
                "using the " + self.__str__() + ", Secret Messages! can\n",
                "first encode your message using a one-time pad.  This\n",
                "scrambles your message before it is encrypted.  WARNING--\n",
                "if you use a one-time pad code, your message will be\n",
                "unrecoverable without entering the same code while\n",
                "decrypting.  To be theoretically unbreakable, the one-time\n",
                "pad code must equal or exceed the length of your message,\n",
                "but a code of any length may be used.")
        else:
            print(
                "One-Time Pad:  If this message was encrypted using a\n",
                "one-time pad code, you MUST enter the same code now in\n",
                "order to decrypt the message.")
        # If user chooses to use a one-time pad...
        if i_o.yes_no("Do you want to use a one-time pad on this cipher?"):
            done = False
            # Loop until a code is obtained, or user aborts.
            while done is False:
                # Get the one-time pad code from the user.
                pad_code = self._get_keyword("Enter a one-time code now:  ")
                if pad_code == "":
                    if i_o.yes_no(
                            "Do you want to " + self.mode.lower() + "this " +
                            "message without a one-time pad code?"):
                        # If no one-time pad code, do nothing.
                        return
                    # end if (method exits)
                else:
                    done = True
                # end if
            # end while
            # Work pad magic here.  Simple modular addition/subtraction
            #  is used.
            alphanum = ALPHABET + NUMBERS
            # Convert the pad code to a list of numbers.
            pad_code_list = []
            for letter in pad_code:
                pad_code_list.append(alphanum.index(letter.upper()))
            # end for
            new_string = ""
            if self.mode == "Encrypt":
                mod = 1
            else:
                mod = -1
            # end if
            # This method operates on both letters and numbers.
            # Loop through the text, performing addition or subtraction
            #  on each letter, using each number in the pad code in
            #  succession.  Note that if the one-time pad code is
            #  shorter than the message, the code repeats.
            index = 0
            for letter in self.plaintext:
                # Substitute recoded letter for original letter.
                new_string += (
                    alphanum[(alphanum.index(letter) +
                              (pad_code_list[index] * mod)) % 36])
                # Next number in code sequence; reset if at end.
                index = (index + 1) % len(pad_code_list)
            # end for
            # Put the results back into the plaintext attribute.
            self.plaintext = new_string
        # end if
        return
    # end method
