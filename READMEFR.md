# Croisement de Moyennes Mobiles — Backtesting de Stratégie

## De quoi s'agit-il ?
Avant de risquer de l'argent réel sur une stratégie de trading,
les analystes quantitatifs la simulent sur des données historiques
pour mesurer ses performances. C'est ce qu'on appelle le backtesting.

Dans ce projet, j'ai construit un système de backtesting en Python
pour répondre à une question simple :

> Une stratégie de trading basée sur des règles simples peut-elle battre le fait de ne rien faire ?

## La stratégie : Croisement de Moyennes Mobiles
La stratégie repose sur deux Moyennes Mobiles :
- MA20 = moyenne des prix de clôture sur les 20 derniers jours
- MA50 = moyenne des prix de clôture sur les 50 derniers jours

Si MA20 passe AU-DESSUS de MA50 → Acheter
Si MA20 passe EN-DESSOUS de MA50 → Vendre

## Données
- Actifs : AAPL (Apple), JPM (JPMorgan), MSFT (Microsoft)
- Période : Janvier 2022 → Janvier 2024
- Source : Yahoo Finance via yfinance
- Capital de départ : 10 000$ par actif

## Métriques de Performance
Trois métriques sont utilisées pour évaluer la stratégie :

   ### Rendement Total
La stratégie a-t-elle gagné ou perdu de l'argent ?
> Rendement Total = (Valeur Finale - Capital Initial) / Capital Initial

   ### Ratio de Sharpe
Le rendement valait-il le risque pris ?
> Ratio de Sharpe = (Rendement Annuel - Taux Sans Risque) / Volatilité Annuelle

   ### Max Drawdown
Quelle était la pire perte depuis un sommet avant récupération ?
> Max Drawdown = (Portefeuille au creux - Portefeuille au sommet) / Portefeuille au sommet

## Résultats
AAPL (Apple)
Rendement Total : -38.16% | Ratio de Sharpe : -0.93 | Max Drawdown : -45.30%

JPM (JPMorgan)
Rendement Total : -20.45% | Ratio de Sharpe : -0.55 | Max Drawdown : -39.26%

MSFT (Microsoft)
Rendement Total : -44.53% | Ratio de Sharpe : -1.07 | Max Drawdown : -58.57%

Les trois actifs ont produit des rendements négatifs avec des ratios de Sharpe négatifs.

## Stratégie vs Buy & Hold
Pour évaluer si la stratégie MA apporte une vraie valeur ajoutée,
je l'ai comparée au benchmark le plus simple possible : le Buy & Hold.

Le Buy & Hold consiste à investir 10 000$ au premier jour
et ne jamais vendre, quelles que soient les conditions du marché.

> Valeur Buy & Hold = 10 000$ × (Prix aujourd'hui / Prix au jour 1)

Ce benchmark répond à une question fondamentale en finance quantitative :

> La complexité de ma stratégie justifie-t-elle son existence ?
> Ou aurait-il été plus rentable de ne rien faire ?

AAPL : Stratégie MA : -38.16% | Buy & Hold : 25.40%
JPM  : Stratégie MA : -20.45% | Buy & Hold : 35.58%
MSFT : Stratégie MA : -44.53% | Buy & Hold : 33.08%

Sur les trois actifs, la stratégie MA a sous-performé le Buy & Hold.

## Pourquoi la stratégie a-t-elle échoué ?
2022 était un marché baissier, les actions technologiques ont
chuté significativement en raison de la hausse des taux d'intérêt
et de l'incertitude macroéconomique.

Les stratégies de croisement de moyennes mobiles fonctionnent bien
dans les marchés tendanciels, mais génèrent trop de faux signaux
dans les marchés volatils et sans direction claire.

En 2022, le marché changeait rapidement de direction, poussant la
stratégie à acheter juste avant les baisses et à vendre juste avant
les hausses.

