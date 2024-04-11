# 跑一次 然後 loop

liquidity_orig = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25)
}
liquidity = {}


def reset_liquidity():
    global liquidity,liquidity_orig
    liquidity = {}
    for key in liquidity_orig:
        liquidity[key] = liquidity_orig[key]


def reset():
    reset_liquidity()

def getUsed(tokenFrom, tokenTo):
    global uesed
    if (tokenFrom, tokenTo) in uesed:
        return uesed[(tokenFrom, tokenTo)]
    else:
        uesed[(tokenFrom, tokenTo)] = False
        return False
        

    


def findRate(tokenFrom, tokenTo):
    if (tokenFrom, tokenTo) in liquidity:
        return liquidity[(tokenFrom, tokenTo)]
    elif (tokenTo, tokenFrom) in liquidity:
        return liquidity[(tokenTo, tokenFrom)][::-1]  # reverse
    else:
        raise Exception(f"findRate: from {tokenFrom} to {tokenTo} Not found")

def setRate(tokenFrom, tokenTo, dX, dY):
    if (tokenFrom, tokenTo) in liquidity:
        liquidity[(tokenFrom, tokenTo)] = (dX, dY)
    elif (tokenTo, tokenFrom) in liquidity:
        liquidity[(tokenTo, tokenFrom)] = (dY, dX)
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
    return  (997 * dX *Y)/ (1000*X+997*dX), X, Y

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
def findBestPath(tokenFrom, balance, dep=1, startToken=None, startBalance=0, maxdep=4): # dfs
    global __FBP_BALANCE__, __FBP_PATH__, uesed
    if dep == 1: 
        startToken = tokenFrom
        startBalance = balance
        
    if balance <= 0 or dep> maxdep : return False

    if dep > 1 and tokenFrom == startToken:
        if balance > __FBP_BALANCE__:
            #print(dep, balance)
            __FBP_BALANCE__ = balance
            __FBP_PATH__ = [tokenFrom]
            print(f"dep = {dep} {tokenFrom} balance={balance}")
            return True
    
    ret = False
    for tokenTo in tokens:
        if tokenFrom == tokenTo: continue
        
        new_balance, X, Y = getAmountOut(tokenFrom, tokenTo, balance)
        
        #print(f"-------{new_balance}")
        
        setRate(tokenFrom, tokenTo, balance, new_balance)
        ret |= findBestPath(tokenTo, new_balance, dep+1, startToken, startBalance, maxdep)
        setRate(tokenFrom, tokenTo, X, Y)
        

    if ret :
        #print(dep, ret, tokenFrom, __FBP_PATH__)
        #print(f"\tdep = {dep} {tokenFrom}")
        __FBP_PATH__.append(tokenFrom) 
        return True
    else:
        return False






def arbitrage (token, s_bal, maxdep):
    
    global __FBP_BALANCE__, __FBP_PATH__ 
    
    dY = s_bal
    ans = []
    
    end_balance, path = 0, None

    __FBP_BALANCE__, __FBP_PATH__ = 0, []
    
    if  findBestPath(tokenFrom=token, balance = dY, maxdep=maxdep): 
        end_balance, path = __FBP_BALANCE__, __FBP_PATH__

    if  end_balance > 0 : # found
        path = path[::-1] # reverse 

    print(path)
    ans += path[:-1]
    for i in range(len(path)-1):
        print(dY, end=" -> ")
        dY, _, _ = getAmountOut(path[i], path[i+1], dY)
    print(dY)
            
            

    # Output
    ans.append(token)
    print(f"** Path len = {len(ans)}") 
    balance = s_bal
    for i in range(len(ans)-1):
        tF = ans[i]
        tT = ans[i+1]
        print(tF, end="->")
        # 實際調整 liquidity
        new_balance, X, Y = getAmountOut(tF, tT, balance)
        setRate(tF, tT, balance, new_balance)
        balance = new_balance

    print(f"{token} balance={dY:0.6f}")

'''
__FBP_BALANCE__, __FBP_PATH__ = 0, []
findBestPath(tokenFrom="tokenB", balance=5, dep=1, startToken=None, startBalance=0, maxDep=20)
print(__FBP_BALANCE__, __FBP_PATH__)
raise Exception("debug stop!")
'''


reset()
arbitrage("tokenB", 5, 7)
preBalanec = __FBP_BALANCE__
'''
for i in range(10):
    print("-"*20)
    print(f"loop = {i+1}")

    print(f"arbitrage(\"tokenB\", {__FBP_BALANCE__}, 7)")
    #reset_used()
    arbitrage("tokenB", __FBP_BALANCE__, 7)

    if preBalanec > __FBP_BALANCE__:
        break

    preBalanec = __FBP_BALANCE__
'''

