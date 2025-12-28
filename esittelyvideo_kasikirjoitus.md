# Esittelyvideon Käsikirjoitus: PDF-Luokitteluohjelma

**Kesto:** n. 3-5 min  
**Tarkoitus:** Esitellä ohjelman logiikka, uusi skannattujen PDF:ien käsittely ja tiedostojen siirto.

---

## 0. Intro (Kamera / Yleiskuva)
"Tässä videossa käydään läpi Pythonilla toteutettu älykäs PDF-luokittelija. Ohjelma lukee PDF-tiedostoja, päättelee niiden sisällön OpenAI:n kielimallin avulla ja siirtää ne oikeisiin kansioihin. Katsotaan koodia."

---

## 1. Pääohjelma ja Käyttöliittymä (`Main/app.py`)

"Aloitetaan ohjelman ytimestä, `app.py` tiedostosta, joka hoitaa käyttöliittymän."

*   **Rivit 17-27 (`show_menu`):** "Tässä `Rich`-kirjastolla piirretään terminaaliin valikko. Selkeä lista toiminnoista."
*   **Rivi 100 (`run`):** "Tämä `while True` -silmukka pitää ohjelman käynnissä. Käyttäjän syöte luetaan ja ohjataan eteenpäin."
*   **Rivi 106:** "Kun käyttäjä valitsee ykkösen ('1'), kutsutaan `classifier.process_all_files()`. Siirrytään sinne."

---

## 2. Luokitteluprosessi (`Main/classifier.py`)

"Tämä on ohjelman aivot. Funktio `process_all_files` (rivi 15) ohjaa koko prosessia."

*   **Rivi 20:** "Ensin ladataan luokitteluohjeet Excelistä (`instructions_loader`)."
*   **Rivi 27:** "Haetaan kaikki käsittelemättömät PDF:t `Search`-kansiosta."
*   **Rivi 38 (`extract_text`):** "Yritetään irrottaa teksti PDF:stä perinteisin keinoin."
    
**(Tärkeä kohta: Uusi ominaisuus)**
*   **Rivit 43-48:** "Tässä on uusi logiikka. Jos tekstiä *ei* saada irti (esim. skannattu kuvatiedosto), ohjelma ei enää luovuta. Sen sijaan se kutsuu `llm_client.analyze_scanned_pdf` -funktiota ja lähettää tiedoston suoraan tekoälyn katsottavaksi."

---

## 3. Tekoäly ja OpenAI Integraatio (`Main/llm_client.py`)

"Katsotaan, miten tuo tekoälykutsu tapahtuu pellon alla."

*   **Rivi 18 (`classify_document`):** "Tämä on se perusfunktio tekstipohjaisille PDF:ille. Rakentaa promptin ja lähettää tekstin."
*   **Rivi 102 (`analyze_scanned_pdf`):** "Tämä on uusi funktio skannatuille tiedostoille."
*   **Rivi 115:** "Tiedosto ladataan (`client.files.create`) ensin OpenAI:n palvelimelle."
*   **Rivit 153-166:** "Sitten tehdään pyyntö, jossa viitataan tuohon ladattuun tiedostoon (`file_id`). Näin malli voi 'nähdä' dokumentin sisällön kuvana."
*   **Rivi 177:** "Lopuksi siivotaan ja poistetaan väliaikainen tiedosto pilvestä."

---

## 4. Tiedostojen Siirto (`Main/classifier.py` & `Main/filesystem.py`)

"Palataan `classifier.py`:hyn. Kun luokka on saatu selville..."

*   **Rivi 88 (`classifier.py`):** "Määritetään kohdekansio koodin perusteella."
*   **Rivi 90 (`classifier.py`):** "Kutsutaan `filesystem.move_file`."

"Katsotaan nopeasti vielä `filesystem.py`."

*   **Rivi 21 (`move_file`):** "Tämä funktio hoitaa fyysisen siirron."
*   **Rivit 33-39:** "Tässä on tärkeä varmistus: jos kohdekansiossa on jo samanniminen tiedosto, ohjelma ei ylikirjoita sitä, vaan nimeää uuden tiedoston juoksevalla numerolla (esim. `lasku_1.pdf`)."

---

## 5. Lopetus

"Lopuksi `classifier.py` rivillä 94 tallennetaan kaikki tapahtumat tietokantaan (`db.log_event`), jotta jää jälki siitä, mitä tehtiin. Näin prosessi on turvallinen, automaattinen ja jäljitettävä."
