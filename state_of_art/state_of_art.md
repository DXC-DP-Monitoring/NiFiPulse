## State of Art
#  État de l’art : Supervision et Observabilité des Pipelines de Données

## 1. Introduction

### 1.1. Problématique : Manque de fiabilité et de visibilité
Malgré leur rôle stratégique, les pipelines de données restent faiblement observables et difficiles à maintenir.  
Plusieurs études soulignent que la mauvaise qualité des données entraîne en moyenne une perte annuelle de plus de **15 millions de dollars** par organisation [3].

Ce déficit de fiabilité découle principalement d’un **manque de supervision centralisée** et d’une **fragmentation des outils de suivi**.  
Les ingénieurs de données font face à des pipelines sujets aux erreurs, difficiles à déboguer, et coûteux à opérer (Foidl et al., 2024) [3].

Dans ce contexte, la mise en place d’une **supervision continue** devient indispensable.  
Celle-ci englobe la surveillance des **métriques de performance**, le suivi des **opérations techniques** et l’évaluation de la **qualité des données** tout au long du cycle de vie du pipeline.

Cette approche s’inscrit dans la logique d’**observabilité des données**, qui vise à assurer une vision holistique des flux, incluant :
- la **traçabilité complète (data lineage)**,  
- la **corrélation entre logs, métriques et traces**,  
- la **détection proactive des anomalies** [4].

> L’observabilité dépasse donc le simple monitoring en intégrant la capacité à comprendre le comportement interne du pipeline et à anticiper les défaillances.

---

### 1.2. Objectif du travail
L’objectif de ce travail est de présenter l’évolution des approches de supervision et d’observabilité des pipelines de données, en identifiant leurs apports, leurs limites et les axes d’amélioration.

Il s’agit notamment de comprendre comment les solutions récentes intègrent la **surveillance technique** et la **traçabilité** au sein d’un cadre cohérent.

Dans ce cadre, **Apache NiFi** constitue un élément clé.  
Conçu pour la gestion automatisée des flux de données, NiFi (et sa déclinaison légère *MiNiFi*) offre des **capacités natives de monitoring et d’observabilité** grâce à ses **FlowFiles**, qui encapsulent à la fois les données et leurs métadonnées de transfert.

Ces métadonnées peuvent être exploitées pour :
- la **collecte de métriques** (via Prometheus),  
- l’**agrégation analytique** (via PostgreSQL ou un cube OLAP),  
- et la **visualisation intégrée** (via Power BI),  
formant ainsi un socle technique aligné avec une approche d’observabilité complète [4].

---

## 2. Objectifs et Types de Supervision

### 2.1. Objectifs du Monitoring et de l’Observabilité

Le **monitoring** consiste à observer de manière continue les performances opérationnelles et le comportement des processus au sein du pipeline.  
Il s’appuie sur la **journalisation (logging)**, la **collecte de métriques (metrics scraping)** et la **génération d’alertes** afin d’anticiper les défaillances [1].

Dans l’architecture proposée :
- **Apache NiFi** génère des métriques sur la latence, la taille des files et la provenance des flux.  
- **Prometheus** collecte ces métriques pour les visualiser dans **Grafana** ou **Power BI**, permettant une analyse à la fois technique et analytique.

> L’observabilité vise à corréler ces signaux techniques avec des informations de contexte, de manière à comprendre le *« pourquoi »* derrière chaque anomalie [1].

| Objectif de supervision | Description | Soutien par la littérature |
|--------------------------|-------------|-----------------------------|
| **1. Garantir la qualité des données** | Surveiller les dimensions de la DQ : exactitude, complétude, cohérence, actualité. Great Expectations valide les datasets produits par NiFi avant ingestion analytique. | Ehrlinger et al. (2022) |
| **2. Détecter les anomalies d’exécution** | Suivre latence, erreurs, et temps d’exécution via Prometheus. | Serrano et al. (2021) |
| **3. Fournir la traçabilité et l’observabilité** | Garantir le suivi du *data lineage* à travers les FlowFiles et les métadonnées exportées vers l’entrepôt analytique. | Monteiro et al. (2023) |

Ainsi, la supervision devient un **cadre d’observabilité intégré**, reliant les métriques d’exécution, la qualité des données et la compréhension globale du flux de transformation.

---

### 2.2. Types de Monitoring Basés sur les Sources

La supervision peut être déclinée en plusieurs types selon les dimensions observées : **opérationnelle**, **structurelle** et **métadonnées**.  
Ces couches interagissent pour former une solution d’observabilité complète, centrée sur Apache NiFi comme cœur du flux.

#### **Type 1 : Monitoring Opérationnel / de Performance**
Surveillance des performances techniques : latence, débit, erreurs et charge.  
NiFi fournit ces indicateurs nativement, collectés et stockés par **Prometheus**, puis visualisés dans **Grafana** ou **Power BI**.

#### **Type 2 : Monitoring Structurel et Profilage des Données**
Suivi de la structure des jeux de données (schémas, colonnes, relations) et détection de changements de schéma (*schema drift*).  
Les métadonnées issues de NiFi sont centralisées dans un entrepôt PostgreSQL pour l’analyse historique.

