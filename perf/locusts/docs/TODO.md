- Demander les stats actuels du site
	now :
		- 100.000 / semaine  (call api)
		- 20-50 bénéficiaires
		- 7000 conseillers
		- 73k visiteurs
	future :
		- x2 conseillers
		- x4 visiteurs

	=> app
	=> mobile

- Demander le plan d'archi du site
- Demander les URL prod / preprod / testing (aucun test dessus)

-------------------

- Faire les Docker
- Faire audit de sécu sur custom-auth-oidc
	- vérifier les versions des libs
	- vérifier les headers
	- vérifiers les input filters
- Faire scénario :
	>>> et ça serait un scenario, je vais sur le site, je me connecte, je fais 2-3 actions et ça boucle la dessus
	>>> un autre scenario qui simule sur le back l'activité mobile
	>>> un autre scenario qui simule le traffic partenaire sur le back (ptet moins prio)
	>>> et un dernier scenario qui lance en // les 3 scenarios pour avoir le vrai bruit de la prod
	>>> surement un sujet sur l'injection des données et surement des bouchons à fabriquer
- Faire un env de "test" avec docker swam ou docker compose (api, app, connect, web)
- Faire un env de "tir" avec docker swam ou docker compose (locust nodes)
- Proposer une archi pour gérer le flux de données
- Tester gattling ?
