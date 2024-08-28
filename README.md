# prAprocessor

A language agnostic C like preprocessor.

## Name

The name prAprocessor stands for "preprocessor for anything". It's intent is to provide C like preprocessor syntax for any language without modifying that language syntax. The directives, like #define, #ifdef etc. can be put in comments, thus no requirements other than possibility to write commands in a specific language.\
\
The name is also a kind of nerd joke - pra suggests its something old(school), just like C <3

## Version

Currently prAprocessor is under development.

## Example

Let's say that in react jsx file we want to disable some specific parts of code in production release:

```
createRoot(document.getElementById("root")).render(

  // #ifndef PROD#
  <StrictMode>
    {/* #endif# */}

    <App />

    {/* #ifdef PROD# */}
  </StrictMode>
  // #endif#

);
```

## Design choices

- A concious design choice to end each preprocessor directive with a # (unlike in C, where directives end with endline) comes from the fact that the tool is supposed to be language agnostic. This means, that in some languages, directives will be placed inside comment sections that have an ending, for example /\* #define X=10# \*/
- In current version, multiple directives in single line are not allowed, although it's a plan for the future as ending character for the directive described above allows it. In other words, currently /\* #ifdef X# \*/ some_code(); /\* #endif# \*/ is not allowed, but the plan is that it will be in the future.

## How does it work - architecture overview

A.K.A quickstart guide.

### Flow

First, always the config is loaded - the config sets up how the script will run further on.\
\
There are two possible modes - normal single run default mode, and watch mode.\
\
In single run mode, first the target directory is cleared. All files are deleted. Thus be careful with this operation as it might be dangerous!\
Next, for each file (recursive) in source directory a copy of that file is created inside target directory. The output files are already preprocessed.\
\
In watch mode, first a full run is done as described above. Later, the watch is turned on, and the script observes source directory for changes, preprocessess them if needed and saves output to target dir.

### Context

Context stores two types of information.\
\
First one is all declared preprocessor variables. For example, if there is a defined variable in config file, or there is a variable passed from CLI, or #define VAR_NAME# is encountered in source dir, this information is stored in context.\
\
There are two types of variables:

- global - a variable that is either passed from CLI or defined in config. Such variable will be exactly the same for all processed files.
- local - a variable defined inside a file using #define ...#. Such variable is local only to this file. In the future there is a plan to make something similar to #include from C, which would allow to share local variables among files.\

Local and global variables are stored in local and global context inside Context class. Both are dictionaries.\
\
Second type of information stored in Context is information about cutting out parts of code. The ifdefed function return True if currently processed code should be cut out, and False otherwise.\
\
Because there is a possibility that directives can be nested, like this:

```
#ifdef A#
  #ifdef B#
    #ifdef C#
      do_something()
    #endif# <- C
  #endif# <- B
#endif# <- A
```

The ifdefed value is actually a stack of pairs <VAR_NAME, current_state>, where current state is information whether at this point ifdefed should return True or False.\
\
For the example above, the stack calls would be like this:

```
#define A#
#define C#

#ifdef A#  -> push("A", False) False, because A is defined
  #ifdef B# -> push("B", True) True, because B is not defined
    #ifdef C# -> push("C", True) True, because there is already True on stack
      do_something() -> this will be cut out as top of the stack is True
    #endif# <- C -> pop() - still top of the stack is True, we are inside #ifdef B#
  #endif# <- B -> pop() - top of the stack if now False, we are inside #ifdef A#
#endif# <- A -> pop() - stack is now empty aka ifdefed returns False
```

### Handlers

For each directive there is a handler that handles this directive behaviour. They are defined in directives.py and mapped from string to function in handlers variable. Dispatching happens in get_directive called from handle_line.

### run_full

Full run (deletion of target directory and parsing all files in source) is handled in run_full() function. There is a crawler implemention going through all files in source directory and calling handle_single_file_callback callback.

### run_watch

Turns on watch mode. Currently has to be killed with ctrl+c / cmd+c.\
Uses 3rd party watchdog.

## Contribution

You're welcome to contribute. Create an issue with requests or fork and pull request your proposed changes.\
Rules for pull requests:

- add only things that make sense for this tool, I want to keep it small and clean
- add tests, I want it to be reliable
- don't add 3rd party libraries if not absolutely necessary
- keep your code clean, readable and CLs small
- write good description of the CL - what, why and how if needed. Use amend if made a mistake.
