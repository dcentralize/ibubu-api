.. _role:

****
Role
****

Represents a role. A role defines domains to control and accountabilities to perform. A :ref:`partner` can be assigned to core roles (e.g. facilitator, secretary, lead link, rep link, cross link) as well as custom roles.

.. qrefflask:: swarm_intelligence_app.app:application
  :endpoints: role

|

.. autoflask:: swarm_intelligence_app.app:application
  :endpoints: role

Accountabilities
----------------

Represents the accountabilities of a role. See :ref:`accountability` for a description of a single accountability.

.. qrefflask:: swarm_intelligence_app.app:application
  :endpoints: roleaccountabilities

|

.. autoflask:: swarm_intelligence_app.app:application
  :endpoints: roleaccountabilities

Circle
------

Converts a role to a :ref:`circle` and vice versa.

.. qrefflask:: swarm_intelligence_app.app:application
  :endpoints: rolecircle

|

.. autoflask:: swarm_intelligence_app.app:application
  :endpoints: rolecircle

Domains
-------

Represents the domains of a role. See :ref:`domain` for a description of a single domain.

.. qrefflask:: swarm_intelligence_app.app:application
  :endpoints: roledomains

|

.. autoflask:: swarm_intelligence_app.app:application
  :endpoints: roledomains

Members
-------

Represents the members of a role. See :ref:`partner` for a description of a single member.

.. qrefflask:: swarm_intelligence_app.app:application
  :endpoints: rolemembers, rolemembersassociation

|

.. autoflask:: swarm_intelligence_app.app:application
  :endpoints: rolemembers, rolemembersassociation
