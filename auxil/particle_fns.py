

'''
Aux particle functions
'''

def dE(self,index=1):
    return self.sp[index].E/self.sp[index].E[0] - 1

def dPtor(self,index=1):
    return self.sp[index].Ptor/self.sp[index].Ptor - 1

