Diagrammes de classes de PALM Tracer
====================================

Ces diagrammes présentent les principales classes et leurs relations.
Les attributs et les méthodes sont volontairement masqués afin de privilégier une vue synthétique de l'architecture.

.. Diagrammes au format dot avec ``python docs/tools/generate_class_diagrams.py``.

Cœur applicatif
---------------

Ce diagramme regroupe l'orchestration, les traitements, les résultats, la configuration et les outils de PALM Tracer.


.. graphviz:: _static/graph/classes_palm_tracer.dot
   :alt: Diagramme du cœur applicatif de PALM Tracer
   :align: center
   :caption: Diagramme du cœur applicatif de PALM Tracer


Interface graphique
-------------------

Ce diagramme présente les classes du paquet ``palm_tracer.UI``, dont les widgets Napari et les vues de résultats.


.. graphviz:: _static/graph/classes_ui.dot
   :alt: Diagramme de l'interface graphique de PALM Tracer
   :align: center
   :caption: Diagramme de l'interface graphique de PALM Tracer


Groupes de paramètres
---------------------

Ce diagramme présente la hiérarchie des groupes qui structurent la configuration des différentes étapes du traitement.


.. graphviz:: _static/graph/classes_groups.dot
   :alt: Diagramme des groupes de paramètres PALM Tracer
   :align: center
   :caption: Diagramme des groupes de paramètres PALM Tracer


Types de paramètres
--------------------

Ce diagramme présente les types de paramètres réutilisables et leur hiérarchie.


.. graphviz:: _static/graph/classes_types.dot
   :alt: Diagramme des types de paramètres PALM Tracer
   :align: center
   :caption: Diagramme des types de paramètres PALM Tracer
