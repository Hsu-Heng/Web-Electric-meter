
# coding=UTF-8
class Meter:
    def __init__(self, Capaturetime, VLN_A, VLN_B, VLN_C, I_A, I_B, I_C, KW_A, KW_B, KW_C, KVAR_A, KVAR_B, KVAR_C, KWH, KVARH):
        self.Capaturetime = Capaturetime
        self.VLN_A = VLN_A
        self.VLN_B = VLN_B
        self.VLN_C = VLN_C
        self.I_A = I_A
        self.I_B = I_B
        self.I_C = I_C
        self.KW_A = KW_A
        self.KW_B = KW_B
        self.KW_C = KW_C
        self.KVAR_A = KVAR_A
        self.KVAR_B = KVAR_B
        self.KVAR_C = KVAR_C
        self.KWH = KWH
        self.KVARH = KVARH

    def Meterdict(self):
        returnstr = {}
        returnstr['Capaturetime'] = self.Capaturetime
        returnstr['VLN_A'] = self.VLN_A
        returnstr['VLN_B'] = self.VLN_B
        returnstr['VLN_C'] = self.VLN_C
        returnstr['I_A'] = self.I_A
        returnstr['I_B'] = self.I_B
        returnstr['I_C'] = self.I_C
        returnstr['KW_A'] = self.KW_A
        returnstr['KW_B'] = self.KW_B
        returnstr['KW_C'] = self.KW_C
        returnstr['KVAR_A'] = self.KVAR_A
        returnstr['KVAR_B'] = self.KVAR_B
        returnstr['KVAR_C'] = self.KVAR_C
        returnstr['KWH'] = self.KWH
        returnstr['KVARH'] = self.KVARH
        return returnstr
