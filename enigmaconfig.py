class EnigmaConfig:
    """
    setting the Enigma configuration based on the user input.
    @todo: make it configurable
    @todo: give user the options
    """
    configValid = False

    def __init__(self, reflector, rotors,ring_setting, rotor_position,plugsCon):
        self.ring_settings = ring_setting
        self.reflector = reflector
        self.rotors = rotors
        self.rotors_pos = rotor_position
        self.plugsCon = plugsCon
    @staticmethod
    def check_reflector_valid(value):
        valid_values = ['A', 'B', 'C']
        is_valid = value in valid_values
        if not is_valid:
            print(f'Please enter one of the following {valid_values}')
        return is_valid
    @staticmethod
    def is_plug_lead_mappings_valid(value):
        return len(value) <= 10
    @staticmethod
    def is_rotor_arg_value_valid(value):
        #print(value)
        val_len = len(value)
        if val_len != 3 and val_len != 4:
            print('Please enter 3 or 4 values')
            return False

        valid_values = ['I', 'II', 'III', 'IV', 'V', 'Beta', 'Gamma']
        for i in value:
            if not i in valid_values:
                print(f'Please enter one of the following {valid_values}')
                return False
        return True

    @classmethod
    def from_user_input_settings(cls, input_string):
        """Set the Enigma from user input string.
         for e.g string with "B I-II-III 01-01-01 A-A-Z HL-MO-AJ-CX-BZ-SR-NI-YW-DG-PK" will be interpreted as
         enigma machine with rotors I II III, reflector B, ring settings 01 01 01, and initial positions A A Z.
         The plugboard should map the following pairs: HL MO AJ CX BZ SR NI YW DG PK.
         The result of encoding the string HELLOWORLD should be RFKTMBXVVW.
        """

        config_inputs = input_string.split()
        reflector = config_inputs[0]
        cls.configValid = cls.check_reflector_valid(reflector)
        if len(config_inputs) > 4:
            plugboard = config_inputs[4].replace('-', ' ').split()
            cls.configValid = cls.is_plug_lead_mappings_valid(plugboard)
        else:
            plugboard = [] # no plugboard conenction made
            cls.configValid = True
        rotorList_from_user = []
        rotorPostition_from_user = []
        config_ring_settings = []
        for rotor_id, rotor_ring_setting, rotor_start_position in zip(config_inputs[1].split('-')[::-1],
                                                             config_inputs[2].split('-')[::-1],
                                                             config_inputs[3].split('-')[::-1]):
            rotorList_from_user.append(rotor_id)
            rotorPostition_from_user.append(rotor_start_position)
            config_ring_settings.append(int(rotor_ring_setting))
        cls.configValid = cls.is_rotor_arg_value_valid(rotorList_from_user)
        if not cls.configValid:
            raise Exception(f'Your configuration is incorrect')
        return cls(reflector, rotorList_from_user, config_ring_settings, rotorPostition_from_user,  plugboard)

    def is_valid_setup(self):
        """Confirm if config is valid"""
        return self.configValid
