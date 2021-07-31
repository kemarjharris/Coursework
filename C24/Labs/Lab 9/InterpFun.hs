module InterpFun where

import           Data.Map.Strict (Map)
import qualified Data.Map.Strict as Map

data Expr
    = Num Integer
    | Bln Bool
    | Var String
    | Prim2 Op2 Expr Expr         -- Prim2 op operand operand
    | Cond Expr Expr Expr         -- Cond test then-branch else-branch
    | Let [(String, Expr)] Expr   -- Let [(name, rhs), ...] eval-me
    | Lambda String Expr          -- Lambda var body
    | App Expr Expr               -- App func param
    deriving (Eq, Show)

data Op2 = Eq | Plus | Minus | Mul
    deriving (Eq, Show)

-- The type of possible values from the interpreter.
data Value = VN Integer
           | VB Bool
           | VClosure (Map String Value) String Expr
    deriving (Eq, Show)

mainInterp :: Expr -> Either String Value
-- There can be failure conditions such as variable not found and wrong operand
-- type.  I use "Left errorMessage" to represent failures.  Recall that "Either
-- String" is a monad, this will be useful.
mainInterp expr = interp expr Map.empty

-- Helper to raise errors.  Why not say "Left" everywhere?  Because more
-- future-proof.
raise :: String -> Either String a
raise = Left

-- Helper to expect the VN case (failure if not) and return the integer.
intOrDie :: Value -> Either String Integer
intOrDie (VN i) = pure i
intOrDie _ = raise "type error"

interp :: Expr -> Map String Value -> Either String Value

interp (Num i) _ = pure (VN i)

interp (Bln b) _ = pure (VB b)

interp (Prim2 Plus e1 e2) env =
    interp e1 env
    >>= \a -> intOrDie a
    >>= \i -> interp e2 env
    >>= \b -> intOrDie b
    >>= \j -> return (VN (i+j))

interp (Prim2 Minus e1 e2) env =
    interp e1 env
    >>= \a -> intOrDie a
    >>= \i -> interp e2 env
    >>= \b -> intOrDie b
    >>= \j -> return (VN (i-j))

interp (Prim2 Mul e1 e2) env =
    interp e1 env
    >>= \a -> intOrDie a
    >>= \i -> interp e2 env
    >>= \b -> intOrDie b
    >>= \j -> return (VN (i*j))

interp (Prim2 Eq e1 e2) env =
    interp e1 env
    >>= \a -> intOrDie a
    >>= \i -> interp e2 env
    >>= \b -> intOrDie b
    >>= \j -> return (VB (i == j))

interp (Cond test eThen eElse) env =
    interp test env
    >>= \a -> case a of
      VB True -> interp eThen env
      VB False -> interp eElse env
      _ -> raise "type error"

interp (Var v) env = case Map.lookup v env of
  Just a -> pure a
  Nothing -> raise "variable not found"

interp (Let eqns evalMe) env =
    extend eqns env
    >>= \env' -> interp evalMe env'
    -- Example:
    --    let x=2+3; y=x+4 in x+y
    -- -> x+y   (with x=5, y=9 in the larger environment env')
    -- "extend env eqns" builds env'
  where
    extend [] env = return env
    extend ((v,rhs) : eqns) env =
        interp rhs env
        >>= \a -> let env' = Map.insert v a env
                  in extend eqns env'

interp (Lambda v body) env = pure (VClosure env v body)

interp (App f e) env =
    interp f env
    >>= \c -> case c of
      VClosure fEnv v body ->
          interp e env
          >>= \eVal -> let bEnv = Map.insert v eVal fEnv  -- fEnv, not env
                       in interp body bEnv
          -- E.g.,
          --    (\y -> 10+y) 17
          -- -> 10 + y      (but with y=17 in environment)
          --
      _ -> raise "type error"
