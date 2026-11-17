# PROTOCOLE TECHNIQUE D'INSTALLATION & MATRICE DE DÉPLOIEMENT
## Bureau numérique BTP — Procédure Standardisée d'Intervention Sécurisée

---

## 1. PROCÉDURE DE CONNEXION DISTANTE SÉCURISÉE (Zéro Partage de Mot de Passe)

> [!IMPORTANT] Règle de Sécurité Absolue
> **Ne jamais demander ni manipuler le mot de passe personnel de l'artisan.**
> La prise en main doit se faire en direct, avec l'artisan présent devant son écran, via les outils natifs de Windows ou des utilitaires temporaires à code unique.

### Méthode 1 (Privilégiée) : « Assistance Rapide » de Windows (Quick Assist)
- **Avantage :** 100 % natif dans Windows 10 et Windows 11, déjà installé, zéro téléchargement requis pour le client.
- **Protocole :**
  1. Vous dites au client : *"Appuyez simultanément sur les touches `Ctrl` + `Touche Windows` + `Q`"*.
  2. Vous lancez l'Assistance Rapide depuis votre poste et cliquez sur *"Aider une autre personne"*.
  3. Microsoft vous génère un code sécurisé à 6 chiffres valable 10 minutes.
  4. Vous dictez ce code à l'artisan, qui l'encode sur son écran et clique sur *"Partager l'écran"*.
  5. Vous demandez le *"Contrôle total"* qu'il valide d'un simple clic.
  6. Dès que vous avez fini, la session se coupe et aucun accès ultérieur n'est possible.

### Méthode 2 (Alternative) : AnyDesk à Mot de Passe Temporaire
- Si le client est sur une ancienne version ou Mac :
  1. Le client télécharge l'exécutable léger `AnyDesk.exe` (sans installation requise).
  2. Il vous donne son identifiant à 9 chiffres.
  3. Vous initiez la connexion et il clique sur le bouton vert *"Accepter"*.

---

## 2. MATRICE D'ENVIRONNEMENT : QUE FAIRE SELON L'ÉQUIPEMENT DU CLIENT ?

Tous les artisans ne possèdent pas une licence Microsoft 365 Business. Voici la stratégie de déploiement à adopter selon l'audit préalable :

```
┌────────────────────────────────────────────────────────────────────────┐
│             AUDIT DE L'ENVIRONNEMENT LOGICIEL DU CLIENT                │
├──────────────────────────┬─────────────────────────────────────────────┤
│ CAS A : Le client a déjà │ ➔ Déploiement standard :                    │
│ M365 Business Basic/Std  │    • Microsoft Lists + Excel connecté       │
│                          │    • Alertes via flux Power Automate        │
│                          │    • Coût logiciel additionnel : 0,00 €     │
├──────────────────────────┼─────────────────────────────────────────────┤
│ CAS B : Le client a une  │ ➔ Recommandation d'upgrade ou Option C :    │
│ vieille version Office   │    • Si le client est d'accord : achat d'une│
│ (2013/2016/2019) ou rien │      licence M365 Business Basic (5,60 €/m) │
│                          │      facturée directement par Microsoft.    │
│                          │    • Si refus catégorique de payer un       │
│                          │      abonnement : bascule vers CAS C.       │
├──────────────────────────┼─────────────────────────────────────────────┤
│ CAS C : ZÉRO ABONNEMENT  │ ➔ DÉPLOIEMENT ALTERNATIF GOOGLE WORKSPACE   │
│ Le client refuse tout    │    • Google Sheets (Tableau de bord jumeau) │
│ coût mensuel tiers       │    • Google Forms pour la saisie mobile     │
│                          │    • Google Apps Script gratuit pour les    │
│                          │      rappels et alertes automatiques        │
│                          │    • Coût logiciel perpétuel : 0,00 € !     │
└──────────────────────────┴─────────────────────────────────────────────┘
```

---

## 3. L'ALTERNATIVE PRAGMATIQUE À L'API WHATSAPP (Formulaire Web Mobile PWA)

L'API WhatsApp officielle étant payante et complexe pour une TPE, la remontée des données du chantier vers le bureau s'effectue via un **raccourci mobile sécurisé 100 % gratuit** :

1. **Création d'un formulaire épuré :**
   - Réalisé sous **Microsoft Forms** (si M365) ou **Google Forms** (si compte gratuit).
   - Comporte 4 champs obligatoires seulement : *Nom du client*, *Montant estimé HTVA*, *Description courte*, *Photo du bon de travail ou du croquis*.
2. **Installation sur le smartphone de l'artisan (en 30 secondes) :**
   - Ouvrir le lien du formulaire dans Safari (iPhone) ou Chrome (Android).
   - Cliquer sur *"Ajouter à l'écran d'accueil"*.
   - Renommer l'icône : **« NOUVEAU DEVIS »**.
3. **Résultat sur le terrain :**
   - L'artisan quitte le client, sort son smartphone, tape sur l'icône « NOUVEAU DEVIS », saisit le nom et le montant en 20 secondes.
   - Les données tombent instantanément dans le tableau de bord du bureau sans ouvrir d'ordinateur.

---

## 4. BLINDAGE ET VERROUILLAGE DU CLASSEUR EXCEL (Protection Anti-Erreur)

Pour empêcher l'artisan ou sa secrétaire de casser accidentellement les formules, le classeur est protégé selon une architecture à deux zones :

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ZONAGE DE PROTECTION EXCEL                      │
├──────────────────────────────────────────────────┬─────────────────────┤
│ ZONE VERROUILLÉE (Lecture seule protégée)        │ ZONE DÉVERROUILLÉE  │
│ • Colonne A : N° Devis (auto ou incrémental)     │ • Colonne C : Nom   │
│ • Colonne H : Date de relance calculée           │ • Colonne D : Tél   │
│ • Colonne I : Formule du statut d'urgence        │ • Colonne E : Objet │
│ • Feuille « Tableau de Bord » complète           │ • Colonne F : Prix  │
│   (Toutes les formules SUMIF/COUNTIF protégées)  │ • Colonne G : Statut│
│                                                  │ • Colonne K : Notes │
└──────────────────────────────────────────────────┴─────────────────────┘
```

- **Mot de passe de déverrouillage de maintenance :** Défini par vous (conservé dans votre fichier client), évitant toute corruption fortuite.
- **Règle de sauvegarde de secours :** Mise en place d'un dossier OneDrive avec historique des versions activé (permet de restaurer en 1 clic un fichier écrasé à l'état de la veille).
