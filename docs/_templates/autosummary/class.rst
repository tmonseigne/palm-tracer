{{ fullname | escape }}
{{ '=' * fullname|length }}

.. autoclass:: {{ fullname }}
   :show-inheritance:

{% if attributes %}
Attributs
---------

.. autosummary::
   {% for item in attributes %}
   {{ item }}
   {% endfor %}
{% endif %}

{% if methods %}
Méthodes
--------

.. autosummary::
   {% for item in methods %}
   {{ item }}
   {% endfor %}
{% endif %}
