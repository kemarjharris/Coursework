module ExprParser where

import Control.Applicative

import ExprDef
import ParserLib

mainParser :: Parser Expr
mainParser = whitespaces *> expr <* eof

expr :: Parser Expr
expr = or 
    where
        -- read ors first
        or = chainr1 and (operator "||" *> pure (Prim2 Or))
        -- read ands next
        and = chainr1 eq (operator "&&" *> pure (Prim2 And))
        -- try to read expression
        eq = addsub <* whitespaces 
                -- if == is seen, read right side of eq o/w return what was read by add
            >>= \e1 -> optional (operator "==" <* whitespaces)
                >>= \exists -> case exists of
                    (Just _) -> addsub <* whitespaces
                        >>= \e2 -> return (Prim2 EqNat e1 e2)
                    Nothing -> return e1
        -- read plus minus
        addsub = chainl1 negnot (satisfy (\c -> c `elem` "+-") 
            >>= \op -> case op of
                '+' -> pure (Prim2 Add)
                '-' -> pure (Prim2 Sub)) 
        -- check for possible plus minus
        negnot = optional (satisfy (\c -> c `elem` "!-") <* whitespaces)
            >>= \op -> case op of
                -- if ! is found, read next set of possible op 1s and wrap result
                (Just '!') -> negnot <* whitespaces
                    >>= \v -> return (Prim1 Not v)
                -- same logic as !
                (Just '-') -> negnot <* whitespaces
                    >>= \v -> return (Prim1 Neg v)
                -- If no !- , continue to atomic operators
                Nothing -> atom <* whitespaces
        -- read atomic operators
        atom = fmap LitNat natural
            <|> fmap Var var
            <|> (openParen *> expr <* closeParen)
        -- Read variables except for this one
        var = identifier ["or", "assert", "while", "do"]
        
    