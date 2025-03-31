(define (problem p3-dungeon)
  (:domain Dungeon)

  ; Naming convention:
  ; - loc-{i}-{j} refers to the location at the i'th column and j'th row (starting in top left corner)
  ; - c{i}{j}{h}{k} refers to the corridor connecting loc-{i}-{j} and loc-{h}-{k}
  (:objects
    loc-3-4 loc-4-5 loc-1-2 loc-2-2 loc-3-2 loc-3-3 loc-2-5 loc-1-3 loc-2-1 loc-1-4 loc-3-5 loc-2-4 loc-4-4 loc-2-3 loc-4-3 - location
    key1 key2 key3 key4 key5 key6 - key
    c2122 c1222 c2232 c1213 c1223 c2223 c3223 c3233 c1323 c2333 c1314 c2314 c2324 c2334 c3334 c1424 c2434 c2425 c2535 c3545 c4544 c4443 - corridor
  )

  (:init

    ; Hero location and carrying status
    (hero-at loc-2-1)
    (free-hand)

    ; Locationg <> Corridor Connections
    (connected loc-2-1 loc-2-2 c2122)
    (connected loc-2-2 loc-2-1 c2122)
    (connected loc-1-2 loc-2-2 c1222)
    (connected loc-2-2 loc-1-2 c1222)
    (connected loc-2-2 loc-3-2 c2232)
    (connected loc-3-2 loc-2-2 c2232)
    (connected loc-1-2 loc-1-3 c1213)
    (connected loc-1-3 loc-1-2 c1213)
    (connected loc-1-2 loc-2-3 c1223)
    (connected loc-2-3 loc-1-2 c1223)
    (connected loc-2-2 loc-2-3 c2223)
    (connected loc-2-3 loc-2-2 c2223)
    (connected loc-3-2 loc-2-3 c3223)
    (connected loc-2-3 loc-3-2 c3223)
    (connected loc-3-2 loc-3-3 c3233)
    (connected loc-3-3 loc-3-2 c3233)
    (connected loc-1-3 loc-2-3 c1323)
    (connected loc-2-3 loc-1-3 c1323)
    (connected loc-2-3 loc-3-3 c2333)
    (connected loc-3-3 loc-2-3 c2333)
    (connected loc-1-3 loc-1-4 c1314)
    (connected loc-1-4 loc-1-3 c1314)
    (connected loc-2-3 loc-1-4 c2314)
    (connected loc-1-4 loc-2-3 c2314)
    (connected loc-2-3 loc-2-4 c2324)
    (connected loc-2-4 loc-2-3 c2324)
    (connected loc-2-3 loc-3-4 c2334)
    (connected loc-3-4 loc-2-3 c2334)
    (connected loc-3-3 loc-3-4 c3334)
    (connected loc-3-4 loc-3-3 c3334)
    (connected loc-1-4 loc-2-4 c1424)
    (connected loc-2-4 loc-1-4 c1424)
    (connected loc-2-4 loc-3-4 c2434)
    (connected loc-3-4 loc-2-4 c2434)
    (connected loc-2-4 loc-2-5 c2425)
    (connected loc-2-5 loc-2-4 c2425)
    (connected loc-2-5 loc-3-5 c2535)
    (connected loc-3-5 loc-2-5 c2535)
    (connected loc-3-5 loc-4-5 c3545)
    (connected loc-4-5 loc-3-5 c3545)
    (connected loc-4-5 loc-4-4 c4544)
    (connected loc-4-4 loc-4-5 c4544)
    (connected loc-4-4 loc-4-3 c4443)
    (connected loc-4-3 loc-4-4 c4443)

    ; Key locations
    (key-at key1 loc-2-1)
    (key-at key2 loc-2-3)
    (key-at key3 loc-2-3)
    (key-at key4 loc-2-3)
    (key-at key5 loc-2-3)
    (key-at key6 loc-4-4)

    ; Locked corridors
    (locked c1223 red)
    (locked c1323 red)
    (locked c2314 red)
    (locked c2223 red)
    (locked c2324 red)
    (locked c3223 red)
    (locked c2333 red)
    (locked c2334 red)
    (locked c2425 purple)
    (locked c2535 green)
    (locked c3545 purple)
    (locked c4544 green)
    (locked c4443 rainbow)

    ; Unlocked corridors
    (unlocked c2122)
    (unlocked c1222)
    (unlocked c1213)
    (unlocked c1314)
    (unlocked c2232)
    (unlocked c3233)
    (unlocked c3334)
    (unlocked c2434)
    (unlocked c1424)

    ; Risky corridors
    (risky c1223)
    (risky c1323)
    (risky c2314)
    (risky c2223) 
    (risky c2324)
    (risky c3223)
    (risky c2333)
    (risky c2334)

    ; Key colours
    (key-colour key1 red)
    (key-colour key2 green)
    (key-colour key3 green)
    (key-colour key4 purple)
    (key-colour key5 purple)
    (key-colour key6 rainbow)

    ; Key usage properties (one use, two use, etc)
    (multi-use key1)
    (one-use key2)
    (one-use key3)
    (one-use key4)
    (one-use key5)
    (one-use key6)

  )
  (:goal
    (and
      ; Hero's final location goes here
      (hero-at loc-4-3)
    )
  )

)
