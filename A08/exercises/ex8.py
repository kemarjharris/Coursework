class Light_Switch():
    '''a class that represents a switch'''
    def __init__(self, switch_val):
        if switch_val == 'on':
            self.switch_val = True
        elif switch_val == 'off':
            self.switch_val = False
        else:
            self.switch_val = False

    def __str__(self):
        if (self.switch_val is True):
            return 'I am on'
        else:
            return 'I am off'

    def turn_on(self):
        self.switch_val = True

    def turn_off(self):
        self.switch_val = False

    def flip(self):
        self.switch_val = not(self.switch_val)


class SwitchBoard():
    '''
    Data Dictionary:
    num_of_switches: number of switches on the switchboard
    on_switches: the switches in num_of_switches that are True
    e: the value in an elemental for loop.
    s_flipped: the switch that has been switched.

    '''
    # create a switchboard w a cetain number
    def __init__(self, num_of_switches):
        self.num_of_switches = [None]*num_of_switches
    # set all the switches to off
        for i in range(len(self.num_of_switches)):
            self.num_of_switches[i] = False

    # print the switches that are on
    def __str__(self):
        switches_that_are_on = ''
        for i in range(len(self.num_of_switches)):
            if (self.num_of_switches[i] is True):
                switches_that_are_on += str(i) + ' '
        return 'The on switches are: ' + switches_that_are_on

    # get the switches that are on
    def which_switch(self):
        on_switches = []
        for i in range(len(self.num_of_switches)):
            if (self.num_of_switches[i] is True):
                on_switches += [i]
        return on_switches

    # flip a specific switch
    def flip(self, s_flip):
        if (s_flip < len(self.num_of_switches)):
            self.num_of_switches[s_flip] = not(self.num_of_switches[s_flip])

    # flip the nth switch
    def flip_every(self, n):
        for i in range(0, len(self.num_of_switches), n):
            self.num_of_switches[i] = not(self.num_of_switches[i])

    # reset method that sets everything back to off
    def reset(self):
        for i in range(len(self.num_of_switches)):
            self.num_of_switches[i] = False

'''if (__name__ == '__main__'):
    a = SwitchBoard(1023)
    n = 0
    while (n < 0):
        a.flip_every(n)
        n += 1'''
