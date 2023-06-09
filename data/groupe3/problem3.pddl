(define (problem rubik3)
    (:domain rubik)
    (:objects r w b g o y - color)
    (:init
        (face1 o g w)
        (face2 o b w)
        (face3 r g w)
        (face4 r b w)
        (face5 o g y)
        (face6 o b y)
        (face7 r g y)
        (face8 r b y)
    )
    (:goal (and
        (face1 o b y)
        (face2 r g w)
        (face3 y r b)
        (face4 b o w)
        (face5 y o g)
        (face6 r b w)
        (face7 w o g)
        (face8 r y g)
        )
    )
)

