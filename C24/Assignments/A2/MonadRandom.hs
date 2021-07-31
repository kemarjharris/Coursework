module MonadRandom where

import Control.Applicative (liftA2)

import Data.Ratio ((%))

import MonadRandomDef

import Data.List

instance Functor DecisionTree where
    -- If you are confident in your Monad instance, you may use:
    -- fmap f t = t >>= \x -> return (f x)
    fmap f (Tip a) = Tip(f a)
    fmap f (Choose rat l r) = Choose rat (fmap f l) (fmap f r)

instance Applicative DecisionTree where
    -- If you are confident in your Monad instance, you may use:
    -- liftA2 op t1 t2 = t1 >>= \x1 -> t2 >>= \x2 -> return (op x1 x2)
    pure a = Tip a
    liftA2 op t@(Tip a) u@(Tip b) = Tip (op a b)
    liftA2 op t@(Tip a) u@(Choose uRat ul ur) = Choose uRat (liftA2 op t ul) (liftA2 op t ur)
    liftA2 op (Choose tRat tl tr) u@(Choose uRat ul ur) = Choose tRat (liftA2 op tl u) (liftA2 op tr u)

instance Monad DecisionTree where
    return a = Tip a
    Tip a >>= f = f a
    t@(Choose rat l r) >>= f = Choose rat (l >>= f) (r >>= f)

instance MonadRandom DecisionTree where
    choose rat l r = Choose rat l r 

expectedValue :: Fractional q => (t -> q) -> DecisionTree t -> q
expectedValue f t = expectedValueHelper f t 0 1

expectedValueHelper :: Fractional q => (t -> q) -> DecisionTree t -> q -> q -> q
expectedValueHelper f t@(Tip a) value probability = value + (probability * f a)
expectedValueHelper f t@(Choose rational l r) value probability = final
    where
        lVal = expectedValueHelper f l value (probability*(fromRational rational))
        final = expectedValueHelper f r lVal (probability*fromRational (1-rational))

probability :: Fractional q => (t -> Bool) -> DecisionTree t -> q
probability pred t = expectedValue bernoulli t
  where
    bernoulli a | pred a = 1
                | otherwise = 0

uniform :: MonadRandom m => [a] -> m a
uniform (x:[]) = return x
uniform xt = choose (toInteger (lLen) % toInteger (len)) (uniform lHalf) (uniform rHalf)
    where
        len = length xt
        split = splitAt ((len + 1) `div` 2) xt
        lHalf = fst split
        rHalf = snd split
        lLen = length lHalf

hangman :: MonadRandom m => String -> Int -> String -> m WinLose
hangman word k letters = hangmanHelper word k (uniform (permutations letters))

hangmanHelper :: MonadRandom m => String -> Int -> m String -> m WinLose
hangmanHelper word k tree = fmap (strMatch (word) k) tree

-- word k letters
strMatch :: String -> Int -> String -> WinLose
strMatch "" _ _ = Win
strMatch _ 0 _ = Lose
strMatch _ _ "" = Lose
strMatch word k letters@(l:rest) = strMatch (filter (/=l) word) (k-1) (rest)