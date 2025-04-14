# AI Maze Solver 🚀

🎯 **AI Maze Solver** je interaktivna aplikacija koja spaja zabavu 🎮 i snagu algoritama 🧠 za rješavanje labirinta. Bilo da ste entuzijast za igre, student koji uči algoritme ili iskusni programer, ovaj projekt pruža uzbudljiv **showcase** moćnih algoritama pretraživanja puta kroz zamršene labirinte – uz vizualizacije u stvarnom vremenu i statističku usporedbu 📊! 

## 🧩 Uvod i motivacija  
Zamislite da generirate vlastiti labirint i gledate kako računalo pronalazi izlaz dok vi pratite svaki korak! **AI Maze Solver** nastao je iz želje da se demonstrira kako različiti algoritmi pretraživanja pronalaze put kroz kompleksne zagonetke. Kroz intuitivno korisničko sučelje i atraktivne vizualizacije, ovaj projekt istovremeno educira i zabavlja, pružajući uvid u **BFS**, **DFS** i **A*** algoritme na djelu. Prepustite se istraživanju algoritamskih rješenja dok aplikacija statistički prati njihov učinak i efikasnost. 🔍🎉

## 🚀 Ključne značajke projekta  
- **Generiranje labirinta**: Jednim klikom generirajte nasumični labirint različitih dimenzija i složenosti. Svaki je labirint unikatna zagonetka spremna za rješavanje.
- **Algoritmi rješavanja**: Podržano je rješavanje labirinta trima algoritmima pretraživanja:
  - **BFS (pretraživanje u širinu)** – pronalazi najkraći put sloj po sloj.
  - **DFS (pretraživanje u dubinu)** – istražuje put do krajnjih granica prije povratka.
  - **A*** (A-star algoritam) – heuristički pretražuje najbrži put kombinirajući udaljenost i procjenu preostalog puta.
- **Interaktivni UI**: Intuitivno **grafičko sučelje** omogućuje odabir algoritma, pokretanje generiranja i rješavanja labirinta te praćenje postupka u stvarnom vremenu. 🕹️ 
- **Vizualizacija korak-po-korak**: Gledajte animaciju pretrage – algoritam boji put kojim prolazi, istražuje susjede i pronalazi rješenje. Završni pronađeni put jasno je istaknut kroz labirint. ✨
- **Statistika izvedbe**: Nakon rješavanja, aplikacija prikazuje ključne statistike: dužinu pronađenog puta, broj posjećenih polja, te vrijeme izvršavanja algoritma. Usporedite učinkovitost različitih algoritama na istom labirintu uz pomoć grafičkih prikaza i brojčanih pokazatelja. 📊
- **Edukativno i zabavno**: AI Maze Solver je odličan alat za učenje – eksperimentirajući s algoritmima korisnici mogu intuitivno razumjeti njihove razlike. Istovremeno, generiranje labirinata i promatranje rješavanja pruža puno zabave svim korisnicima.

## 🛠️ Tehnologije i biblioteke  
Projekt je izgrađen koristeći moderni **Python** ekosustav te provjerene biblioteke za razvoj vizualno privlačnih algoritamskih simulacija:  
- **Python 3.x** – Glavni programski jezik projekta, koristi se za implementaciju logike generiranja labirinta i algoritama pretraživanja.  
- **Pygame** – Biblioteka za razvoj igara i grafičkih aplikacija u Pythonu. Koristi se za izradu interaktivnog 2D sučelja, crtanje labirinta i animaciju koraka algoritama u stvarnom vremenu. 🎮  
- **Matplotlib** – Biblioteka za grafički prikaz podataka. Koristi se za kreiranje grafikona i prikaz statističkih usporedbi (npr. usporedba vremena izvršavanja algoritama). 📊  
- *(Ostale biblioteke)* – Standardne Python biblioteke poput `random` za generiranje nasumičnih labirinata, kao i `time` za mjerenje vremena, te dodatne pomoćne biblioteke navedene u **requirements.txt** datoteci.

## ⚙️ Instalacija  
Slijedite ove korake za postavljanje projekta na vaše računalo:  

1. **Klonirajte repozitorij**: Preuzmite izvorni kod ovog repozitorija s GitHub-a (`git clone https://github.com/vaš-korisnički-račun/AI-Maze-Solver.git`) ili preuzmite ZIP arhivu.  
2. **Kreirajte virtualno okruženje** (preporučeno):  
   ```bash
   python3 -m venv venv             # kreiranje virtualnog okruženja
   source venv/bin/activate         # aktivacija na Linux/macOS
   venv\Scripts\activate            # aktivacija na Windows
   ```  
   Ovo osigurava izolirano okruženje za potrebne pakete, bez utjecaja na globalne instalacije.  
3. **Instalirajte ovisnosti**: U korijenu projekta pokrenite naredbu:  
   ```bash
   pip install -r requirements.txt
   ```  
   Ova naredba povući će i instalirati sve potrebne Python pakete za pokretanje aplikacije. (Provjerite da koristite `pip` unutar aktiviranog virtualnog okruženja.)  
4. **Spremni za pokretanje**: Nakon uspješne instalacije ovisnosti, projekt je spreman za korištenje! 🎉  

> **Napomena:** Potrebno je barem imati instaliran **Python 3.7+**, a naša preporuka je Python 3.10 radi potpune kompatibilnosti sa svim korištenim paketima.

## 🚀 Pokretanje i korištenje

- U terminalu se pozicionirajte u korijenski direktorij projekta i pokrenite glavnu skriptu:  
  ```bash
  python main.py
  ```  
