# pytest-hot-test
Hot reload with Pytest

Work in Progress.

Ambicious Goal: map the dependencies of tests, and skip tests that have no dependencies modified

How? Not all details are yet sorted out, but here's the summary:

1. Analyse collected items (test files) source code
2. Find all dependencies from main code that are imported into the test file
3. Analyse the imported modules, recursively, to determine which source files are used in the implementation
4. Compute the hashes of all source files, and check if any of the dependencies (source files), and check if they changed
5. If they changed, do nothing (test as normal)
6. Else, add them to the ignore list

Note: this plugin does not aim at adding the auto execute functionality, this can be done out of the box with other plugins.

At the moment, the project is still being developed - it works locally, but is not yet packaged to installed / used in other projects (work todo)

![ezgif com-gif-maker-2](https://user-images.githubusercontent.com/5386983/206796931-ce4e9be8-4858-4aae-85b9-034ffda91046.gif)
