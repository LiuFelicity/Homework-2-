# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

> Solution

> profitable path: tokenB->tokenA->tokenC->tokenE->tokenD->tokenC->tokenB, tokenB balance=22.497222
amountIn: 5, tokenB->tokenA, amountOut: 5.655321988655322
amountIn: 5.655321988655322, tokenA->tokenC, amountOut: 2.372138936383089
amountIn: 2.372138936383089, tokenC->tokenE, amountOut: 1.5301371369636168
amountIn: 1.5301371369636168, tokenE->tokenD, amountOut: 3.450741448619708
amountIn: 3.450741448619708, tokenD->tokenC, amountOut: 6.684525579572586
amountIn: 6.684525579572586, tokenC->tokenB, amountOut: 22.49722180697414


## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

> Solution

> * slippage is the difference between the expected price and the actual price of a trade.
> * Uniswap V2 使用 UniswapV2Router01::swapExactTokensForTokens, 在第二個參數 "amountout_min" 是表示如果獲利少於"amountout_min"就不執行swap
```solidity=
router.swapExactTokensForTokens(
    5 ether
    , 20 ether // when amountout < 20, don't do the swap and this is how Uniswap V2 address this issue
    , path
    , arbitrager
    , block.timestamp
);
```

## Problem 3
Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

> Solution
> 如果不設置此 aminium liquidity，首位使用者就可以利用少量資金控制流動池，因此採取此機制來避免此情況發生。

## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

> Solution
> * 公式：liquidity = min(amount0/reserve0, amount1/reserve1)*totalsupply
> * 這個公式讓使用者會得到比例比較差那個(amount0 / reserve0 or amount1 / reserve1)。這會使他們盡量平衡token1和token2的比例。避免使用者利用比例大幅不同而進行不合理的套利。

## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap?

> Solution
> 三明治攻擊是一種在DEX上操縱價格的攻擊方式。攻擊者會在交易者提交交易前後快速的進行大量交易，利用提供更高的Gas fee來加快處理速度。導致交易者在交易時價格發生不利變動。使得交易者在完成交易時得到不利價格，從而損失更多的資產。
