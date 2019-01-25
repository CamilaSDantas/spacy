# The following list consists of:
# - exceptions generated from polish_srx_rules [1]
#    (https://github.com/milekpl/polish_srx_rules)
# - abbreviations parsed from Wikipedia
# - some manually added exceptions
#
# [1] M. Miłkowski and J. Lipski,
#  “Using SRX Standard for Sentence Segmentation,” in LTC 2009,
#  Lecture Notes in Artificial Intelligence 6562,
#  Z. Vetulani, Ed. Berlin Heidelberg: Springer-Verlag, 2011, pp. 172–182.
PL_BASE_EXCEPTIONS = ['0.',
'1.',
'10.',
'2.',
'3.',
'4.',
'5.',
'6.',
'7.',
'8.',
'9.',
'A.A.',
'A.B.',
'A.C.',
'A.D.',
'A.E.',
'A.F.',
'A.G.',
'A.H.',
'A.I.',
'A.J.',
'A.K.',
'A.L.',
'A.M.',
'A.N.',
'A.O.',
'A.P.',
'A.R.',
'A.S.',
'A.T.',
'A.U.',
'A.W.',
'A.Y.',
'A.Z.',
'A.Ó.',
'A.Ą.',
'A.Ć.',
'A.Ę.',
'A.Ł.',
'A.Ń.',
'A.Ś.',
'A.Ź.',
'A.Ż.',
'Ad.',
'Adw.',
'Al.',
'Art.',
'B.A.',
'B.B.',
'B.C.',
'B.D.',
'B.E.',
'B.F.',
'B.G.',
'B.H.',
'B.I.',
'B.J.',
'B.K.',
'B.L.',
'B.M.',
'B.N.',
'B.O.',
'B.P.',
'B.R.',
'B.S.',
'B.T.',
'B.U.',
'B.W.',
'B.Y.',
'B.Z.',
'B.Ó.',
'B.Ą.',
'B.Ć.',
'B.Ę.',
'B.Ł.',
'B.Ń.',
'B.Ś.',
'B.Ź.',
'B.Ż.',
'D.A.',
'D.B.',
'D.C.',
'D.D.',
'D.E.',
'D.F.',
'D.G.',
'D.H.',
'D.I.',
'D.J.',
'D.K.',
'D.L.',
'D.M.',
'D.N.',
'D.O.',
'D.P.',
'D.R.',
'D.S.',
'D.T.',
'D.U.',
'D.W.',
'D.Y.',
'D.Z.',
'D.Ó.',
'D.Ą.',
'D.Ć.',
'D.Ę.',
'D.Ł.',
'D.Ń.',
'D.Ś.',
'D.Ź.',
'D.Ż.',
'Dh.',
'Doc.',
'Dr.',
'Dyr.',
'Dyw.',
'Dz.U.',
'E.A.',
'E.B.',
'E.C.',
'E.D.',
'E.E.',
'E.F.',
'E.G.',
'E.H.',
'E.I.',
'E.J.',
'E.K.',
'E.L.',
'E.M.',
'E.N.',
'E.O.',
'E.P.',
'E.R.',
'E.S.',
'E.T.',
'E.U.',
'E.W.',
'E.Y.',
'E.Z.',
'E.Ó.',
'E.Ą.',
'E.Ć.',
'E.Ę.',
'E.Ł.',
'E.Ń.',
'E.Ś.',
'E.Ź.',
'E.Ż.',
'F.A.',
'F.B.',
'F.C.',
'F.D.',
'F.E.',
'F.F.',
'F.G.',
'F.H.',
'F.I.',
'F.J.',
'F.K.',
'F.L.',
'F.M.',
'F.N.',
'F.O.',
'F.P.',
'F.R.',
'F.S.',
'F.T.',
'F.U.',
'F.W.',
'F.Y.',
'F.Z.',
'F.Ó.',
'F.Ą.',
'F.Ć.',
'F.Ę.',
'F.Ł.',
'F.Ń.',
'F.Ś.',
'F.Ź.',
'F.Ż.',
'G.A.',
'G.B.',
'G.C.',
'G.D.',
'G.E.',
'G.F.',
'G.G.',
'G.H.',
'G.I.',
'G.J.',
'G.K.',
'G.L.',
'G.M.',
'G.N.',
'G.O.',
'G.P.',
'G.R.',
'G.S.',
'G.T.',
'G.U.',
'G.W.',
'G.Y.',
'G.Z.',
'G.Ó.',
'G.Ą.',
'G.Ć.',
'G.Ę.',
'G.Ł.',
'G.Ń.',
'G.Ś.',
'G.Ź.',
'G.Ż.',
'H.A.',
'H.B.',
'H.C.',
'H.D.',
'H.E.',
'H.F.',
'H.G.',
'H.H.',
'H.I.',
'H.J.',
'H.K.',
'H.L.',
'H.M.',
'H.N.',
'H.O.',
'H.P.',
'H.R.',
'H.S.',
'H.T.',
'H.U.',
'H.W.',
'H.Y.',
'H.Z.',
'H.Ó.',
'H.Ą.',
'H.Ć.',
'H.Ę.',
'H.Ł.',
'H.Ń.',
'H.Ś.',
'H.Ź.',
'H.Ż.',
'Hr.',
'I.A.',
'I.B.',
'I.C.',
'I.D.',
'I.E.',
'I.F.',
'I.G.',
'I.H.',
'I.I.',
'I.J.',
'I.K.',
'I.L.',
'I.M.',
'I.N.',
'I.O.',
'I.P.',
'I.R.',
'I.S.',
'I.T.',
'I.U.',
'I.W.',
'I.Y.',
'I.Z.',
'I.Ó.',
'I.Ą.',
'I.Ć.',
'I.Ę.',
'I.Ł.',
'I.Ń.',
'I.Ś.',
'I.Ź.',
'I.Ż.',
'Inż.',
'J.A.',
'J.B.',
'J.C.',
'J.D.',
'J.E.',
'J.F.',
'J.G.',
'J.H.',
'J.I.',
'J.J.',
'J.K.',
'J.L.',
'J.M.',
'J.N.',
'J.O.',
'J.P.',
'J.R.',
'J.S.',
'J.T.',
'J.U.',
'J.W.',
'J.Y.',
'J.Z.',
'J.Ó.',
'J.Ą.',
'J.Ć.',
'J.Ę.',
'J.Ł.',
'J.Ń.',
'J.Ś.',
'J.Ź.',
'J.Ż.',
'K.A.',
'K.B.',
'K.C.',
'K.D.',
'K.E.',
'K.F.',
'K.G.',
'K.H.',
'K.I.',
'K.J.',
'K.K.',
'K.L.',
'K.M.',
'K.N.',
'K.O.',
'K.P.',
'K.R.',
'K.S.',
'K.T.',
'K.U.',
'K.W.',
'K.Y.',
'K.Z.',
'K.Ó.',
'K.Ą.',
'K.Ć.',
'K.Ę.',
'K.Ł.',
'K.Ń.',
'K.Ś.',
'K.Ź.',
'K.Ż.',
'Ks.',
'L.A.',
'L.B.',
'L.C.',
'L.D.',
'L.E.',
'L.F.',
'L.G.',
'L.H.',
'L.I.',
'L.J.',
'L.K.',
'L.L.',
'L.M.',
'L.N.',
'L.O.',
'L.P.',
'L.R.',
'L.S.',
'L.T.',
'L.U.',
'L.W.',
'L.Y.',
'L.Z.',
'L.Ó.',
'L.Ą.',
'L.Ć.',
'L.Ę.',
'L.Ł.',
'L.Ń.',
'L.Ś.',
'L.Ź.',
'L.Ż.',
'Lek.',
'M.A.',
'M.B.',
'M.C.',
'M.D.',
'M.E.',
'M.F.',
'M.G.',
'M.H.',
'M.I.',
'M.J.',
'M.K.',
'M.L.',
'M.M.',
'M.N.',
'M.O.',
'M.P.',
'M.R.',
'M.S.',
'M.T.',
'M.U.',
'M.W.',
'M.Y.',
'M.Z.',
'M.Ó.',
'M.Ą.',
'M.Ć.',
'M.Ę.',
'M.Ł.',
'M.Ń.',
'M.Ś.',
'M.Ź.',
'M.Ż.',
'Mat.',
'Mec.',
'Mojż.',
'N.A.',
'N.B.',
'N.C.',
'N.D.',
'N.E.',
'N.F.',
'N.G.',
'N.H.',
'N.I.',
'N.J.',
'N.K.',
'N.L.',
'N.M.',
'N.N.',
'N.O.',
'N.P.',
'N.R.',
'N.S.',
'N.T.',
'N.U.',
'N.W.',
'N.Y.',
'N.Z.',
'N.Ó.',
'N.Ą.',
'N.Ć.',
'N.Ę.',
'N.Ł.',
'N.Ń.',
'N.Ś.',
'N.Ź.',
'N.Ż.',
'Na os.',
'Nadkom.',
'Najśw.',
'Nb.',
'Np.',
'O.A.',
'O.B.',
'O.C.',
'O.D.',
'O.E.',
'O.F.',
'O.G.',
'O.H.',
'O.I.',
'O.J.',
'O.K.',
'O.L.',
'O.M.',
'O.N.',
'O.O.',
'O.P.',
'O.R.',
'O.S.',
'O.T.',
'O.U.',
'O.W.',
'O.Y.',
'O.Z.',
'O.Ó.',
'O.Ą.',
'O.Ć.',
'O.Ę.',
'O.Ł.',
'O.Ń.',
'O.Ś.',
'O.Ź.',
'O.Ż.',
'OO.',
'Oo.',
'P.A.',
'P.B.',
'P.C.',
'P.D.',
'P.E.',
'P.F.',
'P.G.',
'P.H.',
'P.I.',
'P.J.',
'P.K.',
'P.L.',
'P.M.',
'P.N.',
'P.O.',
'P.P.',
'P.R.',
'P.S.',
'P.T.',
'P.U.',
'P.W.',
'P.Y.',
'P.Z.',
'P.Ó.',
'P.Ą.',
'P.Ć.',
'P.Ę.',
'P.Ł.',
'P.Ń.',
'P.Ś.',
'P.Ź.',
'P.Ż.',
'Podkom.',
'Przyp.',
'Ps.',
'Pt.',
'Płk.',
'R.A.',
'R.B.',
'R.C.',
'R.D.',
'R.E.',
'R.F.',
'R.G.',
'R.H.',
'R.I.',
'R.J.',
'R.K.',
'R.L.',
'R.M.',
'R.N.',
'R.O.',
'R.P.',
'R.R.',
'R.S.',
'R.T.',
'R.U.',
'R.W.',
'R.Y.',
'R.Z.',
'R.Ó.',
'R.Ą.',
'R.Ć.',
'R.Ę.',
'R.Ł.',
'R.Ń.',
'R.Ś.',
'R.Ź.',
'R.Ż.',
'Red.',
'Reż.',
'Ryc.',
'Rys.',
'S.A.',
'S.B.',
'S.C.',
'S.D.',
'S.E.',
'S.F.',
'S.G.',
'S.H.',
'S.I.',
'S.J.',
'S.K.',
'S.L.',
'S.M.',
'S.N.',
'S.O.',
'S.P.',
'S.R.',
'S.S.',
'S.T.',
'S.U.',
'S.W.',
'S.Y.',
'S.Z.',
'S.Ó.',
'S.Ą.',
'S.Ć.',
'S.Ę.',
'S.Ł.',
'S.Ń.',
'S.Ś.',
'S.Ź.',
'S.Ż.',
'Sp.',
'Spółdz.',
'Stow.',
'Stoł.',
'Sz.P.',
'Szer.',
'T.A.',
'T.B.',
'T.C.',
'T.D.',
'T.E.',
'T.F.',
'T.G.',
'T.H.',
'T.I.',
'T.J.',
'T.K.',
'T.L.',
'T.M.',
'T.N.',
'T.O.',
'T.P.',
'T.R.',
'T.S.',
'T.T.',
'T.U.',
'T.W.',
'T.Y.',
'T.Z.',
'T.Ó.',
'T.Ą.',
'T.Ć.',
'T.Ę.',
'T.Ł.',
'T.Ń.',
'T.Ś.',
'T.Ź.',
'T.Ż.',
'Tow.',
'Tzw.',
'U.A.',
'U.B.',
'U.C.',
'U.D.',
'U.E.',
'U.F.',
'U.G.',
'U.H.',
'U.I.',
'U.J.',
'U.K.',
'U.L.',
'U.M.',
'U.N.',
'U.O.',
'U.P.',
'U.R.',
'U.S.',
'U.T.',
'U.U.',
'U.W.',
'U.Y.',
'U.Z.',
'U.Ó.',
'U.Ą.',
'U.Ć.',
'U.Ę.',
'U.Ł.',
'U.Ń.',
'U.Ś.',
'U.Ź.',
'U.Ż.',
'W.A.',
'W.B.',
'W.C.',
'W.D.',
'W.E.',
'W.F.',
'W.G.',
'W.H.',
'W.I.',
'W.J.',
'W.K.',
'W.L.',
'W.M.',
'W.N.',
'W.O.',
'W.P.',
'W.R.',
'W.S.',
'W.T.',
'W.U.',
'W.W.',
'W.Y.',
'W.Z.',
'W.Ó.',
'W.Ą.',
'W.Ć.',
'W.Ę.',
'W.Ł.',
'W.Ń.',
'W.Ś.',
'W.Ź.',
'W.Ż.',
'Y.A.',
'Y.B.',
'Y.C.',
'Y.D.',
'Y.E.',
'Y.F.',
'Y.G.',
'Y.H.',
'Y.I.',
'Y.J.',
'Y.K.',
'Y.L.',
'Y.M.',
'Y.N.',
'Y.O.',
'Y.P.',
'Y.R.',
'Y.S.',
'Y.T.',
'Y.U.',
'Y.W.',
'Y.Y.',
'Y.Z.',
'Y.Ó.',
'Y.Ą.',
'Y.Ć.',
'Y.Ę.',
'Y.Ł.',
'Y.Ń.',
'Y.Ś.',
'Y.Ź.',
'Y.Ż.',
'Z.A.',
'Z.B.',
'Z.C.',
'Z.D.',
'Z.E.',
'Z.F.',
'Z.G.',
'Z.H.',
'Z.I.',
'Z.J.',
'Z.K.',
'Z.L.',
'Z.M.',
'Z.N.',
'Z.O.',
'Z.P.',
'Z.R.',
'Z.S.',
'Z.T.',
'Z.U.',
'Z.W.',
'Z.Y.',
'Z.Z.',
'Z.Ó.',
'Z.Ą.',
'Z.Ć.',
'Z.Ę.',
'Z.Ł.',
'Z.Ń.',
'Z.Ś.',
'Z.Ź.',
'Z.Ż.',
'Zob.',
'a.',
'ad.',
'adw.',
'afr.',
'ags.',
'akad.',
'al.',
'alb.',
'am.',
'amer.',
'ang.',
'aor.',
'ap.',
'apost.',
'arch.',
'arcyks.',
'art.',
'artyst.',
'asp.',
'astr.',
'aust.',
'austr.',
'austral.',
'b.',
'bałt.',
'bdb.',
'belg.',
'białorus.',
'białost.',
'bm.',
'bot.',
'bp.',
'br.',
'bryg.',
'bryt.',
'bułg.',
'bł.',
'c.b.d.o.',
'c.k.',
'c.o.',
'cbdu.',
'cd.',
'cdn.',
'centr.',
'ces.',
'chem.',
'chir.',
'chiń.',
'chor.',
'chorw.',
'cieśn.',
'cnd.',
'cyg.',
'cyt.',
'cyw.',
'cz.',
'czes.',
'czw.',
'czyt.',
'd.',
'daw.',
'dcn.',
'dekl.',
'demokr.',
'det.',
'dh.',
'diec.',
'dk.',
'dn.',
'doc.',
'doktor h.c.',
'dol.',
'dolnośl.',
'dost.',
'dosł.',
'dot.',
'dr h.c.',
'dr hab.',
'dr.',
'ds.',
'dst.',
'duszp.',
'dypl.',
'dyr.',
'dyw.',
'dł.',
'egz.',
'ekol.',
'ekon.',
'elektr.',
'em.',
'ent.',
'est.',
'europ.',
'ew.',
'fab.',
'farm.',
'fot.',
'fr.',
'franc.',
'g.',
'gastr.',
'gat.',
'gd.',
'gen.',
'geogr.',
'geol.',
'gimn.',
'gm.',
'godz.',
'gorz.',
'gosp.',
'gosp.-polit.',
'gr.',
'gram.',
'grub.',
'górn.',
'głęb.',
'h.c.',
'hab.',
'hist.',
'hiszp.',
'hitl.',
'hm.',
'hot.',
'hr.',
'i in.',
'i s.',
'id.',
'ie.',
'im.',
'in.',
'inż.',
'iron.',
'itd.',
'itp.',
'j.',
'j.a.',
'jez.',
'jn.',
'jw.',
'jwt.',
'k.',
'k.k.',
'k.o.',
'k.p.a.',
'k.p.c.',
'k.r.',
'k.r.o.',
'kard.',
'kark.',
'kasz.',
'kat.',
'katol.',
'kier.',
'kk.',
'kl.',
'kol.',
'kpc.',
'kpt.',
'kr.',
'krak.',
'kryt.',
'ks.',
'książk.',
'kuj.',
'kult.',
'kł.',
'l.',
'laic.',
'lek.',
'lit.',
'lp.',
'lub.',
'm.',
'm.b.',
'm.in.',
'm.p.',
'm.st.',
'mar.',
'maz.',
'małop.',
'mec.',
'med.',
'mgr.',
'min.',
'mn.',
'mn.w.',
'muz.',
'mł.',
'n.',
'n.e.',
'n.p.m.',
'n.p.u.',
'na os.',
'nadkom.',
'najśw.',
'nb.',
'niedz.',
'niem.',
'norw.',
'np.',
'nt.',
'nż.',
'o s.',
'o.',
'oO.',
'ob.',
'odc.',
'odp.',
'ok.',
'oo.',
'op.',
'os.',
'p.',
'p.a.',
'p.f.',
'p.f.v.',
'p.n.e.',
'p.o.',
'p.p.',
'p.p.m.',
'p.r.',
'p.r.v.',
'phm.',
'pie.',
'pl.',
'pn.',
'pocz.',
'pod.',
'podgat.',
'podkarp.',
'podkom.',
'poet.',
'poj.',
'pok.',
'pol.',
'pom.',
'pon.',
'poprz.',
'por.',
'port.',
'posp.',
'pow.',
'poz.',
'poł.',
'pp.',
'ppanc.',
'ppor.',
'ppoż.',
'prawdop.',
'proc.',
'prof.',
'prok.',
'przed Chr.',
'przyp.',
'ps.',
'pseud.',
'pt.',
'pw.',
'półn.',
'płd.',
'płk.',
'płn.',
'r.',
'r.ż.',
'red.',
'reż.',
'ros.',
'rozdz.',
'rtg.',
'rtm.',
'rub.',
'rum.',
'ryc.',
'rys.',
'rz.',
's.',
'serb.',
'sierż.',
'skr.',
'sob.',
'sp.',
'społ.',
'spółdz.',
'spółgł.',
'st.',
'st.rus.',
'stow.',
'stoł.',
'str.',
'sud.',
'szczec.',
'szer.',
'szt.',
'szw.',
'szwajc.',
'słow.',
't.',
't.j.',
'tatrz.',
'tel.',
'tj.',
'tow.',
'trl.',
'tryb.',
'ts.',
'tur.',
'tys.',
'tzn.',
'tzw.',
'tłum.',
'u s.',
'ub.',
'ukr.',
'ul.',
'up.',
'ur.',
'v.v.',
'vs.',
'w.',
'warm.',
'wlk.',
'wlkp.',
'woj.',
'wroc.',
'ws.',
'wsch.',
'wt.',
'ww.',
'wyb.',
'wyd.',
'wyj.',
'wym.',
'wyst.',
'wył.',
'wyż.',
'wzgl.',
'wędr.',
'węg.',
'wł.',
'x.',
'xx.',
'zach.',
'zagr.',
'zak.',
'zakł.',
'zal.',
'zam.',
'zast.',
'zaw.',
'zazw.',
'zał.',
'zdr.',
'zew.',
'zewn.',
'ziel.',
'zm.',
'zn.',
'zob.',
'zool.',
'zw.',
'ząbk.',
'Ó.A.',
'Ó.B.',
'Ó.C.',
'Ó.D.',
'Ó.E.',
'Ó.F.',
'Ó.G.',
'Ó.H.',
'Ó.I.',
'Ó.J.',
'Ó.K.',
'Ó.L.',
'Ó.M.',
'Ó.N.',
'Ó.O.',
'Ó.P.',
'Ó.R.',
'Ó.S.',
'Ó.T.',
'Ó.U.',
'Ó.W.',
'Ó.Y.',
'Ó.Z.',
'Ó.Ó.',
'Ó.Ą.',
'Ó.Ć.',
'Ó.Ę.',
'Ó.Ł.',
'Ó.Ń.',
'Ó.Ś.',
'Ó.Ź.',
'Ó.Ż.',
'Ą.A.',
'Ą.B.',
'Ą.C.',
'Ą.D.',
'Ą.E.',
'Ą.F.',
'Ą.G.',
'Ą.H.',
'Ą.I.',
'Ą.J.',
'Ą.K.',
'Ą.L.',
'Ą.M.',
'Ą.N.',
'Ą.O.',
'Ą.P.',
'Ą.R.',
'Ą.S.',
'Ą.T.',
'Ą.U.',
'Ą.W.',
'Ą.Y.',
'Ą.Z.',
'Ą.Ó.',
'Ą.Ą.',
'Ą.Ć.',
'Ą.Ę.',
'Ą.Ł.',
'Ą.Ń.',
'Ą.Ś.',
'Ą.Ź.',
'Ą.Ż.',
'Ć.A.',
'Ć.B.',
'Ć.C.',
'Ć.D.',
'Ć.E.',
'Ć.F.',
'Ć.G.',
'Ć.H.',
'Ć.I.',
'Ć.J.',
'Ć.K.',
'Ć.L.',
'Ć.M.',
'Ć.N.',
'Ć.O.',
'Ć.P.',
'Ć.R.',
'Ć.S.',
'Ć.T.',
'Ć.U.',
'Ć.W.',
'Ć.Y.',
'Ć.Z.',
'Ć.Ó.',
'Ć.Ą.',
'Ć.Ć.',
'Ć.Ę.',
'Ć.Ł.',
'Ć.Ń.',
'Ć.Ś.',
'Ć.Ź.',
'Ć.Ż.',
'ćw.',
'ćwicz.',
'Ę.A.',
'Ę.B.',
'Ę.C.',
'Ę.D.',
'Ę.E.',
'Ę.F.',
'Ę.G.',
'Ę.H.',
'Ę.I.',
'Ę.J.',
'Ę.K.',
'Ę.L.',
'Ę.M.',
'Ę.N.',
'Ę.O.',
'Ę.P.',
'Ę.R.',
'Ę.S.',
'Ę.T.',
'Ę.U.',
'Ę.W.',
'Ę.Y.',
'Ę.Z.',
'Ę.Ó.',
'Ę.Ą.',
'Ę.Ć.',
'Ę.Ę.',
'Ę.Ł.',
'Ę.Ń.',
'Ę.Ś.',
'Ę.Ź.',
'Ę.Ż.',
'Ł.A.',
'Ł.B.',
'Ł.C.',
'Ł.D.',
'Ł.E.',
'Ł.F.',
'Ł.G.',
'Ł.H.',
'Ł.I.',
'Ł.J.',
'Ł.K.',
'Ł.L.',
'Ł.M.',
'Ł.N.',
'Ł.O.',
'Ł.P.',
'Ł.R.',
'Ł.S.',
'Ł.T.',
'Ł.U.',
'Ł.W.',
'Ł.Y.',
'Ł.Z.',
'Ł.Ó.',
'Ł.Ą.',
'Ł.Ć.',
'Ł.Ę.',
'Ł.Ł.',
'Ł.Ń.',
'Ł.Ś.',
'Ł.Ź.',
'Ł.Ż.',
'Łuk.',
'łac.',
'łot.',
'łow.',
'Ń.A.',
'Ń.B.',
'Ń.C.',
'Ń.D.',
'Ń.E.',
'Ń.F.',
'Ń.G.',
'Ń.H.',
'Ń.I.',
'Ń.J.',
'Ń.K.',
'Ń.L.',
'Ń.M.',
'Ń.N.',
'Ń.O.',
'Ń.P.',
'Ń.R.',
'Ń.S.',
'Ń.T.',
'Ń.U.',
'Ń.W.',
'Ń.Y.',
'Ń.Z.',
'Ń.Ó.',
'Ń.Ą.',
'Ń.Ć.',
'Ń.Ę.',
'Ń.Ł.',
'Ń.Ń.',
'Ń.Ś.',
'Ń.Ź.',
'Ń.Ż.',
'Ś.A.',
'Ś.B.',
'Ś.C.',
'Ś.D.',
'Ś.E.',
'Ś.F.',
'Ś.G.',
'Ś.H.',
'Ś.I.',
'Ś.J.',
'Ś.K.',
'Ś.L.',
'Ś.M.',
'Ś.N.',
'Ś.O.',
'Ś.P.',
'Ś.R.',
'Ś.S.',
'Ś.T.',
'Ś.U.',
'Ś.W.',
'Ś.Y.',
'Ś.Z.',
'Ś.Ó.',
'Ś.Ą.',
'Ś.Ć.',
'Ś.Ę.',
'Ś.Ł.',
'Ś.Ń.',
'Ś.Ś.',
'Ś.Ź.',
'Ś.Ż.',
'ŚW.',
'Śp.',
'Św.',
'śW.',
'śl.',
'śp.',
'śr.',
'św.',
'Ź.A.',
'Ź.B.',
'Ź.C.',
'Ź.D.',
'Ź.E.',
'Ź.F.',
'Ź.G.',
'Ź.H.',
'Ź.I.',
'Ź.J.',
'Ź.K.',
'Ź.L.',
'Ź.M.',
'Ź.N.',
'Ź.O.',
'Ź.P.',
'Ź.R.',
'Ź.S.',
'Ź.T.',
'Ź.U.',
'Ź.W.',
'Ź.Y.',
'Ź.Z.',
'Ź.Ó.',
'Ź.Ą.',
'Ź.Ć.',
'Ź.Ę.',
'Ź.Ł.',
'Ź.Ń.',
'Ź.Ś.',
'Ź.Ź.',
'Ź.Ż.',
'Ż.A.',
'Ż.B.',
'Ż.C.',
'Ż.D.',
'Ż.E.',
'Ż.F.',
'Ż.G.',
'Ż.H.',
'Ż.I.',
'Ż.J.',
'Ż.K.',
'Ż.L.',
'Ż.M.',
'Ż.N.',
'Ż.O.',
'Ż.P.',
'Ż.R.',
'Ż.S.',
'Ż.T.',
'Ż.U.',
'Ż.W.',
'Ż.Y.',
'Ż.Z.',
'Ż.Ó.',
'Ż.Ą.',
'Ż.Ć.',
'Ż.Ę.',
'Ż.Ł.',
'Ż.Ń.',
'Ż.Ś.',
'Ż.Ź.',
'Ż.Ż.',
'ż.',
'żarg.',
'żart.',
'żyd.',
'żyw.']
