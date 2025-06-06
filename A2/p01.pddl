(define (problem p1-dungeon)
  (:domain Dungeon)

  ; Naming convention:
  ; - loc-{i}-{j} refers to the location at the i'th column and j'th row (starting in top left corner)
  ; - c{i}{j}{h}{k} refers to the corridor connecting loc-{i}-{j} and loc-{h}-{k}
  (:objects
    loc-3-1 loc-1-2 loc-2-2 loc-3-2 loc-4-2 loc-2-3 loc-3-3 loc-2-4 loc-3-4 loc-4-4 - location
    key1 key2 key3 key4 - key
    c3132 c1222 c2232 c3242 c2223 c3233 c2333 c2324 c3334 c2434 c3444 - corridor
  )

  (:init

    ; Hero location and carrying status
    (hero-at loc-1-2)
    (free-hand)
    ; Location <> Corridor Connections
    (connected loc-3-1 loc-3-2 c3132)
    (connected loc-3-2 loc-3-1 c3132)
    (connected loc-1-2 loc-2-2 c1222)
    (connected loc-2-2 loc-1-2 c1222)
    (connected loc-2-2 loc-3-2 c2232)
    (connected loc-3-2 loc-2-2 c2232)
    (connected loc-3-2 loc-4-2 c3242)
    (connected loc-4-2 loc-3-2 c3242)
    (connected loc-2-2 loc-2-3 c2223)
    (connected loc-2-3 loc-2-2 c2223)
    (connected loc-3-2 loc-3-3 c3233)
    (connected loc-3-3 loc-3-2 c3233)
    (connected loc-2-3 loc-3-3 c2333)
    (connected loc-3-3 loc-2-3 c2333)
    (connected loc-2-3 loc-2-4 c2324)
    (connected loc-2-4 loc-2-3 c2324)
    (connected loc-3-3 loc-3-4 c3334)
    (connected loc-3-4 loc-3-3 c3334)
    (connected loc-2-4 loc-3-4 c2434)
    (connected loc-3-4 loc-2-4 c2434)
    (connected loc-3-4 loc-4-4 c3444)
    (connected loc-4-4 loc-3-4 c3444)

    ; Key locations
    (key-at key1 loc-2-2)
    (key-at key2 loc-2-4)
    (key-at key3 loc-4-2)
    (key-at key4 loc-4-4)

    ; Locked corridors
    (locked c3132 rainbow)
    (locked c3242 purple)
    (locked c2324 red)
    (locked c2434 red)
    (locked c3444 yellow)

    ; Unlocked corridors
    (unlocked c1222)
    (unlocked c2232)
    (unlocked c2223)
    (unlocked c3233)
    (unlocked c2333)
    (unlocked c3334)

    ; Risky corridors
    (risky c2324)
    (risky c2434)

    ; Key colours
    (key-colour key1 red)
    (key-colour key2 yellow)
    (key-colour key3 rainbow)
    (key-colour key4 purple)

    ; Key usage properties (one use, two use, etc)
    (multi-use key1)
    (two-use key2)
    (one-use key3)
    (one-use key4)
  )
  (:goal
    (and
      ; Hero's final location goes here
      (hero-at loc-3-1)
    )
  )
)
