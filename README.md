<a href="super-tiny-compiler.py"><img width="731" alt="THE SUPER TINY COMPILER" src="https://cloud.githubusercontent.com/assets/952783/14413766/134c4068-ff39-11e5-996e-9452973299c2.png"/></a>

***Welcome to The Super Tiny Compiler!***

This is a Python version of [The Super Tiny Compiler](https://github.com/thejameskyle/the-super-tiny-compiler) originally developed in JavaScript by [@thejameskyle](https://github.com/thejameskyle)

Although I must admit I did tweaks to it:
* Right and left Parenthesis on the tokenizer are treated as 2 separated token types, to simplify a condition on the parser.
* Didn't liked how the visitor map of functions in the `transformer` function looked like with lambda's, so I wroted it as functions so It'll look more tidy.
* Usage of Python placeholders on the `codeGeneration` function

---

Distributed under the same license as author, because I know nothing about licenses.

[![cc-by-4.0](https://licensebuttons.net/l/by/4.0/80x15.png)](http://creativecommons.org/licenses/by/4.0/)
