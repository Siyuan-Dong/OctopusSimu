import Sketches

sketches=Sketches.Sketches()
for i in range(0,50):
    sketches.insketch[3].Insert(100)
    sketches.update_edge_key(100)
print(sketches.ab_fg())
# print(sketches.insketch[3].Query(100))
# sketches.Clear()
# print(sketches.insketch[3].Query(100))

