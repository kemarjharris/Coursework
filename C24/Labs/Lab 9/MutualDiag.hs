module MutualDiag where

import InterpFun
-- Like interpreter from lecture but added support for subtraction: Prim2 Minus

-- Recall recursive factorial from the lecture using the diagonal technique.
--
-- If the recursive function is
--
--     fac = \n -> if n==0 then 1 else fac (n-1)
--
-- then I rewrite and use as
--
--     let mkfac = \f -> \n -> if n==0 then 1 else n * (f f) (n-1)
--     in mkfac mkfac k
--
-- which is mkfac and usefac below:
mkfac = ( "mkfac"
        , Lambda "f" (Lambda "n"
            (Cond
              (Prim2 Eq (Var "n") (Num 0))
              (Num 1)
              (Prim2 Mul (Var "n")
                         (App (App (Var "f") (Var "f"))
                              (Prim2 Minus (Var "n") (Num 1))))))
        )

usefac n = Let [mkfac] (App (App (Var "mkfac") (Var "mkfac")) (Num n))

-- Can test with eg, mainInterp (usefac 10).


-- Now your turn to adapt this to a pair of mutually recursive functions!
-- The pair is

f n = if n==0 then 0 else f (n-1) + g (n-1)
g n = if n==0 then 1 else g (n-1) - f (n-1)

-- Complete mkf, mkg, usef, useg, like mkfac and usefac.

mkf = ( "mkf"
      , Lambda "f" (
            Lambda "g" ( 
                Lambda "n"
                    (Cond
                        (Prim2 Eq (Var "n") (Num 0))
                        (Num 0)
                        (Prim2 Plus 
                            (App
                                (App 
                                    (App (Var "f") (Var "f"))
                                    (Var "g")
                                )
                                (Prim2 Minus (Var "n") (Num 1))
                            )
                            (App
                                (App 
                                    (App (Var "g") (Var "g"))
                                    (Var "f")
                                )
                                (Prim2 Minus (Var "n") (Num 1))
                            )
                            
                        )
                    )
            )
        )
      )

mkg = ( "mkg"
      , Lambda "g"(
           Lambda "f" (
                Lambda "n"
                    (Cond
                        (Prim2 Eq (Var "n") (Num 0))
                        (Num 1)
                        (Prim2 Minus
                            (App
                                (App 
                                    (App (Var "g") (Var "g"))
                                    (Var "f")
                                )
                                (Prim2 Minus (Var "n") (Num 1))
                            )
                            (App
                                (App 
                                    (App (Var "f") (Var "f"))
                                    (Var "g")
                                )
                                (Prim2 Minus (Var "n") (Num 1))
                            )
                        )
                    )
           )
        )
      )

usef n = Let [mkf, mkg]  (App 
                            (App 
                                (App 
                                    (Var "mkf") (Var "mkf")
                                )
                                (Var "mkg")
                            )
                            (Num n)
                        )

useg n = Let [mkf, mkg] (App
                            (App
                                (App 
                                    (Var "mkg") (Var "mkg")
                                )
                                (Var "mkf")
                            )
                            (Num n)
                        )

-- Can test with eg, mainInterp (usef 11), mainInterp (useg 11).
-- Can also check answers with f 11, g 11.