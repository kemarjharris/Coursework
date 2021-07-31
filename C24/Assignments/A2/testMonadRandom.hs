-- How to use: runghc testMonadRandom.hs

import           Control.Applicative (liftA2)
import           Data.Ratio ((%)) -- 2 % 5 is Rational notation for 2/5
import           System.Environment (getArgs)
import           System.Exit (exitFailure)
import           Test.HUnit
import           Text.Read (readMaybe)

import           MonadRandomDef
import qualified MonadRandom as C (expectedValue, uniform, hangman, strMatch)

-- Re-assert desired types.
expectedValue :: Fractional q => (t -> q) -> DecisionTree t -> q
expectedValue = C.expectedValue
uniform :: MonadRandom m => [a] -> m a
uniform = C.uniform
hangman :: MonadRandom m => String -> Int -> String -> m WinLose
hangman = C.hangman
strMatch :: String -> Int -> String -> WinLose
strMatch = C.strMatch

probability :: Fractional q => (t -> Bool) -> DecisionTree t -> q
probability pred t = expectedValue bernoulli t
  where
    bernoulli a | pred a = 1
                | otherwise = 0

abcTree = Choose (1/3)
            (Tip 'A')
            (Choose (1/2) (Tip 'B') (Tip 'C'))
abcProfit 'A' = 3
abcProfit 'B' = -1
abcProfit 'C' = -4

testExpectedValue =
    [ expectedValue abcProfit abcTree ~?= -(2%3)
    ]

testFunctor =
    [ fmap reverse (Choose (3/5) (Tip "ab") (Tip "cd"))
      ~?= Choose (3/5) (Tip "ba") (Tip "dc")
    ]

data Coin = Head | Tail deriving (Eq, Ord, Bounded, Enum, Show)

testApplicative =
    [ pure reverse <*> Choose (3/5) (Tip "ab") (Tip "cd")
      ~?= Choose (3/5) (Tip "ba") (Tip "dc")
    , liftA2 (\x y -> (x,y))
          (Choose (1/3) (Tip Head) (Tip Tail))
          (Choose (1/4) (Tip 1) (Tip 2))
      ~?= Choose (1/3)
              (Choose (1/4) (Tip (Head,1)) (Tip (Head,2)))
              (Choose (1/4) (Tip (Tail,1)) (Tip (Tail,2)))
    ]

myK Head = Choose (1/4) (Tip 1) (Tip 2)
myK Tail = Choose (2/5) (Tip 1) (Tip 2)

testMonad =
    [ (Choose (1/3) (Tip Head) (Tip Tail) >>= myK)
      ~?= Choose (1/3)
              (Choose (1/4) (Tip 1) (Tip 2))
              (Choose (2/5) (Tip 1) (Tip 2))
    ]

testMonadRandom =
    [ choose (1/3) (return Head) (return Tail) ~?= Choose (1/3) (Tip Head) (Tip Tail)
    ]

isWin Win = True
isWin Lose = False

testHangman =
    [ probability isWin (hangman "lol" 2 "lcbo") ~?= (1%4)*(1%3)*2,
      probability isWin (hangman "a" 0 "a") ~?= 0,
      probability isWin (hangman "a" 1 "a") ~?= 1
      -- To win in 2 guesses, you must guess 'l' (1/4) then 'o' (1/3),
      -- or the other order.
    ]

testUniform = [uniform [1] ~?= (Tip 1)
              ,uniform [1,2] ~?= Choose (1/2) (Tip 1) (Tip 2)
              ,uniform [1,2,3] ~?= Choose (2/3) (Choose (1/2) (Tip 1) (Tip 2)) (Tip 3)]

testStrMatch = [strMatch "a" 1 "a" ~?= Win,
                strMatch "a" 0 "a" ~?= Lose,
                strMatch "a" 1 "ab" ~?= Win,
                strMatch "a" 1 "ba" ~?= Lose,
                strMatch "a" 1 "c" ~?= Lose,
                strMatch "" 0 "" ~?= Win,
                strMatch "ab" 1 "a" ~?= Lose,
                strMatch "ab" 2 "a" ~?= Lose]

tests = testExpectedValue
        ++ testFunctor ++ testApplicative ++ testMonad ++ testMonadRandom ++ testUniform
        ++ testHangman ++ testStrMatch
-- More tests when marking.

main = do
    args <- getArgs
    case args of
      a:_ | Just n <- readMaybe a, 0 <= n, n < length tests ->
            do c@Counts{errors=e, failures=f} <- runTestTT (tests !! n)
               if e == 0 && f == 0
                   then return c
                   else exitFailure
          | otherwise -> error "No such test number."
      _ -> runTestTT (TestList tests)