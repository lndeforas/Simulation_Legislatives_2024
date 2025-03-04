## Informations

**Méthode de calcul**
- Coefficients ([Voir le fichier JSON](coefficients.json)) : à adapter selon les actualités, dernière modification le 02/07 pour tenir compte des désistements et des sondages.
- Je me suis inspiré de [Le grand continent](https://legrandcontinent.eu/fr/2024/07/02/la-baisse-de-la-participation-au-second-tour-pourrait-donner-la-majorite-absolue-au-rn/#:~:text=Reports%20de%20voix%20dans%20les,4%20lignes%20et%2011%20colonnes.&text=Lors%20du%20premier%20tour%2C%20le,du%20premier%20tour%20de%202022.) pour faire les coefficients, mais mes estimations sont approximatives.  
- Pour un duel A-B, on regarde les proportions de gens qui ont voté pour A, B, C ou D au premier tour et vont voter pour A ou B au second. Par exemple pour le duel ENS-RN, j'ai indiqué que 40% des gens qui ont voté NFP au premier tour vont voter ENS, et 0% des gens qui ont voté NFP au premier tour vont voter RN ensuite.

**Outils**
- Webscraping : BeautifulSoup and requests
- Data Legislatives 1er tour : [https://www.resultats-elections.interieur.gouv.fr/legislatives2024/index.html](https://www.resultats-elections.interieur.gouv.fr/legislatives2024/index.html)
- Preprocessing : Pandas
- Fond de carte : OpenStreetMap
- Carte intéractive : Leaflet
- Circonscriptions : [https://www.data.gouv.fr/fr/datasets/carte-des-circonscriptions-legislatives-2012-et-2017/#/resources](https://www.data.gouv.fr/fr/datasets/carte-des-circonscriptions-legislatives-2012-et-2017/#/resources)
- Diagramme circulaire : Chart.js
- Site web : JS et HTML
- Hébergement du site : Arise

## Screenshots du site
![](images/Capture%20d’écran%202024-07-02%20154034.png)
![](images/Capture%20d’écran%202024-07-02%20154105.png)
![](images/Capture%20d’écran%202024-07-03%20103005.png)
