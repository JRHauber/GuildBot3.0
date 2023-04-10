class Ship:
    def __init__ (self, type, id, health, shields, attacks, dice, defences):
        
        self.type = type
        self.id = id
        self.health = health
        self.maxhealth = health
        self.shields = shields
        self.maxshields = shields
        self.attacks = attacks
        self.dice = dice
        self.defences = defences
        
    def __str__(self):
        
        return f"{self.type} - {self.id} ({self.health}/{self.maxhealth})"

    
defaults = {
    "Harrower" : [['turbolaser', 'laser', 'ion', 'torpedo', 'missile'], ['10d40', '4d40', '1d40', '6d30', '6d40'], 60, 10, 10],
    "Centurion" : [['turbolaser', 'laser', 'ion'], ['6d40', '6d30', '6d40'], 50, 8, 8],
    "Terminus" : [['turbolaser', 'laser', 'ion', 'missile'], ['6d40', '8d30', '1d40', '3d40'], 50, 8, 6],
    "Bulk" : [['turbolaser'], ['5d40'], 40, 6, 6],
    "Gage" : [['turbolaser', 'ramming'], ['5d40', '1d100'], 40, 4, 6],
    "Derriphan" : [['autoblaster', 'laser', 'missile'], ['6d40', '4d30', '3d40'], 40, 8, 0],
    "Interdictor" : [['turbolaser', 'laser'], ['5d40', '6d30'], 40, 4, 6],
    "Phantom" : [['laser', 'missile', 'torpedo'], ['4d30', '1d30', '1d30'], 30, 2, 2],
    "Fury" : [['laser', 'missile', 'torpedo'], ['4d30', '1d30', '1d30'], 30, 4, 2],
    "Decimus" : [['laser', 'missile', 'torpedo'], ['2d20', '1d30', '1d30'], 25, 2, 3],
    "Onslaught" : [['laser', 'mlaser', 'missile'], ['2d20', '2d40', '1d30'], 25, 4, 1],
    "Extinction" : [['laser', 'torpedo'], ['2d20', '1d30'], 25, 3, 2],
    "Mangler" : [['laser', 'missile', 'railgun'], ['4d20', '1d30', '10d20'], 25, 2, 1],
    "Dustmaker" : [['laser', 'missile'], ['2d20', '1d30'], 25, 2, 1],
    "Supremacy" : [['laser'], ['4d20'], 20, 2, 0],
    "Blackbolt" : [['laser', 'missile'], ['2d20', '1d30'], 20, 2, 0],
    "Quell" : [['laser', 'missile'], ['2d20', '1d30'], 20, 1, 1],
    "Rycer" : [['llaser', 'laser'], ['2d20', '2d20'], 20, 1, 1],
    "Mailoc" : [['laser', 'railgun'], ['2d20', '5d20'], 20, 1, 1]
}