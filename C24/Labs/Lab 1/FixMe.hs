module FixMe where

pow :: Integer -> Integer -> Integer
pow b e
    | e == 0 = 1
    | r == 0 = y2
    | r == 1 = y2 * b
    
  where
    (q, r) = divMod e 2
    y = pow b q
    y2 = y * y