- Nakon pokretanja, otvorit će se grafičko korisničko sučelje aplikacije. U sučelju možete:  
  - **Generirati labirint** – Odaberite željene postavke (težinu labirinta), zatim kliknite na gumb *"Generiraj labirint"*. Aplikacija će stvoriti novi nasumični labirint.  
  - **Odabrati algoritam** – Odaberite jedan od algoritama pretraživanja: *BFS*, *DFS* ili *A**.  
  - **Pokrenuti rješavanje** – Kliknite tipku za početak rješavanja kako biste pokrenuli odabrani algoritam. Sada možete pratiti animaciju dok algoritam prolazi kroz labirint u potrazi za izlazom. 🔄  
- **Praćenje vizualizacije** – Tijekom izvršavanja, algoritam boja trenutno istraživane putanje i čvorove labirinta. Možete vidjeti redoslijed obilaska: npr. BFS ravnomjerno širi pretragu sloj po sloj (što izgleda poput valova kroz labirint), dok DFS ide duboko u jedan smjer pa se vraća unazad. A* inteligentno skakuće prema cilju na temelju procjene udaljenosti.  
- **Prikaz rezultata** – Kada algoritam pronađe izlaz, krajnji put od starta do cilja bit će istaknut bojom. UI će također prikazati statistike poput:
  - Duljina pronađenog puta (broj koraka kroz labirint do cilja).
  - Broj posjećenih polja (čvorova) tijekom pretrage.
  - Ukupno trajanje rješavanja (u milisekundama).  
- **Eksperimentiranje** – Slobodno promijenite algoritam ili generirajte novi labirint te pokušajte ponovno. Usporedite kako različiti algoritmi pristupaju rješavanju iste zagonetke. Svako novo pokretanje donosi drugačiji izazov i priliku za učenje! 🧪

## 📊 Vizualizacija i statistika  
U nastavku su prikazani primjeri vizualizacije rada aplikacije i statističkih rezultata algoritama (GIF animacije i slike u završnoj verziji README-a):  

<!-- Animirani GIF koji prikazuje postupak rješavanja labirinta -->
<!-- ![Animacija rješavanja labirinta](docs/maze_solver_demo.gif) -->

<!-- Slika ili graf koji prikazuje statističku usporedbu algoritama (trajanje i broj koraka) -->
<!-- ![Usporedna statistika algoritama](docs/maze_solver_stats.png) -->

*_(Slika gore:_ **Animacija** prikazuje korak-po-korak rješavanje generiranog labirinta pomoću jednog od algoritama. **Grafikon** ilustrira usporedbu performansi algoritama BFS, DFS i A* na više različitih labirinata.)*

## 📁 Struktura projekta  
Projekt je organiziran kako bi kod bio razumljiv i proširiv. Glavni dijelovi strukture (foldera i datoteka) su:  

```plaintext
AI-Maze-Solver/
├── docs/                        # Dokumentacija i mediji (slike, GIF-ovi za prezentaciju)
│   ├── wbs.png                  # Hijerarhijska podjela svih projektnih zadataka
│   ├── pert-dijagram.png        # Pert dijagram s vremenskim prikazom zadataka
│   └── README.md                 
├── requirements.txt             # Popis potrebnih Python paketa (ovisnosti)
├── README.md                    # Ovaj README dokument projekta
├── src/                         # Izvorni kod aplikacije 
│   ├── main.py                  # Glavna skripta za pokretanje aplikacije 
│   ├── maze_generator/          # Kod za generiranje nasumičnih labirinata 
│   │   ├── __init__.py
│   │   ├── generator.py
│   ├── algorithms/              # Implementacije algoritama (BFS, DFS, A*)
│   │   ├── __init__.py
│   │   ├── bfs.py               # Implementacija BFS (Breadth-First Search)
│   │   ├── dfs.py               # Implementacija DFS (Depth-First Search)
│   │   ├── astar.py             # A* algoritam s heuristikama
│   ├── visualization/           # Kod za korisničko sučelje i vizualizaciju labirinta
│   │   ├── __init__.py
│   │   ├── pygame_ui.py         # Glavni modul za korisničko sučelje (UI) u Pygame-u
│   ├── performance/
│   │   ├── __init__.py
│   │   └── stats.py             # Funkcije za mjerenje vremena, broja posjećenih čvorova, duljine pronađenog puta
│   └── integration/             # Brine se da su sve komponente konzistentno povezane
│       ├── __init__.py
│       └── integrator.py
└── tests/                       # Sve testne skripte za validaciju projekta
    ├── test_generator.py
    ├── test_bfs_dfs.py
    ├── test_astar.py
    ├── test_visualization.py
    └── test_integration.py            
```

Slobodno nam se obratite putem **GitHub Issues** stranice ili emaila za bilo kakva pitanja, prijedloge ili suradnju. Cijenimo povratne informacije i rado ćemo pomoći oko korištenja projekta ili razvoja novih značajki!

## 🎉 Zahvala i poziv na korištenje  
Hvala vam što ste odvojili vrijeme za pregled ovog projekta! 🙏 Nadamo se da će vam ovaj alat biti jednako zabavan i koristan kao što je bio i nama tijekom razvoja. Pozivamo vas da isprobate aplikaciju, podijelite je s drugima i javite nam svoje dojmove.  

Ako vam se projekt sviđa, ne zaboravite ostaviti ⭐ zvjezdicu i doprinijeti širenju riječi. Sretno rješavanje labirinata i uživajte u istraživanju algoritama! 🎯🤖