#### **Type 3 : Monitoring du Flux de Travail et des Métadonnées**
Garantir la cohérence du pipeline dans son ensemble.  
Les **FlowFiles NiFi** et les **métadonnées de provenance** exportées vers PostgreSQL permettent de reconstruire le *data lineage* complet, de la source à la visualisation Power BI.

---

## 3. Outils et Approches Existants pour la Supervision et l’Observabilité

L’écosystème de la supervision vise à renforcer la fiabilité et la continuité opérationnelle des flux.  
Dans l’architecture proposée, la supervision repose sur quatre composants complémentaires :

- **Apache NiFi** : orchestration et gestion des flux  
- **GitHub Actions** : automatisation et génération périodique de métriques  
- **PostgreSQL** : stockage analytique des indicateurs  
- **Power BI** : visualisation et suivi en temps réel  

Cette combinaison permet d’assurer un niveau d’observabilité complet, englobant la collecte, la persistance et l’analyse des métriques de performance.

---

### 3.1. Monitoring Opérationnel et Orchestration Native

**Apache NiFi** orchestre le flux complet de données et fournit des métadonnées détaillées via ses **Flow Files**.  
Un **workflow GitHub Actions** exécute périodiquement des scripts Python pour collecter les métriques de performance (CPU, mémoire, statut des processeurs, disponibilité des nœuds).  

Les données sont stockées dans **PostgreSQL**, selon un modèle **OLAP dénormalisé**, permettant des analyses temporelles et comparatives.  
Des **triggers PL/pgSQL** assurent la génération automatique d’alertes en cas d’anomalie détectée (latence, charge, erreurs critiques).

---

### 3.2. Système de Visualisation et de Reporting Analytique

La **visualisation** repose sur **Power BI**, connecté à PostgreSQL.  
Les tableaux de bord présentent :
- l’évolution des indicateurs en temps réel,  
- les taux d’exécution et d’erreurs,  
- la corrélation entre logs et périodes d’activité.

Cette interface offre une vision opérationnelle et intuitive de l’état du pipeline, accessible à tous les profils (techniques ou métiers).

---

### 3.3. Traçabilité et Corrélation des Événements

La **traçabilité (data lineage)** est assurée par les FlowFiles de NiFi et les journaux d’exécution sauvegardés dans PostgreSQL.  
La corrélation entre les traces issues de NiFi et les métriques issues de GitHub Actions permet une **analyse causale** des anomalies (*root cause analysis*).  
Power BI restitue ces informations sous forme de tableaux de bord temporels intégrant logs, métriques et événements.

---

## 5. Discussion et Conclusion

### 5.1. Synthèse

#### A. Absence de Vue Unifiée
Les outils actuels restent fragmentés entre monitoring applicatif, infrastructure et flux métier.  
Il est donc difficile d’obtenir une **vue consolidée** reliant erreurs, performances et étapes d’exécution.

#### B. Manque d’Observabilité Intégrée
Les logs, métriques et traces demeurent souvent séparés.  
L’absence d’un **stockage analytique centralisé** empêche l’analyse historique et la corrélation automatique des événements.

#### C. Manque d’Automatisation
Les alertes statiques et la surveillance manuelle limitent la réactivité.  
Un besoin fort d’**automatisation et d’intelligence opérationnelle** se fait sentir pour améliorer la maintenance et la fiabilité.

---

### 5.2. Vers une Solution de Supervision

La solution proposée repose sur quatre piliers :

- **Orchestration et logs (Apache NiFi)**  
  Extraction de la base de provenance et des logs d’exécution.

- **Centralisation et stockage (PostgreSQL)**  
  Intégration des métriques et logs dans un modèle OLAP dénormalisé.

- **Alerte automatisée (PL/pgSQL)**  
  Déclenchement de triggers en cas d’anomalie ou dépassement de seuil.

- **Visualisation analytique (Power BI)**  
  Restitution des métriques sous forme de tableaux de bord dynamiques.

> Cette architecture offre une vue consolidée, continue et automatisée de la supervision, combinant logs, métriques et événements dans un cadre unifié.

---

### 5.3. Conclusion Générale

Les limites identifiées — manque d’unification, d’observabilité intégrée et d’automatisation — justifient la conception d’une **solution de monitoring opérationnel intelligent**.

L’approche proposée, fondée sur :
- l’extraction des logs NiFi,  
- leur intégration dans PostgreSQL,  
- et leur visualisation dans Power BI,  

constitue une **base expérimentale solide** pour le développement d’une supervision proactive et, à terme, d’une observabilité prédictive.

---

## Références

- Foidl et al. (2024). *A Survey of Pipeline Tools for Data Engineering*. [arXiv:2406.08335](https://arxiv.org/abs/2406.08335)  
- Ehrlinger et al. (2022). *A Survey of Data Quality Measurement and Monitoring Tools*. [Frontiers in Big Data](https://www.frontiersin.org/journals/big-data/articles/10.3389/fdata.2022.850611/full)  
- Monteiro et al. (2023). *Data Observability Foundations and Practices*.  
- *A Novel Spatial Data Pipeline for Orchestrating Apache NiFi/MiNiFi*. [IGI Global](https://www.igi-global.com/article/a-novel-spatial-data-pipeline-for-orchestrating-apache-nifiminifi/333164)


