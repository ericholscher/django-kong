Meta Documentation
==================

What is the point
-----------------

Kong came about to solve a problem. At the Lawrence Journal-World, we have over 20 sites that we maintain that run a couple different versions of software that we make. Every time we wanted to push code live, we had no good way of making sure that we didn't break shit, other than hand testing sites or spidering them. Kong is a middle ground in between those 2 approaches, allowing you to specify certain behaviors that you want to test across all of your sites. By using Twill as the language, it lets us do interesting things like fill out forms and follow links, providing you with interesting ways of testing that your sites are functioning correctly after a deployment.
