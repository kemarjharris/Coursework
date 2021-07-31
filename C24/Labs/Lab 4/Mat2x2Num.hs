module Mat2x2Num where

import Mat2x2Def

instance Num a => Num (Mat a) where
    -- (+) :: Mat a -> Mat a -> Mat a
    -- matrix addition
    (+) MkMat a b c d MkMat w x y z = MkMat (a+w) (b+x) (c+y) (d+z)

    -- negate :: Mat a -> Mat a
    -- negate every element
    negate MkMat a b c d = MkMat (-a) (-b) (-c) (-d)

    -- No need to do (-), and not tested during marking, default implementation
    -- uses your (+) and negate.

    -- (*) :: Mat a -> Mat a -> Mat a
    -- matrix multiplication

    (*) MkMat a b c d MkMat w x y z = MkMat ((a * w) + (b * y)) ((a * x) + (b * z)) ((c * w) + (d * y)) ((c * x) + (d * z))

    -- We skip abs and signum this time.
    abs = error "not required"
    signum = error "not required"

    -- fromInteger :: Integer -> Mat a
    -- Conceptually, and by example,
    --
    -- fromInteger 4 = ( 4 0 )
    --                 ( 0 4 )
    --
    -- but watch the types!  The LHS 4 has type Integer, but the RHS 4s need to
    -- have type "a".  How do you convert?  Hint: "a" itself is a Num instance...

    fromInteger a = MkMat (fromInteger a) (0) (0) (fromInteger a)
