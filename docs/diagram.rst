Diagramme de classe PALM Tracer
===============================

Ces diagrammes présentent les principales classes et leurs relations.
Les attributs et les méthodes sont volontairement masqués afin de privilégier une vue synthétique de l'architecture.

.. Diagrammes au format dot avec ``python docs/tools/generate_class_diagrams.py``.

Cœur applicatif
---------------

Le premier diagramme regroupe l'orchestration, les traitements, les résultats, les outils et les interfaces graphiques de PALM Tracer.


.. graphviz:: _static/graph/classes_palm_tracer.dot
   :alt: Diagramme de classe PALM Tracer
   :align: center
   :caption: Diagramme de classe PALM Tracer


Groupes de paramètres
---------------------

Le deuxième diagramme présente la hiérarchie des groupes qui structurent la configuration des différentes étapes du traitement.


.. graphviz:: _static/graph/classes_groups.dot
   :alt: Diagramme des groupes de paramètres PALM Tracer
   :align: center
   :caption: Diagramme des groupes de paramètres PALM Tracer


Types de paramètres
--------------------

Le dernier diagramme présente les types de paramètres réutilisables et leur hiérarchie.


.. graphviz:: _static/graph/classes_types.dot
   :alt: Diagramme des types de paramètres PALM Tracer
   :align: center
   :caption: Diagramme des types de paramètres PALM Tracer
