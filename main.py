
from rotor import *
from plugboard import *
from enigmaconfig import *

class Enigma:
    """making the enigma main machine"""
    def __init__(self, config):
        """
        :param config: taking enigmaconfig object which has the engima config
        @todo: make sure config is value
        """
        self.config = config
        self.plugboard = Plugboard()
        for lead_setting in config.plugsCon:
            self.plugboard.add(PlugLead(lead_setting))

        self.rotor_ring = Rotor.Rotor_Type['Base']

        #rotors must be from the list I, II, III, IV, V, Beta, Gammma, have a list which append all the rotors which
        #are part of the Enigma machine
        self.rotors_list = []
        for rotor_type, rotor_pos, rotor_ring_setting in zip(config.rotors, config.rotors_pos, config.ring_settings):
            self.rotors_list.append(Rotor(rotor_type, rotor_initial_position=self.rotor_ring.index(rotor_pos),
                                     ring_setting=(rotor_ring_setting - 1)))
        # add reflector
        self.rotors_list.append(Rotor(config.reflector))
        for rotor_id in range(len(self.rotors_list)):
            first = rotor_id == 0
            last = rotor_id == len(self.rotors_list) - 1
            if not last:
                self.rotors_list[rotor_id].rotor_set_left(self.rotors_list[rotor_id + 1])
            if not first:
                self.rotors_list[rotor_id].rotor_set_right(self.rotors_list[rotor_id - 1])

    def rotate_rotors(self, n):
        """
        rotate the rightmost rotor each time before start encoding
        rotation of the other rorors depends on the notch
        :param n: step to rotate
        :return: None
        """
        for i in range(n):
            rotate_left_rotor = self.rotors_list[0].rotate()
            if rotate_left_rotor or self.rotors_list[1].is_notch_position():
                rotate_left_rotor = self.rotors_list[1].rotate()
                if rotate_left_rotor:
                    self.rotors_list[2].rotate()

    def encode_input_string(self, input_text):
        """
        :param input_text: taking the input text to be encoded
        also, starting the rotor rotation before encoding
        :return: return encoded char
        """
        encoded_string = ""
        for ch in input_text:
            self.rotate_rotors(1)
            encoded_string += str(self.encode_input_character(ch))
        return encoded_string


    def rotate_all_rotors(self):
        """Set rotor positions back to starting position"""
        for rotor_list,rotor_position in zip(self.rotors_list[:-1], self.config.rotors_pos):
            rotor_list.position = self.rotor_ring.index(rotor_position)

    def encode_input_character(self, char):
        """
        :param char: character to encode
        :return: encoided character
        """
        character = self.plugboard.encode(char)
        for rotor in self.rotors_list:
            character = rotor.encodeR2L(character)
        for rotor in reversed(self.rotors_list[0:-1]):
            character = rotor.encodeL2R(character)
        index = self.rotor_ring.index(character)
        first_rotor_position_diff = (self.rotors_list[0].get_rotor_position()) % 26
        character = self.rotor_ring[(index - first_rotor_position_diff) % 26]
        character = self.plugboard.encode(character)
        return character

    def print_config(self):
        return (self.config)

if __name__ == '__main__':

    #string = "B Beta-I-III 23-02-10 A-A-B VH-PT-ZG-BJ-EY-FS"
    #print(string)
    #enigmasetup = EnigmaConfig.from_user_input_settings(string)
    enigmasetup = EnigmaConfig.from_user_input_settings("C Beta-Gamma-V 04-02-14 M-J-M KI-XN-FL")
    print(enigmasetup.is_valid_setup())
    enigma = Enigma(enigmasetup)
    encodedString = enigma.encode_input_string("DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ")
    print(encodedString)

    configObj = enigma.print_config()
    print(configObj.check_reflector_valid('B'))
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
