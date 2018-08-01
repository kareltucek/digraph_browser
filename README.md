tree graph viewer
=================
This is a simple dot graph browser designed for browsing of small parts of large directed graphs. The motivation is browsing of call graphs constructed via tools like callgrind or egypt. 

I.e., the graph begins totally folded. Clickling on nodes unfolds small number of layers and optimizes the positions via a set of spring-like operators. I.e., the layout changes in continuous manner when browsing the graph.

This might be dirty reinvention of wheel, yet the tools I have come across (dotty, xdot as well as some bigger projects) did not seem tu support the required functionality.

NOTE that however the parsing format is inspired by the standard dot language, it is not compatible with its advanced features! 
