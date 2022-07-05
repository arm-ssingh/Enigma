class Rotor:
    # making class variables to rotor type and notch settings which are fixed
    #@todo: make  notch position user configurable
    Rotor_Type = {
        'Base': "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        'Beta': "LEYJVCNIXWPBQMDRTAKZGFUHOS",
        'Gamma': "FSOKANUERHMBTIYCWLQPZXVGJD",
        'I': "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        'II': "AJDKSIRUXBLHWTMCQGZNPYFVOE",
        'III': "BDFHJLCPRTXVZNYEIWGAKMUSQO",
        'IV': "ESOVPZJAYQUIRHXLNFTGKDCMWB",
        'V': "VZBRGITYUPSDNHLXAWMJQOFECK",
        'A': "EJMZALYXVBWFCRQUONTSPIKHGD",
        'B': "YRUHQSLDPXNGOKMIEBFZCWVJAT",
        'C': "FVPJIAOYEDRZXWGCTKUQSBNMHL",
    }
    """
    fixing the notch position. 
    Based on the Enigma machine this notch setting may differ and hence
    """
    Rotor_Notch_Position = {
        'I': "Q",
        'II': "E",
        'III': "V",
        'IV': "J",
        'V': "Z"
    }

    def __init__(self, Rotor_ID, rotor_initial_position=0, left_side_rotor=None, right_side_rotor=None, ring_setting=0):
        if Rotor_ID in Rotor.Rotor_Type:
            self.Rotor_ID = Rotor_ID
            self.ring_setting = ring_setting
            self.left_side_rotor = left_side_rotor
            self.right_side_rotor = right_side_rotor
            self.rotor_position = rotor_initial_position - ring_setting
            self.right_pins = Rotor.Rotor_Type['Base']
            self.rotor_ring = Rotor.Rotor_Type['Base']
            self.left_contact = Rotor.Rotor_Type[Rotor_ID]
            if Rotor_ID in Rotor.Rotor_Notch_Position:
                self.notch = Rotor.Rotor_Notch_Position[Rotor_ID]
                if self.ring_setting > 0:
                    idx = self.right_pins.index(self.notch) - ring_setting
                    self.notch = self.right_pins[idx]
            else:
                self.notch = None
        else:
            raise ValueError("Rotor not from the list")

    def get_rotor_id(self):
        return self.Rotor_ID

    def is_notch_position(self):
        return self.right_pins[self.rotor_position] == self.notch

    def encodeL2R(self, char):
        """
        Rotor Internal encoding from Left to right
        """
        offset = self.rotor_position
        if self.left_side_rotor is not None:
            offset -= self.left_side_rotor.rotor_position % 26
        input_pin = (self.right_pins.index(char) + offset) % 26
        pin_index = self.left_contact.index(self.right_pins[input_pin])
        return self.right_pins[pin_index]

    def encodeR2L(self, char):
        """
        Rotor Internal encoding from right to left
        """
        offset = self.rotor_position
        if self.right_side_rotor is not None:
            offset -= self.right_side_rotor.rotor_position % 26
        input_pin = (self.right_pins.index(char) + offset) % 26
        return self.left_contact[input_pin]

    def rotor_set_right(self, right_side_rotor):
        self.right_side_rotor = right_side_rotor

    def rotate(self):
        """
        Rotor move by one position
        rotate left if reach notch
        """
        rotate_left = self.right_pins[self.rotor_position] == self.notch
        self.rotor_position += 1
        self.rotor_position %= 26
        return rotate_left

    def is_rotor_reflector(self):
        """
        check if rotar is reflector
        """
        if self.left_side_rotor is None:
            return True
        else:
            return False
        #return self.left_side_rotor is None

    def rotor_set_left(self, left_side_rotor):
        self.left_side_rotor = left_side_rotor

    def get_rotor_position(self):
        return self.rotor_position % 26

    def get_rotor_ring_setting(self):
        return self.ring_setting