(define (domain Dungeon)

    (:requirements :typing :negative-preconditions :conditional-effects :fluents :equality)

    ; Do not modify the types
    (:types
        location colour key corridor
    )

    ; Do not modify the constants
    (:constants
        red yellow green purple rainbow - colour
    )

    ; You may introduce whatever predicates you would like to use
    (:predicates

        ; One predicate given for free!
        (hero-at ?loc - location) ;hero location
        (connected ?from ?to -location ?cor - corridor) ;rooms connected by corridor
        (locked ?cor - corridor ?col - colour) ;locked corridor by color
        (unlocked ?cor) ;unlocked state corridor
        (risky ?cor - corridor) ;risky state corridor
        (collapsed ?cor - corridor) ;collapsed state corridor
        (messy ?loc - location) ;messy state corridor
        (holding ?k - key) ;hero holding key
        (free-hand) ;hero hands free
        (key-at ?k - key ?loc - location) ;key location
        (key-colour ?k - key ?col - colour) ;key colour
        (one-use ?k -key) ;key one time use state
        (two-use ?k - key) ;key two time use state
        (multi-use ?k - key) ;key multiuse state (unlimited)
        (used-up ?k -key) ;key used up state (disappears)
    )

    ; IMPORTANT: You should not change/add/remove the action names or parameters

    ;Hero can move if the
    ;    - hero is at current location ?from,
    ;    - hero will move to location ?to,
    ;    - corridor ?cor exists between the ?from and ?to locations
    ;    - there isn't a locked door in corridor ?cor
    ;Effects move the hero, and collapse the corridor if it's "risky" (also causing a mess in the ?to location)
    (:action move

        :parameters (?from ?to - location ?cor - corridor)

        :precondition (and
            (hero-at ?from)
            (connected ?from ?to ?cor)
            (unlocked ?cor)
            (not (collapsed ?cor))
        )

        :effect (and
            (not (hero-at ?from))
            (hero-at ?to)
            (when
                (risky ?cor)
                (and (collapsed ?cor) (messy ?to)))
        )
    )

    ;Hero can pick up a key if the
    ;    - hero is at current location ?loc,
    ;    - there is a key ?k at location ?loc,
    ;    - the hero's arm is free,
    ;    - the location is not messy
    ;Effect will have the hero holding the key and their arm no longer being free
    (:action pick-up

        :parameters (?loc - location ?k - key)

        :precondition (and
            (hero-at ?loc)
            (key-at ?k ?loc)
            (free-hand)
            (not (messy ?loc))
            (not (holding ?k))
        )

        :effect (and
            (not (key-at ?k ?loc))
            (holding ?k)
            (not (free-hand))
        )
    )

    ;Hero can drop a key if the
    ;    - hero is holding a key ?k,
    ;    - the hero is at location ?loc
    ;Effect will be that the hero is no longer holding the key
    (:action drop

        :parameters (?loc - location ?k - key)

        :precondition (and
            (hero-at ?loc)
            (holding ?k)
        )

        :effect (and
            (not (holding ?k))
            (key-at ?k ?loc)
            (free-hand)
        )
    )

    ;Hero can use a key for a corridor if
    ;    - the hero is holding a key ?k,
    ;    - the key still has some uses left,
    ;    - the corridor ?cor is locked with colour ?col,
    ;    - the key ?k is if the right colour ?col,
    ;    - the hero is at location ?loc
    ;    - the corridor is connected to the location ?loc
    ;Effect will be that the corridor is unlocked and the key usage will be updated if necessary
    (:action unlock
        :parameters (?loc - location ?cor - corridor ?col - colour ?k - key)
        :precondition (and
            (hero-at ?loc)
            (holding ?k)
            (locked ?cor ?col)
            (key-colour ?k ?col)
            (exists (?otherloc - location) 
                (connected ?loc ?otherloc ?cor)
            )
        )
        :effect (and
            (not (locked ?cor ?col))
            (unlocked ?cor)

            ;If the key is one-use remove it from holding
            (when (one-use ?k) 
                ((and (used-up ?k) (free-hand)))
            )

            ;If the key is two-use downgrade it to one-use
            (when (two-use ?k) 
                (and (not (two-use ?k)) (one-use ?k))
            )
        )
    )


    ;Hero can clean a location if
    ;    - the hero is at location ?loc,
    ;    - the location is messy
    ;Effect will be that the location is no longer messy
    (:action clean

        :parameters (?loc - location)

        :precondition (and

            (hero-at ?loc)
            (messy ?loc)
        )

        :effect (and
            (not (messy ?loc))
        )
    )

)