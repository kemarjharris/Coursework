module Huffman where

import           Data.Map.Strict (Map, (!))
import qualified Data.Map.Strict as Map
import           LeftistHeap (PQueue)
import qualified LeftistHeap as PQueue

import           HuffmanDef

decode :: HuffmanTree -> [Bool] -> [Char]
decode tree bools = decodeHelper tree tree bools [] 

decodeHelper :: HuffmanTree -> HuffmanTree -> [Bool] -> [Char] -> [Char]
decodeHelper _ leaf@(Leaf k char) [] accum = accum ++ [char]
decodeHelper ogtree leaf@(Leaf k char) (x:xs) accum = decodeHelper ogtree ogtree (x:xs) (accum ++ [char])
decodeHelper ogtree branch@(Branch k l r) (x:xs) accum
    | x == False =  decodeHelper ogtree l xs accum
    | x == True = decodeHelper ogtree r xs accum


huffmanTree :: [(Char, Int)] -> HuffmanTree
huffmanTree (x:xs) = huffmanTreeHelper (makeQueue (x:xs) (PQueue.empty))

huffmanTreeHelper :: PQueue Int HuffmanTree -> HuffmanTree 
huffmanTreeHelper queue
    | huffmanCheck firstTree secondTree = huffmanTreeHelper (insertHelper (makeBranch (firstTree) (secondTree)) (nextQueue)) 
    | otherwise = firstTree
        where 
            next = nextTwo queue
            firstPair = head next
            secondPair = last next
            firstTree = snd firstPair
            secondTree = snd secondPair
            nextQueue = fst secondPair 

huffmanCheck :: HuffmanTree -> HuffmanTree -> Bool
huffmanCheck _ branch@(Branch pri l r) = True
huffmanCheck _ leaf@(Leaf pri char) = pri >= 0

insertHelper :: HuffmanTree -> PQueue Int HuffmanTree -> PQueue Int HuffmanTree
insertHelper branch@(Branch pri l r) queue = PQueue.insert pri branch queue


huffmanExtract :: [(Char, Int)] -> [(PQueue Int HuffmanTree, HuffmanTree)]
huffmanExtract queue = nextTwo ((makeQueue (queue) (PQueue.empty)))

nextTwo :: PQueue Int HuffmanTree -> [(PQueue Int HuffmanTree, HuffmanTree)]
nextTwo queue = [a, b]
    where
        a = huffmanMaybe (PQueue.extractMin (queue))
        b = huffmanMaybe (PQueue.extractMin (fst a))

huffmanMaybe :: Maybe (PQueue Int HuffmanTree, HuffmanTree) -> (PQueue Int HuffmanTree, HuffmanTree)
huffmanMaybe Nothing = (PQueue.empty, Leaf (-1) ' ')
huffmanMaybe (Just a) = a

makeBranch :: HuffmanTree -> HuffmanTree -> HuffmanTree
makeBranch x@(Leaf xPri xChar) y@(Leaf yPri yChar) = Branch (xPri + yPri) x y
makeBranch x@(Branch xPri xl xr) y@(Leaf yPri yChar) = Branch (xPri + yPri) x y
makeBranch x@(Leaf xPri xChar) y@(Branch yPri yl yr) = Branch (xPri + yPri) x y
makeBranch x@(Branch xPri xl xr) y@(Branch yPri yl yr) = Branch (xPri + yPri) x y

makeQueue :: [(Char, Int)] -> PQueue Int HuffmanTree -> PQueue Int HuffmanTree
makeQueue [] queue = queue
makeQueue (x:xs) queue = makeQueue xs (PQueue.insert (snd x) (Leaf (snd x) (fst x)) queue)

buildDict :: HuffmanTree -> Map Char [Bool]
buildDict tree = buildDictHelper tree Map.empty []

buildDictHelper :: HuffmanTree -> Map Char [Bool] -> [Bool] -> Map Char [Bool]
buildDictHelper leaf@(Leaf pri char) map path = Map.insert (char) path map
buildDictHelper branch@(Branch pri l r) map path = finalMap
    where
        leftMap = buildDictHelper (l) (map) (path ++ [False])
        finalMap = buildDictHelper (r) (leftMap) (path ++ [True])

encode :: HuffmanTree -> [Char] -> [Bool]
encode tree cs = concatMap (\c -> dict ! c) cs
  where
    dict = buildDict tree