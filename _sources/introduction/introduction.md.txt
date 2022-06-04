# What is brane ?

Brane is designed to provide a rich I/O management system in the Python programming.
The goals are

* to avoid setting the common arguments or processings on the I/O events
* to be allowed to track data flows

Then, we can save time (quick), get less human errors (stable), use everywhere (reusable), may easily find I/O related bugs (reproduction) and make codes readable.


## What will brane solves ?

In several cases, we have similar small but many boilarplates on reading or writing objects such as

* using `with` statement to open and close the files
* checking the method's name and its arguments' names or orderings
* giving fixed arugments to modules or methods
* making directories before saving files
* loading multiple csv files, concatenating them and optimizing 
* loading images and resizing them in a fixed shape
* writing tables


Brane aims to mitigates these boring or troublesome things by unifying the interfaces and configuring them.
In other words, it realizes the DRY priciple for I/O.

## What does brane means ?

First of all, you should not mind it too much.
Honestly speaking, there is no deep meaning on it but here let me describe it as it implies !

The terminology "brane" comes from the string theory which is considered to be the most possible theory unifying the general relativity (the most established theory of the gravitation) and the quantum field theory (the most established theory on the micro world, to say, particle physics).
There, branes were found as the boudaries or the sources/sinks of the strings which are elementary objects in the (perturbative) string theory as the name suggests.
The other intersting aspect of the branes is a universal soliton or an extend object of the strings.

Now, go back to our programing world which might be artificially at first sight far from the string worlds.
There, the most fundamental actors may be data.
However, data is originally abstract to some extent but needed to be saved as files at storages in some format.
To say, data is absorbed or emitted from the file system what strings to branes (really ?).
And, both serve as some extensible and unifying roles.
That is the reason why the brane comes to our module name.

# Features of brane

## Unified I/O interface

First of all, we provide extension or data type free I/O interfaces.

Secondly, we can handle multiple files in the same interface.




## Hook system

In many cases, we do common preprocessings on reading objects from files or writing objects into files.
In such situations, we apply the same fucntions to the objects or the paths/files before/after I/O operations.
Hook systems in brane help us to do so.


## I/O tracking

* Not implemented yet






















# What is brane ?

Brane is designed to provide a rich I/O management system in the Python programming.
The goals are

* to avoid setting the common arguments or processings on the I/O events
* to be allowed to track data flows

Then, we can save time, get less human error and make codes readable.

## What will brane solves ?

In several cases, we have similar small but many boilarplates on reading or writing objects such as

* using `with` statement to open and close the files
* checking the method's name and its arguments' names or orderings
* giving fixed arugments to modules or methods
* making directories before saving files
* loading multiple csv files, concatenating them and optimizing 
* loading images and resizing them in a fixed shape
* writing tables


Brane aims to mitigates these boring or troublesome things by unifying the interfaces and configuring them.

# Features of brane

## Unified I/O interface

First of all, we provide extension or data type free I/O interfaces.

Secondly, we can handle multiple files in the same interface.




## Hook system

In many cases, we do common preprocessings on reading objects from files or writing objects into files.
In such situations, we apply the same fucntions to the objects or the paths/files before/after I/O operations.
Hook systems in brane help us to do so.


## I/O tracking

* Not implemented yet


