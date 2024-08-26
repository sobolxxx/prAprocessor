# prAprocessor

A language agnostic C like preprocessor.

## name

The name prAprocessor stands for "preprocessor for anything". It's intent is to provide C like preprocessor syntax for any language without modifying that language syntax. The directives, like #define, #ifdef etc. can be put in comments, thus no requirements other than possibility to write commands in a specific language.

## version

Currently prAprocessor is under development.

## example

Let's say that in react jsx file we want to disable some specific parts of code in production release:

```
createRoot(document.getElementById("root")).render(

  // #ifndef PROD
  <StrictMode>
    {/* #endif */}

    <App />

    {/* #ifdef PROD */}
  </StrictMode>
  // #endif

);
```

## contribution

You're welcome to contribute. Create an issue with requests or fork and pull request your proposed changes.\
Rules for pull requests:

- add only things that make sense for this tool, I want to keep it small and clean
- add tests, I want it to be reliable
- don't add 3rd party libraries if not absolutely necessary
- keep your code clean, readable and CLs small
- write good description of the CL - what, why and how if needed. Use amend if made a mistake.
