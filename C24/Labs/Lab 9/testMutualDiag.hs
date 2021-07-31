-- How to use: runghc testMutualDiag.hs

import System.Environment (getArgs)
import System.Exit (exitFailure)
import Test.HUnit
import Text.Read (readMaybe)

import InterpFun
import MutualDiag (usef, useg)

tests =
    [ mainInterp (usef 11) ~?= Right (VN 32)
    , mainInterp (useg 11) ~?= Right (VN (-32))
    ]
-- more tests when marking

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