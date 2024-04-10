liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}
uesed = {
    ("tokenA", "tokenB"): False,
    ("tokenA", "tokenC"): False,
    ("tokenA", "tokenD"): False,
    ("tokenA", "tokenE"): False,
    ("tokenB", "tokenC"): False,
    ("tokenB", "tokenD"): False,
    ("tokenB", "tokenE"): False,
    ("tokenC", "tokenD"): False,
    ("tokenC", "tokenE"): False,
    ("tokenD", "tokenE"): False,
}
def getUsed(tokenFrom, tokenTo):
    global uesed
    if (tokenFrom, tokenTo) in uesed:
        #print(tokenFrom, tokenTo, uesed[(tokenFrom, tokenTo)])
        return uesed[(tokenFrom, tokenTo)]
    elif (tokenTo, tokenFrom) in uesed:
        #print(tokenTo, tokenFrom, uesed[(tokenTo, tokenFrom)])
        return uesed[(tokenTo, tokenFrom)]
    else:
        raise Exception(f"getUsed: from {tokenFrom} to {tokenTo} Not found")
        
def setUsed(tokenFrom, tokenTo, use):
    global uesed
    if (tokenFrom, tokenTo) in uesed:
        uesed[(tokenFrom, tokenTo)] = use
    elif (tokenTo, tokenFrom) in uesed:
        uesed[(tokenTo, tokenFrom)] = use
    #print(uesed)
    


def findRate(tokenFrom, tokenTo):
    if (tokenFrom, tokenTo) in liquidity:
        return liquidity[(tokenFrom, tokenTo)]
    elif (tokenTo, tokenFrom) in liquidity:
        return liquidity[(tokenTo, tokenFrom)][::-1]  # reverse
    else:
        raise Exception(f"findRate: from {tokenFrom} to {tokenTo} Not found")

# print(findRate("tokenA", "tokenB"))
# print(findRate("tokenB", "tokenA"))
#assert(False)

# 997*(997*(997*5*17)/(1000*10+997*5)*9) / (1000*15+997*(997*5*17)/(1000*10+997*5))*13)/(1000*6+997*(997*(997*5*17)/(1000*10+997*5)*9)/(1000*15+997*(997*5*17)/(1000*10+997*5))) = 3.7707
# dY = (997 * dX * Y)/(1000 * X + 997 * dX)
def getAmountOut(tokenFrom, tokenTo, dX ):
    X, Y = findRate(tokenFrom, tokenTo)
    #print(f"{X}, {Y}")
    return  (997 * dX *Y)/ (1000*X+997*dX)

'''
dy = getAmountOut("tokenB", "tokenA", 5)
print(dy)
dy = getAmountOut("tokenA", "tokenD", dy)
print(dy)
dy = getAmountOut("tokenD", "tokenB", dy)
print(dy)
'''


tokens = ("tokenA", "tokenB", "tokenC", "tokenD", "tokenE")


# Golbal var for FBP(findBestPath())
__FBP_BALANCE__ = 0 
__FBP_PATH__= []
def findBestPath(tokenFrom, balance, dep=1, startToken=None, startBalance=0): # dfs
    global __FBP_BALANCE__, __FBP_PATH__, uesed
    if dep == 1: 
        startToken = tokenFrom
        startBalance = balance
        #__FBP_BALANCE__ = 0 
        #__FBP_PATH__= []
        

    if balance <= 0 : return False

    if dep > 1 and tokenFrom == startToken:
        if balance > __FBP_BALANCE__:
            #print(dep, balance)
            __FBP_BALANCE__ = balance
            __FBP_PATH__ = [tokenFrom]
            #print(f"dep = {dep} {tokenFrom} balance={balance}")
            return True
    
    ret = False
    for tokenTo in tokens:
        if tokenFrom == tokenTo: continue
        if getUsed(tokenFrom, tokenTo): continue
        
        
        new_balance = getAmountOut(tokenFrom, tokenTo, balance)
        
        #print(f"-------{new_balance}")
        setUsed(tokenFrom, tokenTo, True)
        ret |= findBestPath(tokenTo, new_balance, dep+1, startToken, startBalance)
        setUsed(tokenFrom, tokenTo, False)

    if ret :
        #print(dep, ret, tokenFrom, __FBP_PATH__)
        #print(f"\tdep = {dep} {tokenFrom}")
        __FBP_PATH__.append(tokenFrom) 
        return True
    else:
        return False






def arbitrage (token, s_bal, e_bal):
    
    global __FBP_BALANCE__, __FBP_PATH__ 
    preDY = -1
    dY = s_bal
    ans = []
    
    end_balance, path = 0, None

    __FBP_BALANCE__, __FBP_PATH__ = 0, []
    if  findBestPath(token, dY): 
        end_balance, path = __FBP_BALANCE__, __FBP_PATH__

    if  end_balance > 0 : # found
        path = path[::-1] # reverse 
    
    #print(path)
    ans += path[:-1]
    
    for i in range(len(path)-1):
        #print(dY, end=" -> ")
        dY = getAmountOut(path[i], path[i+1], dY)
    #print(dY)
    
    
        
            

    # Output
    #print(f"** Path len = {len(ans)}") 
    for t in ans:
        print(t, end="->")
    print(f"{token}, {token} balance={dY:0.6f}")

'''
__FBP_BALANCE__, __FBP_PATH__ = 0, []
findBestPath(tokenFrom="tokenB", balance=5, dep=1, startToken=None, startBalance=0, maxDep=20)
print(__FBP_BALANCE__, __FBP_PATH__)
raise Exception("debug stop!")
'''

# 23.395916598615553 ['tokenB', 'tokenC', 'tokenD', 'tokenA', 'tokenB', 'tokenC', 'tokenD', 'tokenA', 'tokenB', 'tokenC', 'tokenD', 'tokenA', 'tokenB', 'tokenC', 'tokenD', 'tokenB', 'tokenC', 'tokenD', 'tokenB']
# BEST balance=23.396004614099645
arbitrage("tokenB", 5, 20)
#arbitrage("tokenB", 5, 30, 2)

'''
dY = getAmountOut("tokenB", "tokenA", 5)
print(dY)
dY = getAmountOut("tokenA", "tokenC", dY)
print(dY)
dy = getAmountOut("tokenC", "tokenB", dy)
print(dy)
'''

'''
def test(token):
    print(token)
  
    for key in liquidity:
        if key[0] == token:
            val = liquidity[key]
            print(key[1], val[0]/val[1])
        elif key[1] == token:
            val = liquidity[key]
            print(key[0], val[1]/val[0])
    
test("tokenA")
test("tokenB")
test("tokenC")
test("tokenD")
'''
