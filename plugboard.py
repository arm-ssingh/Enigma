class PlugLead:
    """
    mapping the lead connection to the plugboard
    @todo: shall we use one base for plugboard and input to rotor ?
    """
    def __init__(self, mapping):
        # Your code here
        self.plugBase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.plugMapping = {}
        for m in self.plugBase:
            self.plugMapping[m] = m
        # storing the key
        self.plugkey = mapping
        # adding the mapping
        self.addMapping()

    def addMapping(self):
        if (len(self.plugkey) > 1):
            self.plugMapping[self.plugkey[0]] = self.plugkey[1]
            self.plugMapping[self.plugkey[1]] = self.plugkey[0]

    def encode(self, character):
        # Your code here
        return self.plugMapping[character]


class Plugboard:
    # Your code here
    """
    making the plugboard connection
    """
    def __init__(self):
        self.plugBoardMappling = {}
        #@todo: can make it configurable
        self.connectionCount = 0
        self.maxConnection = 11

    def add(self, plugLeadObj):
        """checking for the max 10 connections but keeping it configurable"""
        self.connectionCount +=1
        if self.connectionCount == self.maxConnection:
            raise Exception(f'You cannot have more than allowed plug leads')
        if plugLeadObj.plugkey[0] not in self.plugBoardMappling and plugLeadObj.plugkey[1] not in self.plugBoardMappling:
            self.plugBoardMappling[plugLeadObj.plugkey[0]] = plugLeadObj
            self.plugBoardMappling[plugLeadObj.plugkey[1]] = plugLeadObj
        else:
            raise ValueError("Plugs are already in Use")

    def encode(self, char):
        if char in self.plugBoardMappling:
            self.plugLeadOb = self.plugBoardMappling[char]
            return self.plugLeadOb.encode(char)
        else:
            return char

