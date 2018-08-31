# treehouse-python-project-2
Project #2 for the Treehouse Python Techdegree.

This is the project for Unit 2, Secret Messages!  It implements all of the ciphers listed, implements five-character blocks and one-time pads as user options (except for the Polybius Square Cipher, which outputs a series of two-digit numbers).  The program can, if the user wishes, encrypt and decrypt spaces, capital letters, and common punctuation.  The following test string is included for that feature:


This is a test-string for Secret Messages!  "It includes every punctation mark, and symbol, that can be encoded by the Intelligent Encryption and Decryption rountines?" The main symbols that aren't readable are: the slash and the underscore; these could be included in future versions.


Each cipher is its own subclass of the parent class Cipher, and inherits methods from Cipher (though a couple of ciphers override parent methods when necessary).  Note that the Caesar Cipher is also included, but is a different implementation from the sample file.

All modules have been checked by the pep8 tool (via Spyder) and are Pep 8 compliant except for W293 warnings.
