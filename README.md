# Divisibilty via ~~regexes~~ abominations

This repository contains a single Python script with one sordid purpose: to create regular expressions that test a number *n* in base *b* for divisibility by a divisor *d*. Horrifying, right?

The basis for these ~~regexes~~ abominations are Deterministic Finite Automata, a type of state machine that accepts symbols that transition it from state to state. A DFA that accepts only divisible numbers is simple to construct, and a description of this process can be found [here](https://codegolf.stackexchange.com/a/3505/75773). 

The Python script within this repository can do one of two things: 
* It can generate a `.jff` file containing a DFA for divisibility, which should then be imported into [JFLAP](http://www.jflap.org/) for conversion to a plain regex. However, formal language ~~regexes~~ abominations use a different syntax than programmer regexes., which means you will have to find & replace all `+` characters with `|` characters to get a usable regex.
* It can, directly from the command line, generate a regex using recursion that is *much* smaller and faster than the JFLAP version. However, this regex will (obviously) only work in a regex engine that supports recursion.

Godspeed and have fun

### Why

As with many projects, the original inspiration for project was a simple thought: why am I not dead yet. However, unwilling and unable to take matters into my own hands, I decided that generating ~~regexes~~ abominations of obscene size and complexity with no usefulness whatsoever was the next best thing.

### Credits
The inspiration for this project came from the stack overflow post linked above. I noticed numerous people presenting their already constructed ~~regexes~~ abominations, but no simple and thorough process that allows someone with little knowledge about formal languages to construct their own ~~regexes~~ abominations.

### Licensing Stuff
If you post any of these regexes to a forum or stack exchange, please link people here. I worked reasonably hard on this and ~~bought~~ downloaded an ebook on formal languages just to complete this project.