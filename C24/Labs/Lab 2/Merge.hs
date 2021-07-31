module Merge where

-- There are other questions in other files.

-- Take two lists of integers.  Precondition: Each is already sorted
-- (non-decreasing).  Merge them in non-decreasing order.  Linear time.
--
-- Although intended to be part of mergesort, don't make assumptions about the
-- lengths of the two lists --- they may have very different lengths.
--
-- Example:
-- merge [2, 3, 5] [1, 3, 4, 4, 7] = [1, 2, 3, 3, 4, 4, 5, 7]

merge :: [Integer] -> [Integer] -> [Integer]
merge [] [] = []
merge axt [] = axt
merge [] bxt = bxt
merge axt@(a:axs) bxt@(b:bxs)
    | a < b = a: merge (axs) (bxt)
    | otherwise = b: merge (axt) (bxs)

