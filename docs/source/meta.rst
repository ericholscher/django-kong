Meta Documentation
==================

What is the point
-----------------

Kong came about to solve a problem. At the Lawrence Journal-World, we have over 20 sites that we maintain that run a couple different versions of software that we make. Every time we wanted to push code live, we had no good way of making sure that we didn't break shit, other than hand testing sites or spidering them. Kong is a middle ground in between those 2 approaches, allowing you to specify certain behaviors that you want to test across all of your sites. By using Twill as the language, it lets us do interesting things like fill out forms and follow links, providing you with interesting ways of testing that your sites are functioning correctly after a deployment.

Basic Architecture
------------------

Kong has two main top-level ideas. `Site`s and `Types`. A `Type` is a collection of `Site`s. When you define a test, you either define it for a Type of site -- which will then apply to every Site in that Type. You can also assign a test to a specific Site, for something that is custom functionality for that site. The idea is to define tests mostly on Type's, which will then automatically be run against all sites added to that Type. Then for special cased functionality, you can run that on only a collection of 1 or 2 sites.
