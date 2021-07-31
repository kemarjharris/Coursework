"""
Encrypt or decrypt the contents of a message file using a deck of cards.
"""

import cipher_functions

DECK_FILENAME = 'deck1.txt'
MSG_FILENAME = 'message-decrypted.txt'
MODE = 'e'  # 'e' for encryption, 'd' for decryption.


def main():
    """ () -> NoneType

    Perform the encryption using the deck from a file called DECK_FILENAME and
    the messages from a file called MSG_FILENAME. If MODE is 'e', encrypt;
    otherwise, decrypt. Print the decrypted message to the screen.
    """
    file = open(DECK_FILENAME, 'r')
    deck = file.readlines()
    file.close()
    file2 = open(MSG_FILENAME, 'r')
    messages = file2.readlines()
    file2.close()
    cypher_text = process_messages(file, messages, MODE):
        for e in cypher_text:
            print(e)

