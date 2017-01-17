.. _circle:

Circle
======

Represents a circle. A circle is a :ref:`role` that is broken down into sub roles. Every circle has core roles (e.g. facilitator, secretary, lead link, rep link, cross link) as well as custom roles. A :ref:`partner` can be assigned to a circle as a core member.

.. qrefflask:: swarm_intelligence_app.app:application
  :endpoints: circle

|

.. autoflask:: swarm_intelligence_app.app:application
  :endpoints: circle

Members
--------------

Represents the members of a circle. See :ref:`partner` for a description of a single member.

.. qrefflask:: swarm_intelligence_app.app:application
  :endpoints: circlemembers, circlemembersassociation

|

.. autoflask:: swarm_intelligence_app.app:application
  :endpoints: circlemembers, circlemembersassociation

Roles
------

Represents the roles of a circle. See :ref:`role` for a description of a single role.

.. qrefflask:: swarm_intelligence_app.app:application
  :endpoints: circleroles

|

.. autoflask:: swarm_intelligence_app.app:application
  :endpoints: circleroles
