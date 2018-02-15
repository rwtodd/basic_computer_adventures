# Web Versions

After making the python versions of __neptune__ and __orient___, I thought it might
be fun to see what a bare-bones web version would look like.  I did a version of 
__neptune__ in Typescript, which worked well (it is deleted now but lives on in the 
history of this repo if you want to go looking for it).  But, then I started reading
about all the ES6 features that have landed in browsers lately, and wanted to try
out plain JS modules and async/await.  So, I converted the typescript to plain javascript.

I was very impressed (I am used to doing modules by wrapping the whole file in a closure, 
which works fine but is ugly and cumbersome)... javascript has really come a long way.
Async/await is a _very_ natural fit for converting BASIC terminal programs that expect
to be able to wait for a user to press `ENTER` before continuing.


