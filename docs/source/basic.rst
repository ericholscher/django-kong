===========
Django Kong
===========


What is the point
-----------------

Kong came about to solve a problem. At the Lawrence Journal-World, we have over 20 sites that we maintain that run a couple different versions of software that we make. Every time we wanted to push code live, we had no good way of making sure that we didn't break shit, other than hand testing sites or spidering them. Kong is a middle ground in between those 2 approaches, allowing you to specify certain behaviors that you want to test across all of your sites. By using Twill as the language, it lets us do interesting things like fill out forms and follow links, providing you with interesting ways of testing that your sites are functioning correctly after a deployment.


A simple example
-----------------

You can see a `basic version <http://kong.ericholscher.com>`_ running for my personal site. It is super barebones, but it should give you an idea of what exactly is possible.


Get the code
-------------

The `source <http://github.com/ericholscher/django-kong>`_ is available on Github. A 0.1 release will be uploaded to Pypi soon, after a few of the blemishes have been worked out. I would like to thank `Nathan Borror <http://nathanborror.com>`_ for the design parts that are pretty :)


What's with the name?
----------------------

Originally Kong was called paradigm, because it was going to change the way we thought about deployment. After much convincing from coworkers that this was too enterprisey, during the Djangocon 09 sprints, I was given the name Donkey Kong. I thought it would be a fun play on words to name a project django kong, because it sounds like Djangocon, and it plays off of Donkey Kong. Then I just needed to find a way to associate Kong with what the project actually does, because it's a Deployment Testing Tool for King/Donkey Kong sized sites :)
