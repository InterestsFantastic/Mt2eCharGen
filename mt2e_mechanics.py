from roller import roll

def roll_normal():
    return roll('2d6')

def roll_boon():
    return roll('3d6kh2')

def roll_bane():
    return roll('3d6kl2')
