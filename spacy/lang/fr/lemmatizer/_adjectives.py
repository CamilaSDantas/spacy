from __future__ import unicode_literals
ADJECTIVES = set("""
 abaissant abaiss� abandonn� abasourdi abasourdissant abattu abc�dant aberrant
 abject abjurant aboli abondant abonn� abord� abouti aboutissant about�
 abricot� abrit� abrouti abrupt abruti abrutissant abruzzain absent absolu
 absorb� abstinent abstrait abyssin ab�tardi ab�tissant ab�mant ab�m� acarpell�
 accabl� accalmin� accaparant accastillant accentu� acceptant accept� accident�
 accol� accombant accommodant accommod� accompagn� accompli accord� accorn�
 accoud� accoupl� accoutum� accrescent accroch� accru accr�ditant accr�dit�
 accueillant accumul� accus� acc�l�r� acescent achaland� acharn� achev�
 acidul� aci�r� acotyl� acquitt� activ� acumin� acutangul� acutifoli� acutilob�
 adapt� additionn� additiv� adextr� adh�rent adimensionn� adir� adjacent
 adjoint adjug� adjuvant administr� admirant adn� adolescent adoptant adopt�
 adoss� adouci adoucissant adress� adroit adscrit adsorbant adult�rin ad�quat
 affaibli affaiblissant affair� affam� affectionn� affect� affermi affid�
 affil� affin affligeant affluent affolant affol� affranchi affriolant affront�
 aff�t� aff�t� afghan africain agaillardi agatin agatis� aga�ant agglom�rant
 agglutinant agglutin� aggravant agissant agitant agit� agmin� agnat agonisant
 agraf� agrandi agress� agrippant agr�g� agr�� aguichant ahanant ahuri
 aigrett� aigri aigrissant aiguillet� aiguis� ail� aimant aimant� aim� ajourn�
 ajust� alabastrin alambiqu� alangui alanguissant alarmant alarm� albugin�
 alcalescent alcalifiant alcalin alcalinisant alcoolis� aldin alexandrin alezan
 aligot� aliz� ali�nant ali�n� alkylant allaitant allant allemand allergisant
 alliciant alli� allong� allumant allum� allur� all�chant all�geant all�g�
 alphabloquant alphastimulant alphonsin alpin alternant alternifoli�
 alt�rant alt�r� alucit� alvin alv�ol� al�s� amaigri amaigrissant amalgamant
 amaril ambiant ambisexu� ambivalent ambulant ami amiantac� amiantin amid�
 amin� ammoniac� ammoniaqu� ammoni� amnistiant amnisti� amn�siant amoindrissant
 amorti amplifiant amplifi� ampli� ampoul� amput� amusant amus� amylac�
 am�ricain am�risant anabolisant analg�siant anamorphos� anarchisant anastigmat
 anavirulent ancorn� andin andorran anergisant anesth�siant angevin anglican
 angoissant angoiss� angustifoli� angustipenn� anim� anis� ankylosant ankylos�
 anobli anoblissant anodin anovulant ans� ans�rin antenn� anthropis�
 antialcalin antiallemand antiamaril antiautoadjoint antibrouill�
 anticipant anticip� anticoagulant anticontaminant anticonvulsivant
 antid�capant antid�flagrant antid�rapant antid�tonant antifeutrant
 antigivrant antiglissant antiliant antimoni� antim�th�moglobinisant antinatal
 antiodorant antioxydant antiperspirant antiquisant antirassissant
 antir�fl�chissant antir�publicain antir�sonant antir�sonnant antisym�tris�
 antivieillissant anti�m�tisant ant�c�dent ant�natal ant�pos� ant�rieur
 ant�rosup�rieur an�miant an�mi� ao�t� apaisant apeur� apicalis� aplati apocop�
 apparent apparent� appari� appartenant appaum� appelant appel� appendicul�
 appoint� appos� apprivois� approchant approch� approfondi appropri� approuv�
 appr�t� appuy� app�tissant ap�rianth� aquarell� aquitain arabisant araucan
 arboris� arbor� arcel� archa�sant archiconnu archidioc�sain architectur�
 ardent ardois� ardu argentin argent� argilac� arill� armoricain arm�
 arp�g� arqu� arrangeant arrivant arriv� arrogant arrondi arros� arr�t� ars�ni�
 articul� ar�nac� ar�ol� ar�tin ascendant ascospor� asexu� asin asphyxiant
 aspirant aspir� assaillant assainissant assaisonn� assassin assassinant
 asservissant assidu assimil� assistant assist� assi�geant assi�g� associ�
 assommant assonanc� assonant assorti assoupi assoupissant assouplissant
 assujetti assujettissant assur� ass�chant astreignant astringent atlo�d�
 atonal atrophiant atrophi� attachant attaquant attard� atteint attenant
 attendu attentionn� atterrant attest� attirant attitr� attrayant attristant
 at�lectasi� auricul� auscitain austral authentifiant autoadjoint autoagrippant
 autoancr� autobronzant autocentr� autocoh�rent autocollant autocommand�
 autocontraint autoconvergent autocopiant autoflagellant autofondant autoguid�
 autolubrifiant autolustrant autol�gitimant autol�gitim� automodifiant
 autonettoyant autoportant autoproduit autopropuls� autorepassant autoris�
 autosuffisant autotrempant auvergnat avachi avalant aval� avanc� avari�
 aventurin� aventur� avenu averti aveuglant avianis� avili avilissant avin�
 aviv� avoisinant avou� av�r� azimut� azot� azur� az�ri a�ronaval a�roport�
 a�r� a�n� babillard badaud badg� badin baha� bahre�ni bai baillonn� baissant
 balafr� balanc� balbutiant balein� ballant ballonis� ballonn� ballottant
 balzan bambochard banal banalis� bancal bandant band� bangladeshi banlieusard
 bantou baraqu� barbant barbarisant barbel� barbichu barbifiant barbu bard�
 baroquisant barr� baryt� basan� basculant bascul� basedowifiant basedowifi�
 bastill� bastionn� bataill� batifolant battant battu bavard becqu� bedonnant
 bellifontain bellig�rant beno�t benzol� benzo�n� ber�ant beurr� biacumin�
 bicarbonat� bicarr� bicomponent bicompos� biconstitu� bicontinu bicornu
 bidonnant bienfaisant biens�ant bienveillant bigarr� bigot bigourdan big�min�
 bili� billet� bilob� bimacul� binoclard biod�gradant bioluminescent biorient�
 biparti bipectin� bipinn� bipolaris� bip�dicul� biram� birman bir�fringent
 biscuit� bisexu� bismuth� bisontin bispiral� bissexu� bisublim� bis�ri�
 bitern� bivalent bivitellin bivoltin blafard blanchissant blanchoyant blas�
 bless� bleu bleuissant bleut� blind� blond blondin blondissant blondoyant
 blousant bl�mant bl�missant bodybuild� bois� boitillant bomb� bonard
 bond� bonifi� bonnard borain bordant borin born� bor� bossag� bossu bot
 boucl� boudin� bouffant bouffi bouillant bouilli bouillonnant boulant boulet�
 bouquet� bourdonnant bourdonn� bourgeonnant bourrant bourrel� bourru bourr�
 boutonn� bovin bracel� bradycardisant braillard branchu branch� branlant
 bressan bretess� bretonnant brevet� briard bridg� brid� brillant brillant�
 bringueballant brinquebalant brinqueballant briochin brioch� brisant bris�
 broch� brom� bronzant bronz� brouill� broutant bruissant brun brunissant brut
 br�vistyl� br�lant br�l� budget� burel� burin� bursod�pendant busqu� bus�
 butyrac� but� byzantin b�tard b�ti b�t� b�ant b�at b�douin b�gayant b�nard
 b�n�dictin b�quetant b�quillard b�tonn� b�lant b�tabloquant b�tifiant b�m�
 cabochard cabotin cabriolant cabr� cacaot� cachectisant cachemiri cach�
 cadjin cadmi� caducifoli� cafard cagnard cagot cagoul� cahotant caillout�
 calcicord� calcifi� calcul� calmant calotin cal� camard cambrousard cambr�
 camisard campagnard camphr� camp� cam� canalicul� canin cannel� cann� cantalou
 canulant can� caoutchout� capitolin capitulant capitulard capit� capricant
 capsul� captivant capuchonn� caquetant carabin� caracolant caract�ris�
 carbonat� carbon� carburant carbur� cardiocutan� card� carenc� caressant
 carillonnant carillonn� cari� carmin� carn� carolin caroncul� carp� carr�
 car�n� casqu� cassant cass� castelroussin castillan catalan catastroph�
 cat�goris� caud� caulescent causal causant cavalcadant celtisant cendr� cens�
 centram�ricain centr� cercl� cerdagnol cerdan cern� certain certifi� cervel�
 chafouin chagrin chagrinant chagrin� chaloup� chamois� chamoniard chancelant
 chantant chan�ard chapeaut� chap� charan�onn� charg� charmant charnu charpent�
 charri� chartrain chassant chas� chatoyant chaud chauffant chaussant chauvin
 chenill� chenu chevalin chevauchant chevelu chevel� chevill� chevronn�
 chiant chicard chiffonn� chiffr� chimioluminescent chimior�sistant chin�
 chi� chlamyd� chleuh chlorurant chlorur� chlor� chocolat� choisi chok�
 choral chronod�pendant chrys�l�phantin chuintant chypr� ch�tain ch�latant
 ch�m� cibl� cicatrisant cili� cinglant cingl� cintr� circin� circonspect
 circonvoisin circulant circumtemp�r� cir� cisalpin cisjuran cispadan citadin
 citronn� cit�rieur civil civilis� clabotant clair claironnant clairsem�
 clandestin clapotant claquant clarifiant clarin� classicisant claudicant
 clavel� clignotant climatis� clinquant cliquetant cliss� clivant cloisonn�
 cloqu� clout� clo�tr� cl�ment cl�mentin coagulant coalescent coalis� coassoci�
 coccin� cocu codant codirigeant codominant cod� cod�lirant cod�tenu coexistant
 cogn� coh�rent coiffant coiff� coinch� cok�fiant colicitant colitigant
 collant collodionn� coll� colmatant colombin colonis� colorant color�
 combattant combinant combinard combin� comburant comit� commandant commen�ant
 commun communard communiant communicant communiqu� communisant compact
 compar� compass� compatissant compens� complaisant complexant compliqu�
 composant compos� comprim� compromettant comput�ris� comp�tent comtadin conard
 concertant concert� conciliant concluant concomitant concordant concourant
 concupiscent concurrent conc�dant condamn� condensant condens� condescendant
 conditionn� condupliqu� confiant confident confin� confit confondant conf�d�r�
 congru congruent conjoint conjugant conjugu� connaissant connard connivent
 conn� conquassant conqu�rant consacrant consacr� consanguin conscient conscrit
 conserv� consistant consolant consolid� consomm� consonant constant constell�
 constipant constip� constituant constitu� constringent consultant cons�quent
 containeuris� contaminant contemporain content contenu contestant continent
 continu contondant contourn� contractant contraignant contraint contrapos�
 contrari� contrastant contrast� contravariant contrecoll� contredisant
 contrefait contrevariant contrevenant contrit controuv� controvers� contr�l�
 convaincu convalescent conventionn� convenu convergent converti convolut�
 convulsivant convuls� con�u cooccupant cooccurrent coop�rant coordin�
 coordonn� copartageant coparticipant coquill� coquin coraill� corallin
 cord� cornard cornicul� cornu corn� corpulent correct correspondant corrig�
 corrodant corrompu corr�l� corticod�pendant corticor�sistant cortison�
 cor�f�rent cossard cossu costaud costul� costum� cotisant couard couchant
 coulant coulissant couliss� coupant couperos� coupl� coup� courant courbatu
 couronnant couronn� court courtaud courtisan couru cousu coutur� couvert
 covalent covariant co�ncident co�tant crachotant crach� cramoisi cramponnant
 craquel� cravachant crawl� crevant crevard crev� criant criard criblant cribl�
 crispant cristallin cristallisant cristallis� crochu croisett� croiset�
 croissant� crois� croll� croquant cross� crott� croulant croupi croupissant
 croyant cru crucifi� cruent� crustac� cryodess�ch� cryopr�cipit� cr�mant
 cr�pi cr�pitant cr�pu cr�tac� cr�tin cr�tinisant cr�� cr�pel� cr�t� cubain
 cuirass� cuisant cuisin� cuit cuivr� culminant culott� culpabilisant cultiv�
 cuscut� cutan� cyanos� c�bl� c�lin c�dant c�l�brant c�rul� c�rus� c�venol
 damass� damn� dandinant dansant demeur� demi dentel� denticul� dentu dent�
 dessal� dessiccant dessillant dessin� dessoud� dess�chant deut�r� diad�m�
 diamant� diapr� diastas� diazot� dicarbonyl� dichlor� diffamant diffam�
 diffractant diffringent diffusant diff�renci� diff�rent diff�r� difluor�
 diiod� dilatant dilat� diligent dilob� diluant dimensionn� dimidi� dimid�
 diminu� dioc�sain diphas� dipl�mant dipl�m� direct dirigeant dirig� dirimant
 disciplin� discontinu discord discordant discriminant discut� disert disgraci�
 disloqu� disod� disparu dispersant dispers� dispos� disproportionn� disput�
 dissimul� dissip� dissociant dissoci� dissolu dissolvant dissonant diss�min�
 distant distinct distingu� distrait distrayant distribu� disubstitu� disulfon�
 divagant divaguant divalent divergent divertissant divin divorc� dja�n
 dodu dogmatisant dolent domicili� dominant dominicain donjonn� donnant donn�
 dormant dorsalisant dor� douci dou� drageonnant drag�ifi� drainant dramatisant
 drap� dreyfusard drogu� droit dru drupac� dual ductod�pendant dulcifiant dur
 duvet� dynamisant dynamit� dyspn�isant dystrophiant d�amin� d�barqu� d�bauch�
 d�bilitant d�bloquant d�bordant d�bord� d�bouchant d�bourgeois� d�boussol�
 d�brid� d�brouillard d�broussaillant d�brouss� d�butant d�cadent d�caf�in�
 d�calant d�calcifiant d�calvant d�capant d�capit� d�carburant d�cati d�cav�
 d�cevant d�chagrin� d�charn� d�cha�nant d�cha�n� d�chevel� d�chiquet�
 d�chir� d�chlorur� d�chu d�cidu d�cidu� d�cid� d�clar� d�class� d�clenchant
 d�coiffant d�collet� d�colorant d�color� d�compens� d�compl�ment� d�compl�t�
 d�concertant d�conditionn� d�confit d�congestionnant d�connant d�consid�r�
 d�contractant d�contracturant d�contract� d�cortiqu� d�cor� d�coupl� d�coup�
 d�cousu d�couvert d�crispant d�crochant d�croissant d�cr�pi d�cr�pit d�cuman
 d�cuss� d�c�r�br� d�dor� d�faillant d�fait d�fanant d�fatigant d�favoris�
 d�ferlant d�ferl� d�fiant d�ficient d�fig� d�filant d�fini d�flagrant d�fleuri
 d�fl�chi d�foliant d�fonc� d�formant d�franchi d�fra�chi d�frisant d�froqu�
 d�f�ch� d�f�cant d�f�rent d�gag� d�gingand� d�givrant d�glutin� d�gonfl�
 d�gourdi d�gouttant d�go�tant d�go�t� d�gradant d�grad� d�graissant d�griff�
 d�guis� d�g�n�rescent d�g�n�r� d�hanch� d�hiscent d�jet� d�labrant d�labr�
 d�lassant d�lav� d�lay� d�lib�rant d�lib�r� d�licat d�linquant d�liquescent
 d�litescent d�li� d�loqu� d�lur� d�l�gu� d�magn�tisant d�maquillant d�maqu�
 d�ment d�merdard d�mesur� d�mix� d�mod� d�montant d�mont� d�moralisant
 d�motivant d�motiv� d�mystifiant d�my�linisant d�my�lisant d�m�lant d�naturant
 d�nigrant d�nitrant d�nitrifiant d�nomm� d�nud� d�nutri d�nu� d�odorant
 d�papill� d�pareill� d�pass� d�paysant d�pays� d�peign� d�penaill� d�pendant
 d�peupl� d�phas� d�pit� d�plac� d�plaisant d�plaquett� d�plasmatis� d�pliant
 d�plumant d�plum� d�pl�t� d�poitraill� d�polarisant d�poli d�politisant
 d�ponent d�port� d�posant d�pos� d�pouill� d�pourvu d�poussi�rant d�pravant
 d�primant d�prim� d�pr�d� d�p�rissant d�p�tainis� d�racinant d�racin�
 d�rang� d�rapant d�restaur� d�rivant d�riv� d�rob� d�rogeant d�roulant
 d�r�alisant d�r�gl� d�sabus� d�saccord� d�sadapt� d�saffectiv� d�saffect�
 d�saisonnalis� d�salign� d�sali�nant d�salt�rant d�saluminis� d�sambigu�s�
 d�sargent� d�sarmant d�sar�onnant d�sassorti d�satomis� d�saturant d�sax�
 d�sempar� d�senchant� d�sensibilisant d�sert d�sesp�rant d�sesp�r�
 d�sherbant d�shonorant d�shumanisant d�shydratant d�shydrat� d�shydrog�nant
 d�siconis� d�sillusionnant d�sincarn� d�sincrustant d�sinfectant
 d�sint�ress� d�sirant d�sobligeant d�soblit�rant d�sob�i d�sob�issant
 d�sodorisant d�sod� d�soeuvr� d�solant d�sol� d�sopilant d�sordonn�
 d�sorient� d�soss� d�soxydant d�soxyg�nant d�stabilisant d�stressant
 d�suni d�s�quilibrant d�s�quilibr� d�tachant d�tach� d�tartrant d�tendu d�tenu
 d�terminant d�termin� d�terr� d�tonant d�tonnant d�tourn� d�traqu� d�t�rior�
 d�velopp� d�verbalisant d�vergond� d�vers� d�vert�br� d�viant d�viss�
 d�vois� d�volu d�vorant d�vot d�vou� d�voy� d�watt� d��u effac� effarant
 effarouch� effar� effervescent efficient effiloch� effil� efflanqu�
 effluent effondr� effrang� effrayant effray� effront� effr�n� eff�min�
 emballant embarrassant embarrass� embellissant embiell� embouch� embouti
 embrassant embrass� embrouillant embrouill� embroussaill� embruin� embryonn�
 embusqu� emb�tant emmerdant emmiellant emmi�lant emmott� empaill� empanach�
 empenn� emperl� empes� empi�tant emplum� empoignant empoisonnant emport�
 empress� emprunt� emp�t� emp�ch� emp�tr� encaissant encaiss� encalmin�
 encapsulant encapsul� encartouch� encastr� encerclant enchant� enchifren�
 encloisonn� encloqu� encombrant encombr� encorn� encourageant encrou�
 encro�t� encul� endent� endiabl� endiamant� endimanch� endog� endolori
 endormi endurant endurci enfantin enfarin� enflamm� enfl� enfoir� enfonc�
 engageant engag� engainant englant� englobant engoul� engourdi engourdissant
 engraissant engrav� engrenant engren� engr�l� enguich� enhard� enivrant
 enjamb� enjou� enkikinant enkyst� enlaidissant enla�ant enlev� enneig� ennemi
 ennuyant ennuy� enquiquinant enracinant enrageant enrag� enregistrant enrhum�
 enrichissant enrob� enseignant enseign� ensell� ensoleill� ensommeill�
 ensoutan� ensuqu� entartr� entendu enterr� enthousiasmant entour� entrant
 entra�nant entrecoup� entrecrois� entrelac� entrelard� entreprenant entresol�
 entrouvert enturbann� ent� ent�tant ent�t� envahissant envap� enveloppant
 envenim� envin� environnant envi� envoy� envo�tant ergot� errant erron�
 escarp� espac� espagnol espagnolisant esquintant esquint� esseul� essorant
 estomaqu� estomp� estropi� estudiantin euphorisant euph�mis� eurafricain
 exacerb� exact exag�r� exalbumin� exaltant exalt� exasp�rant excellent
 except� excitant excit� exclu excluant excommuni� excru exc�dant exempt
 exerc� exer�ant exfoliant exhalant exhilarant exigeant exil� exinscrit
 exond� exorbitant exorbit� exospor� exostosant expans� expatri� expectant
 expert expirant exploitant exploit� expos� expropriant expropri� expuls�
 exp�riment� extasi� extemporan� extradoss� extrafort extraplat extrap�riost�
 extraverti extroverti ext�nuant ext�rieur exub�rant exultant facilitant
 faiblissant faignant failli faill� fain�ant faisand� faisant fait falot falqu�
 fan� faraud farci fard� farfelu farinac� fascicul� fascinant fascisant fasci�
 fassi fastigi� fat fatal fatigant fatigu� fauch� favorisant fa�onn� fa�enc�
 feint fendant fendill� fendu fenestr� fenian fen�tr� fermant fermentant
 ferritisant ferruginis� ferr� fertilisant fervent fescennin fessu festal
 festival feuillag� feuillet� feuillu feuill� feutrant feutr� fianc� fibrill�
 ficel� fichant fichu fieff� figulin figur� fig� filant filet� filoguid�
 fil� fimbri� fin final finalis� finaud fini finissant fi�rot flabell� flagell�
 flagrant flamand flambant flamboyant flamb� flamingant flamm� flanchard
 flanquant flapi flatulent flavescent flemmard fleurdelis� fleuri fleurissant
 flippant florentin florissant flottant flottard flott� flou fluctuant fluent
 fluidifi� fluocompact fluorescent fluor� flush� fl�chissant fl�ch� fl�mard
 fl�trissant fl�t� foisonnant foliac� foli� follicul� fol�trant fonc� fondant
 fond� forain foramin� forcen� forc� forfait forg� formalis� format� formicant
 form� fort fortifiant fortrait fortuit fortun� fossilis� foudroyant fouettard
 fouill� fouinard foulant fourbu fourchet� fourchu fourch� fourmillant fourni
 foutral foutu fox� fracassant fractal fractionn� fragilisant fragrant
 franchouillard francisant franciscain franciscanisant frangeant frappant
 fratris� frelat� frett� friand frigorifi� fringant fringu� friqu� frisant
 frisott� frissonnant fris� frit froid froissant fronc� frondescent frottant
 froussard fructifiant fruit� frumentac� frustrant frustr� frutescent
 fr�quent fr�quent� fr�tillant fugu� fulgurant fulminant fumant fum� furfurac�
 furibond fusant fusel� futur fut� fuyant fuyard f�ch� f�bricitant f�cond
 f�culent f�d�r� f�lin f�minin f�minisant f�rin f�ri� f�ru f�l� gabalitain
 gag� gai gaillard galant galb� gallican gallinac� galloisant galonn� galopant
 ganglionn� gangren� gangu� gantel� garant garanti gard� garni garnissant
 gauchisant gazonnant gazonn� gazouillant gaz� ga�l geignard gel� genouill�
 germanisant germ� gestant gesticulant gibelin gigotant gigott� gigot� girond
 gironn� gisant gitan givrant givr� glabrescent glacial glac� glandouillant
 glapissant gla�ant glissant gliss� globalisant glom�rul� glottalis�
 gloussant gloutonnant gluant glucos� glycosyl� glycuroconjugu� godill�
 goguenard gommant gomm� gom�nol� gondolant gonflant gonfl� gouleyant goulu
 gourmand gourm� goussaut gouvernant gouvern� go�tu go�t� gradu� grad� graffit�
 grand grandiloquent grandissant granit� granoclass� granul� graphitisant
 grasseyant gratifiant gratin� gratuit gravant gravitant greffant grelottant
 grenel� grenu gren� griffu grignard grillet� grill� grima�ant grimpant
 grin�ant gripp� grisant grisonnant grivel� grondant grossissant grouillant
 gr�sillant gueulard guignard guilloch� guillotin� guind� guivr� gu�ri g�t�
 g�latinisant g�latin� g�lifiant g�lifi� g�min� g�missant g�nicul� g�n�ralisant
 g�om�trisant g�rant g�nant g�n� g�t� habilitant habilit� habill� habitu�
 hachur� hach� hagard halbren� haletant halin hallucinant hallucin� hanch�
 hant� harassant harass� harcelant harcel� hardi harp� hast� haut hautain
 hennissant heptaperfor� herbac� herboris� herbu hermin� herni� hers� heurt�
 hibernant hilarant hindou hircin hispanisant historicisant historisant
 hivernant hi�rosolymitain holocristallin hominis� homog�n�is� homoprothall�
 homoxyl� honorant honor� hord�ac� hormonod�priv� horodat� horrifiant
 hottentot hoy� huguenot huitard humain humectant humiliant humili� hupp�
 hutu hyalin hydratant hydrocarbon� hydrochlor� hydrocut� hydrog�nant hydrog�n�
 hydrosalin hydrosod� hydroxyl� hyperalcalin hypercalcifiant hypercalc�miant
 hypercoagulant hypercommunicant hypercorrect hyperfin hyperfractionn�
 hyperis� hyperlordos� hypermotiv� hyperphosphat�miant hyperplan hypersomnolent
 hypertrophiant hypertrophi� hypervascularis� hypnotisant hypoalg�siant
 hypocalc�miant hypocarpog� hypocholest�rol�miant hypocotyl� hypoglyc�miant
 hypolipid�miant hypophosphat�miant hyposod� hypotendu hypotonisant
 hypovirulent hypox�miant h�l� h�bra�sant h�b�t� h�licospor� h�liomarin
 h�litransport� h�micord� h�micristallin h�mipl�gi� h�modialys� h�mopigment�
 h�patostri� h�rissant h�riss� h�sitant h�t�roprothall� h�t�rospor� h�t�rostyl�
 identifi� idiot idiotifiant id�al ignifugeant ignorant ignorantin ignor� ign�
 illimit� illumin� imaginant imagin� imag� imbriqu� imbr�l� imbu imit� immacul�
 immerg� immigrant immigr� imminent immod�r� immortalisant immotiv� immun
 immunocomp�tent immunod�primant immunod�prim� immunostimulant immunosupprim�
 imm�diat imm�rit� impair impalud� imparfait imparidigit� imparipenn� impatient
 impay� impens� imperfor� impermanent imperm�abilisant impertinent implorant
 important importun import� imposant impos� impotent impressionnant imprimant
 impromptu impromulgu� improuv� imprudent impr�voyant impr�vu impudent
 impuni impur imp�nitent imp�tiginis� inabord� inabouti inabrit� inabrog�
 inaccept� inaccompli inaccoutum� inachev� inactiv� inadapt� inad�quat
 inaguerri inali�n� inalt�r� inanalys� inanim� inaniti� inapais� inaper�u
 inapparent� inappliqu� inapprivois� inappropri� inappr�ci� inappr�t�
 inarticul� inassimil� inassorti inassouvi inassujetti inattaqu� inattendu
 inavou� incandescent incapacitant incarnadin incarnat incarn� incendi�
 incessant inchang� inch�ti� incident incident� incitant incivil inclass�
 inclin� incl�ment incoh�rent incombant incomitant incommodant incommuniqu�
 incomp�tent inconditionn� inconfess� incongru incongruent inconnu inconquis
 inconsid�r� inconsistant inconsol� inconsomm� inconstant incons�quent
 incontest� incontinent incontr�l� inconvenant incoordonn� incorporant
 incorrect incorrig� incriminant incrimin� incritiqu� incroyant incrustant
 incr�� incubant inculp� incultiv� incurv� indevin� indiff�renci� indiff�rent
 indirect indirig� indisciplin� indiscrimin� indiscut� indispos� indistinct
 indolent indompt� indou indu induit indulgent indupliqu� indur�
 ind�brouill� ind�cent ind�chiffr� ind�cidu� ind�fini ind�finis� ind�frich�
 ind�lib�r� ind�licat ind�montr� ind�m�l� ind�pass� ind�pendant ind�pens�
 ind�termin� ineffectu� inefficient inemploy� inentam� inentendu inesp�r�
 inexauc� inexerc� inexistant inexpert inexpi� inexpliqu� inexploit� inexplor�
 inexprim� inexp�riment� inex�cut� infamant infantilisant infarci infatu�
 infectant infect� infestant infest� infichu infiltrant infini inflamm�
 infl�chi infond� informant informul� infortun� infoutu infr�quent� infus�
 inf�od� inf�rieur inf�rovari� ingrat ing�nu inhabit� inhalant inhibant inhib�
 inh�rent inimit� inintelligent ininterrompu inint�ressant initi� inject�
 innervant innocent innomin� innomm� innom� innovant inn� inobserv� inoccup�
 inond� inopin� inopportun inop�rant inorganis� inoubli� inou� inqui�tant
 insatisfait insatur� inscrit insens� inserment� insignifiant insinuant
 insolent insond� insonorisant insonoris� insouciant insoup�onn� inspirant
 insp�cifi� install� instant instantan� instructur� instruit insubordonn�
 insulinod�pendant insulinor�sistant insultant insult� insurg� ins�curisant
 intelligent intemp�rant intentionn� interalli� interam�ricain intercept�
 intercristallin intercurrent interdigit� interdioc�sain interdit
 interfac� interf�cond interf�rent interloqu� intermittent interm�di� interpol�
 interpr�tant intersect� intersexu� interstratifi� interurbain intervenant
 intestin intimidant intol�rant intoxicant intoxiqu� intramontagnard
 intrigant introduit introject� introverti intumescent int�grant int�grifoli�
 int�ress� int�rieur inusit� inutilis� invaincu invalidant invariant invendu
 inverti invert�br� inviol� invitant involucr� involut� inv�rifi� inv�t�r�
 in�clairci in�cout� in�dit in�gal� in�l�gant in�prouv� in�puis� in�quivalent
 iodoform� iodur� iodyl� iod� ionisant iridescent iridi� iris� ironisant
 irraisonn� irrassasi� irritant irrit� irr�alis� irr�fl�chi irr�fut� irr�mun�r�
 irr�solu irr�v�l� islamisant isohalin isolant isol� isospor� issant issu
 itin�rant ivoirin jacent jacobin jaillissant jama�cain jama�quain jamb�
 japonn� jardin� jarret� jarr� jasp� jauni jaunissant javel� ja�n jobard joint
 joli joufflu jouissant jovial jubilant juch� juda�sant jumel� juponn� jur�
 juxtaposant juxtapos� kalmouk kanak kazakh kenyan kosovar k�ratinis� labi�
 lacini� lactant lactescent lactos� lact� lai laid lain� lait� lambin lambriss�
 lamifi� lamin� lampant lampass� lam� lancinant lanc� lanc�ol� languissant
 lapon laqu� lardac� larmoyant larv� laryng� lassant latent latifoli� latin
 latt� lat�ralis� laur� laur�at lavant lav� la�cisant lent lenticul� letton
 lettr� leucop�niant leucospor� leucostimulant levant levantin levrett� lev�
 liant libertin lib�r� licenci� lich�nifi� liftant lift� ligatur� lignifi�
 ligul� lilac� limac� limitant limougeaud limousin lionn� lippu liqu�fiant
 lithin� lithi� lit� li� li�g� lobul� lob� localis� locul� lointain lombard
 lorrain lor� losang� loti louchant loup� lourd lourdaud lubrifiant luisant
 lunett� lunul� lun� lusitain lustr� luth� lutin lut�inisant lut�ostimulant
 lyophilis� lyr� l�ch� l�nifiant l�onard l�onin l�opard� l�zard� maboul macl�
 madr� mafflu maghr�bin magn�si� magn�tisant magr�bin magyar mahom�tan maillant
 majeur majorant majorquin maladroit malais� malavis� malb�ti malentendant
 malform� malintentionn� malnutri malodorant malotru malouin malpoli malsain
 mals�ant maltraitant malt� malveillant malvoyant mal�fici� mamelonn� mamelu
 manchot mandarin mandchou mani�r� mannit� manoeuvrant manquant manqu� mansard�
 mantouan manuscrit manu�lin maori mara�chin marbr� marcescent marchand
 marial marin mariol mari� marmottant marocain maronnant marquant marquet�
 marqu�san marrant marri martel� martyr marxisant masculin masculinisant
 masqu� massacrant massant mass� mass�t�rin mat matelass� mati mat�rialis�
 maugrabin maugrebin meilleur melonn� membran� membru menac� menant mena�ant
 menthol� menu merdoyant mesquin messin mesur� meublant mexicain micac�
 microencapsul� microgrenu micropliss� micro�clat� miell� mignard migrant
 militant millerand� millim�tr� mill�sim� mineur minidos� minorant minorquin
 miracul� miraill� miraud mirobolant miroitant miroit� mir� mitig� mitr� mit�
 mobili�ris� mochard modelant modifiant modulant modul� mod�lisant mod�r�
 mogol moir� moisi molet� molletonn� mollissant momentan� momifi� mondain mond�
 monili� monobrom� monochlamyd� monochlor� monocompos� monocontinu
 monofluor� monogramm� monohalog�n� monohydrat� mononucl�� monophas�
 monop�rianth� monor�fringent monospor� monotriphas� monovalent montagnard
 montpelli�rain mont� mont�n�grin monument� moralisant mordant mordicant
 mordu morfal morfondu moribond moricaud mormon mort mortifiant morvandiot
 mosellan motivant motiv� mouchard mouchet� moufl� mouillant mouill� moulant
 moul� mourant moussant moussu moustachu moutonnant moutonn� mouvant mouvement�
 moy� mozambicain mucron� mugissant mulard multiarticul� multidigit�
 multilob� multinucl�� multiperfor� multiprogramm� multir�sistant multis�ri�
 multivalent multivari� multivitamin� multivoltin munificent murin muriqu�
 murrhin musard muscl� musqu� mussipontain musulman mutant mutilant mutin
 myorelaxant myrrh� mystifiant mythifiant my�linisant my�linis� m�tin� m�chant
 m�connu m�content m�cr�ant m�daill� m�dian m�diat m�dicalis� m�disant
 m�fiant m�lang� m�lanostimulant m�ning� m�plat m�prisant m�ritant m�rul�
 m�tallescent m�tallis� m�tam�ris� m�tastas� m�thoxyl� m�thylur�
 m�tropolitain m�t�orisant m�l� m�r m�rissant nabot nacr� nageant nain naissant
 nanti napolitain narcissisant nasard nasillard natal natt� naturalis� naufrag�
 naval navigant navrant nazi nervin nervur� nerv� nettoyant neum� neuralisant
 neurom�ning� neutralisant nickel� nictitant nidifiant nigaud nig�rian
 nippon nitescent nitrant nitrifiant nitros� nitrurant nitr� noir noiraud
 nombrant nombr� nominalis� nomm� nonchalant normalis� normand normodos�
 normotendu norm� notari� nourri nourrissant nou� noy� nu nuag� nuanc� nucl�ol�
 nullard num�rot� nutant nu� n� n�bul� n�cessitant n�crosant n�gligent n�glig�
 n�oform� n�olatin n�onatal n�vrosant n�vros� obligeant oblig� oblit�rant
 obscur observant obsolescent obstin� obstru� obs�dant obs�d� obs�quent
 obtur� ob�i ob�issant ob�r� occitan occupant occup� occurrent ocell� ochrac�
 ocul� odorant odorif�rant oeill� oeuv� offensant offens� officiant offrant
 olivac� ol�ac� ol�fiant ol�ifiant oman ombell� ombiliqu� ombrag� ombr�
 omnipr�sent omniscient ondoyant ondulant ondul� ond� ongl� onguicul� ongul�
 opalescent opalin opercul� opiac� opportun opposant oppositifoli� oppos�
 oppress� opprimant opprim� opsonisant optimalisant optimisant opulent op�rant
 orant ordonn� ordr� oreillard oreill� orf�vr� organis� organochlor�
 organosilici� orientalisant orient� oropharyng� orphelin orthonorm� orti�
 osmi� ossifiant ossifluent ossu ostial ostrac� ostrogot ostrogoth ostr�ac� os�
 ouat� ourl� oursin outill� outrageant outrag� outrecuidant outrepass� outr�
 ouvrag� ouvrant ouvr� ovalis� ovill� ovin ovulant ov� oxycarbon� oxydant
 oxyg�n� ozon� o�di� pacifiant padan padouan pahlavi paillard paillet� pair
 palatin palermitain paliss� pallotin palmatilob� palmatinerv� palmatis�qu�
 palmis�qu� palm� palpitant panach� panafricain panard panicul� paniquant pann�
 pantelant pantouflard pan� papalin papelard papilionac� papillonnant
 papou papyrac� paraffin� paralysant paralys� param�dian parchemin� parent
 parfum� paridigitid� paridigit� parigot paripenn� parlant parl� parmesan
 parsi partag� partant parti participant partisan partousard partouzard
 parvenu par� passant passepoil� passerill� passionnant passionn� pass� pataud
 patelin patelinant patent patent� patient patoisant patriotard pattu patt�
 paum� pav� payant pectin� pehlevi peign� peinard peint pelliculant pellicul�
 peluch� pel� penaud penchant pench� pendant pendu pennatilob� pennatinerv�
 penninerv� penn� pensant pensionn� pentavalent pentu pepton� perchlorat�
 percutant percutan� perdant perdu perfectionn� perfoli� perforant performant
 perfus� perlant perlur� perl� permanent permutant perphospor� perruqu� persan
 persistant personnalis� personnifi� person� persuad� persulfur� pers�cut�
 pertinent perturbant perverti per�ant pesant pestif�r� petiot petit peul
 pharmocod�pendant pharyng� phas� philippin philistin phophoryl� phosphat�
 phosphor� photoinduit photoluminescent photor�sistant photosensibilisant
 ph�nol� ph�notyp� piaffant piaillant piaillard picard picot� pigeonnant
 pignonn� pillard pilonnant pilos�bac� pimpant pinaill� pinchard pinc� pinn�
 pin�ard pion�ant piquant piqu� pisan pistill� pitchoun pivotant pi�g�
 plac� plafonnant plaidant plaignant plain plaisant plan planant plant� plan�
 plasmolys� plastifiant plat plein pleurant pleurard pleurnichard pliant
 pliss� pli� plomb� plongeant plumet� pluriarticul� plurihandicap� plurinucl��
 plurivalent pochard poch� poignant poilant poilu pointill� pointu point�
 poitevin poivr� polarisant polaris� poli polic� politicard polluant
 polycarburant polychlor� polycontamin� polycopi� polycristallin polyd�satur�
 polyhandicap� polyinsatur� polylob� polynitr� polynucl�� polyparasit�
 polysubstitu� polysyphilis� polytransfus� polytraumatis� polyvalent
 polyvoltin pommel� pommet� pompant pomp� ponctu� pond�r� pontifiant pontin
 poplit� poqu� porcelain� porcin porrac� portant portoricain poss�dant poss�d�
 postillonn� postnatal postn�onatal post� post�rieur pos� potel� potenc�
 poupin pourprin pourri pourrissant poursuivant pourtournant poussant pouss�
 pratiquant prenant prescient prescrit pressant pressionn� press� prieur primal
 privil�gi� probant prochain procombant procubain profil� profitant profond
 programm� prohib� projetant prolab� prolif�rant prolong� prompt promu
 prononc� propan� proportionn� proratis� proscrit prostr� protestant protonant
 protub�rant prot�in� provenant provocant provoqu� pro�minent prudent pruin�
 pr�alpin pr�bend� pr�cipitant pr�cipit� pr�cit� pr�compact pr�conscient
 pr�contraint pr�con�u pr�cuit pr�c�dent pr�dess�ch� pr�destin� pr�diffus�
 pr�disposant pr�dominant pr�d�coup� pr�emball� pr�encoll� pr�enregistr�
 pr�fabriqu� pr�fix� pr�formant pr�fragment� pr�f�rant pr�f�r� pr�gnant
 pr�latin pr�matur� pr�muni pr�m�dit� pr�nasalis� pr�natal pr�nomm� pr�oblit�r�
 pr�occup� pr�parant pr�pay� pr�pond�rant pr�positionn� pr�programm� pr�roman
 pr�sal� pr�sanctifi� pr�sent pr�signifi� pr�sum� pr�suppos� pr�tendu
 pr�trait� pr�valant pr�valent pr�venant pr�venu pr�voyant pr�vu pr��marg�
 pr��tabli pr�t pr�tant pr�t� psychiatris� psychostimulant psycho�nergisant
 puant pubescent pudibond puissant pulsant puls� pultac� pulv�rulent puni pur
 puritain purpurac� purpurin purulent pustul� putrescent putr�fi� pu�ril pu�n�
 pyramidant pyramid� pyrazol� pyroxyl� p�li p�lissant p�dant p�dantisant
 p�diculos� p�dicul� p�doncul� p�kin� p�lori� p�nalisant p�nard p�nicill�
 p�n�trant p�n�tr� p�quenaud p�rennant p�rianth� p�rigourdin p�rim� p�rinatal
 p�r�grin p�r�grinant p�r�qu� p�tant p�taradant p�tillant p�tiol� p�tochard
 p�trifiant p�trifi� p�tr� p�tulant p�chant qatari quadrifoli� quadrig�min�
 quadriparti quadrivalent quadrupl�t� qualifiant qualifi� quantifi� quart
 questionn� quiescent quinaud quint quintessenci� quintilob� quin� qu�rulent
 rabattable rabattant rabattu rabougri raccourci racorni rac� radiant radicant
 radiodiffus� radiolipiodol� radior�sistant radiotransparent radiot�l�vis�
 raffermissant raffin� rafra�chi rafra�chissant rageant ragot rago�tant
 raisonn� rajeunissant ralli� ramass� ramenard ramifi� ramolli ramollissant
 ram� ranci rang� rapatri� rapiat raplati rappel� rapport� rapproch� rarescent
 rasant rassasiant rassasi� rassembl� rassurant rassur� rass�r�nant ras�
 ratiocinant rationalis� rat� ravageant ravag� raval� ravi ravigotant ravissant
 ray� rebattu rebondi rebondissant rebutant recal� recarburant recercel�
 rechign� recombinant recommand� reconnaissant reconnu reconstituant recoquet�
 recroiset� recroquevill� recru recrudescent recrutant rectifiant recueilli
 redent� redondant redoublant redoubl� refait refoulant refoul� refroidissant
 regardant regrossi reint� relaxant relev� reluisant rel�ch� rel�gu� remarqu�
 rempli remuant renaissant rench�ri rendu renferm� renfl� renfonc� renfor�ant
 rengag� renomm� rentrant rentr� rent� renversant renvers� repentant repenti
 report� reposant repos� repoussant repouss� repress� repr�sentant repu
 resarcel� rescap� rescindant resci� respirant resplendissant ressemblant
 ressortissant ressurgi ressuscit� restant restreint restringent resurgi
 retard� retentissant retenu retir� retombant retrait retrait� retrayant
 retrouss� revanchard revigorant revitalisant reviviscent re�u rhinopharyng�
 rhodi� rhumatisant rhum� rh�nan rh�nalpin riant ribaud riboulant ricain
 ricin� rid� rifain rigolard ringard risqu� riverain roidi romagnol romain
 romand romanisant rompu rond rondouillard ronflant rongeant rosac� rossard
 rotac� roublard roucoulant rouergat rougeaud rougeoyant rougi rougissant
 rouleaut� roulott� roul� roumain rouquin rousseauisant routinis� rou� ruban�
 rubicond rub�fiant rudent� rugissant ruin� ruisselant ruminant rupin rurbain
 rus� rutilant rythm� r�bl� r�lant r�p� r�adapt� r�alisant r�calcitrant r�cent
 r�chauffant r�chauff� r�cidivant r�citant r�clamant r�clinant r�clin�
 r�confortant r�curant r�current r�curv� r�cusant r�duit r�entrant r�flectoris�
 r�fl�chissant r�form� r�frig�rant r�frig�r� r�fringent r�fugi� r�f�renc�
 r�gissant r�glant r�gl� r�gnant r�gress� r�g�n�rant r�g�n�r� r�habilit�
 r�it�r� r�joui r�jouissant r�manent r�mittent r�mun�r� r�nitent r�pandu
 r�prouv� r�publicain r�pugnant r�put� r�serv� r�sidant r�sident r�sign�
 r�sin� r�sistant r�solu r�solvant r�sonant r�sonnant r�sorbant r�sorcin�
 r�sum� r�supin� r�surgent r�tabli r�tam� r�ticent r�ticul� r�trofl�chi
 r�tror�fl�chissant r�tr�ci r�uni r�ussi r�verb�rant r�voltant r�volt� r�volu
 r�vulsant r�vuls� r�v�l� r�v�rend r��quilibrant r�v� r�ti sabin saccad�
 saccharin� sacrifi� sacr� safran� sagitt� sahraoui saignant saignotant
 sain saint saisi saisissant saladin salant salari� salicyl� salin salissant
 samaritain samoan sanctifiant sanglant sanglotant sanguin sanguinolent
 sanskrit santalin saoul saoulard saponac� sarrasin satan� satin� satisfaisant
 saturant saturnin satur� saucissonn� sauc� saugrenu saumon� saumur� sautant
 sautill� saut� sauvagin savant savoyard scalant scarifi� scell� sciant
 scl�rosant scl�ros� scoli� scoriac� scorifiant scout script scrobicul�
 second secr�tant semel� semi-fini sempervirent sem� sensibilisant sens� senti
 serein serpentin serr� servant servi seul sexdigit� sexu� sexvalent seyant
 sibyllin sid�rant sifflant sigill� sigl� signal� signifiant silici� silicos�
 simplifi� simultan� simul� sinapis� sinisant siphonn� situ� slavisant
 snobinard socialisant sociologisant sod� soiffard soignant soign� solognot
 somali sommeillant somm� somnolant somnolent sonnant sonn� sorbonnard sortant
 souah�li soudain soudant soud� soufflant souffl� souffrant soufi soulev�
 sourd souriant soussign� soutenu souterrain souverain so�lant so�lard
 spatul� spermagglutinant spermimmobilisant sphac�l� spiral� spirant spiritain
 spl�nectomis� spontan� sporul� spumescent sp�cialis� stabilisant stagnant
 staphylin stationn� stibi� stigmatisant stigmatis� stimulant stipendi� stipit�
 stipul� stratifi� stressant strict strident stridulant stri� structurant
 stup�fait stup�fiant styl� st�nohalin st�nosant st�rilisant st�rilis�
 su suant subalpin subclaquant subconscient subintrant subit subjacent
 sublimant subneutralisant subordonnant subordonn� subrog� subsident subs�quent
 subul� suburbain subventionn� sub�rifi� succenturi� succinct succulent
 sucrant sucr� suc� suffisant suffocant suffragant suicid� suintant suivant
 sulfamidor�sistant sulfamid� sulfat� sulfhydryl� sulfon� sulfurant sulfuris�
 superfin superfini superflu superg�ant superhydratant superordonn� superovari�
 suppliant supplici� suppl�ant supportant suppos� suppurant suppur�
 supradivergent suprahumain sup�rieur surabondant suractiv� surajout� surann�
 surbrillant surcharg� surchauff� surclass� surcompos� surcomprim� surcoupl�
 surd�terminant surd�termin� surd�velopp� surencombr� surexcitant surexcit�
 surfin surfondu surfrapp� surgel� surgi surglac� surhauss� surhumain suri
 surmenant surmen� surmultipli� surmuscl� surneig� suroxyg�n� surperform�
 surplombant surplu� surprenant surpress� surpuissant surr�alisant sursal�
 sursatur� sursilic� surveill� survitamin� survivant survolt� sur�mancip�
 susdit susd�nomm� susmentionn� susnomm� suspect suspendu susrelat� susurrant
 suzerain su�d� swahili swah�li swazi swingant swingu� sylvain sympathisant
 synanth�r� synchronis� syncop� syndiqu� synth�tisant syst�matis� s�ant s�bac�
 s�chant s�curisant s�curis� s�duisant s�gr�gu� s�gr�g� s�lectionn� s�l�ni�
 s�mitisant s�nescent s�par� s�quenc� s�questrant s�rigraphi� s�roconverti
 s�rotonicod�pendant s�tac� s�villan tabou tabouis� tachet� tach� tadjik taill�
 talot� talut� tal� tamil tamisant tamis� tamoul tangent tannant tann� tapant
 tapissant taponn� tap� taquet� taquin tarabiscot� taraudant tarentin tari
 tartr� tar� tass� tatar taup� taurin tavel� teint teintant teint� tellur�
 temp�rant temp�r� tenaillant tenant tendu tentant ternifoli� terraqu�
 terrifiant terrorisant tessell� testac� texan texturant textur� thallospor�
 thermis� thermocollant thermodurci thermofix� thermoform� thermohalin
 thermoluminescent thermopropuls� thermor�manent thermor�sistant thrombop�niant
 thrombos� thymod�pendant th�bain th�ocentr� th�orb� tib�tain tierc� tigr� tig�
 timbr� timor� tintinnabulant tiquet� tirant tir� tisonn� tissu titan� titr�
 tocard toisonn� tol�rant tombal tombant tomb� tonal tondant tondu tonifiant
 tonnant tonsur� tontur� tophac� toquard toqu� torch� tordant tordu torsad�
 tortu torturant toscan totalisant totipotent touchant touffu toulousain
 tourel� tourmentant tourment� tournant tournoyant tourn� tracassant tract�
 traitant tramaill� tranchant tranch� tranquillisant transafricain transalpin
 transandin transcendant transcutan� transfini transfixiant transformant
 transi transloqu� transmutant transpadan transparent transper�ant transpirant
 transpos� transt�v�rin transylvain trapu traumatisant traumatis� travaillant
 traversant travesti tra�ant tra�nant tra�nard treilliss� tremblant tremblotant
 trempant tremp� tressaillant triboluminescent tributant trichin� tricot�
 trident� trifoliol� trifoli� trifurqu� trig�min� trilob� trin trinerv�
 triparti triphas� triphosphat� trisubstitu� triti� tritubercul� triturant
 trivialis� trompettant tronqu� troublant trouillard trouv� trou� truand
 truff� truit� trypsin� tr�buchant tr�fl� tr�mulant tr�pass� tr�pidant
 tuant tubard tubectomis� tubercul� tubul� tub�rac� tub�rifi� tub�ris� tufac�
 tuil� tumescent tum�fi� tuniqu� turbin� turbocompress� turbulent turgescent
 tutsi tu� twist� typ� t�tonnant t�flonis� t�l�phon� t�l�vis� t�norisant
 t�r�brant t�traphas� t�trasubstitu� t�travalent t�tu t�l� ulc�r� ultracibl�
 ultracourt ultrafin ultramontain ult�rieur uncinul� uncin� uni unifiant
 uniformisant unilob� uninucl�� uniovul� unipotent uniram� unir�fringent
 unistratifi� unis�ri� unitegmin� univalent univitellin univoltin urbain
 urgent urticant usag� usant usit� us� utricul� ut�rin ut�rosacr� vacant
 vaccin� vachard vacillant vadrouillant vagabond vagabondant vagin� vagissant
 vain vaincu vair� vald�tain valgisant validant vallonn� valorisant valu�
 valv� vanadi� vanillin� vanill� vanis� vann� vantard variol� varisant vari�
 varv� vasard vascularis� vasostimulant vasouillard vaudou veinard vein�
 velu venaissin venant vendu ventripotent ventrom�dian ventru vent� verdissant
 verget� verglac� vergla�ant verg� verjut� vermicell� vermicul� vermoulant
 verni verniss� verr� versant vers� vert verticill� vert�br� vespertin vexant
 vibrionnant vicariant vicelard vici� vieilli vieillissant vigil vigilant
 vigorisant vil vilain violac� violent violon� vip�rin virevoltant viril
 virulent visigoth vitamin� vitellin vitr� vivant viverrin vivifiant vivotant
 vogoul voil� voisin vois� volant volant� volatil voletant voltigeant volvul�
 vorticell� voulu vouss� voyant vo�t� vrai vrill� vrombissant vu vuln�rant
 vulturin v�cu v�g�tant v�h�ment v�lin v�lomotoris� v�rol� v�sicant v�sicul�
 v�tu wallingant watt� wisigoth youpin zazou zend zigzagant zinzolin zon�
 zoulou z�l� z�zayant �g� �nonnant �bahi �baubi �berlu� �blouissant �bouriffant
 �burnin �burn� �caill� �cartel� �cart� �cervel� �chancr� �chantillonn� �chapp�
 �chauffant �chauff� �chevel� �chiquet� �choguid� �chu �clairant �claircissant
 �clatant �clat� �clipsant �clop� �coeurant �corch� �cot� �coutant �crant�
 �cras� �crit �cru �cr�m� �cul� �cumant �dent� �difiant �dulcorant �gaill�
 �gar� �gayant �grillard �gris� �grotant �gueul� �hanch� �hont� �labor� �lanc�
 �lectrisant �lectroconvulsivant �lectrofondu �lectroluminescent
 �lev� �lingu� �lisab�thain �lizab�thain �loign� �loquent �lu �l�gant
 �maci� �manch� �mancip� �margin� �mergent �merg� �merillonn� �merveillant
 �migr� �minent �mollient �motionnant �moulu �moustillant �mouvant �mu
 �mulsionnant �m�ch� �m�tisant �nergisant �nervant �nerv� �paississant �panoui
 �pargnant �patant �pat� �peign� �perdu �peur� �picotyl� �picutan� �pic�
 �pig� �pingl� �plor� �ploy� �point� �poustouflant �pouvant� �prouvant �prouv�
 �puis� �pur� �quicontinu �quidistant �quilibrant �quilibr� �quin �quipollent
 �quipol� �quipotent �quip� �quitant �quivalent �raill� �reintant �reint�
 �rubescent �rudit �ryth�matopultac� �tabli �tag� �teint �tendu �th�r�
 �tiol� �toff� �toil� �tonnant �tonn� �touffant �touff� �tourdi �tourdissant
 �triquant �triqu� �troit �tudiant �tudi� �tymologisant �vacuant �vacu� �vad�
""".split())