conj_podryad_first_lexems = "а и только ради лишь затем для между вопреки невзирая независимо несмотря даром при тогда вроде подобно то да кроме хотя как перед пока после прежде раньше в только в вследствие благодаря ввиду из-за оттого по потому так тем"
conj_sostavnye_first_lexems = "или ли либо не то и ни так когда если как хотя едва чем"

cp = conj_podryad_first_lexems.split()
cs = conj_sostavnye_first_lexems.split()
co = []
for i in cs:
    if i in cp:
        co.append(i)

all_conjs = []

f = open("Conjunction_kinds.TXT", encoding="UTF-8").readlines()
for line in f:
    elem = line.strip("\n").strip("\t")
    if elem[-1] != ":":
        all_conjs.append(elem)
all_conjs.sort()
conj_count = len(all_conjs)

for i in range(conj_count):
    if "...," in all_conjs[i]:
        conj1 = all_conjs[i].split("..., ")[0]
        conj2 = all_conjs[i].split("..., ")[1]
        all_conjs[i] = [conj1.split(), conj2.split()]
    else:
        all_conjs[i] = [all_conjs[i].split(), ""]

for i in all_conjs:
    print(i[0], i[1])
