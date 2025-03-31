(define (problem p4-dungeon)
  (:domain Dungeon)

  ; Come up with your own problem instance (see assignment for details)
  ; NOTE: You _may_ use new objects for this problem only.

  ; Naming convention:
  ; - loc-{i}-{j} refers to the location at the i'th column and j'th row (starting in top left corner)
  ; - c{i}{j}{h}{k} refers to the corridor connecting loc-{i}-{j} and loc-{h}-{k}
  (:objects
    loc-1-1 loc-1-2 loc-1-3 loc-2-1 loc-2-2 loc-2-3 loc-3-1 loc-3-2 loc-3-3 - location
    key1 key2 key3 key4 key5 - key
    c1112 c1223 c2313 c2322 c2221 c2231 c3233 c3132 - corridor
  )

  (:init

    ; Hero location and carrying status
    (hero-at loc-1-1)
    (free-hand)

    ; Locationg <> Corridor Connections
    (connected loc-1-1 loc-1-2 c1112)
    (connected loc-1-2 loc-1-1 c1112)
    (connected loc-1-2 loc-2-3 c1223)
    (connected loc-2-3 loc-1-2 c1223)
    (connected loc-2-3 loc-1-3 c2313)
    (connected loc-1-3 loc-2-3 c2313)
    (connected loc-2-3 loc-2-2 c2322)
    (connected loc-2-2 loc-2-3 c2322)
    (connected loc-2-2 loc-2-1 c2221)
    (connected loc-2-1 loc-2-2 c2221)
    (connected loc-2-2 loc-3-1 c2231)
    (connected loc-3-1 loc-2-2 c2231)
    (connected loc-3-2 loc-3-3 c3233)
    (connected loc-3-3 loc-3-2 c3233)
    (connected loc-3-1 loc-3-2 c3132)
    (connected loc-3-2 loc-3-1 c3132)

    ; Key locations
    (key-at key1 loc-1-2)
    (key-at key2 loc-2-1)
    (key-at key3 loc-2-2)
    (key-at key4 loc-3-2)
    (key-at key5 loc-3-3)

    ; Locked corridors
    (locked c1223 red)
    (locked c2231 yellow)
    (locked c2221 yellow)
    (locked c3132 purple)
    (locked c3233 green)
    (locked c2313 rainbow)

    ; Unlocked corridors
    (unlocked c1112)
    (unlocked c2322)

    ; Risky corridors
    (risky c1223)

    ; Key colours
    (key-colour key1 red)
    (key-colour key2 purple)
    (key-colour key3 yellow)
    (key-colour key4 green)
    (key-colour key5 rainbow)

    ; Key usage properties (one use, two use, etc)
    (multi-use key1)
    (two-use key2)
    (one-use key3)
    (one-use key4)
    (one-use key5)
  )
  (:goal
    (and
      ; Hero's final location goes here
      (hero-at loc-1-3)
    )
  )
)
