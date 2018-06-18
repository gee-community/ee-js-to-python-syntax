# ee-js-to-python-syntax
Simplistic conversion of earthengine JavaScript to Python syntax.

**Very** preliminary proof of concept for a package that enables easy conversion of
earth engine JavaScript examples to Python syntax.

Potentially [jiphy](https://github.com/timothycrosley/jiphy) is usful, although
it seems to be un-maintained.

So far RegEx is used to convert general JS syntax to Python equilvilent.

General Python frontmatter is added.

TODO:
+ Why do some of the regex rules not always convert?
+ Dealing with line breaks does not always work
+ Comments within line breaks, break python.  
+ Conversion of ee API calls that are not similar between JS and Python, 
such as plotting, run tasks, ect. 


## Example
see `test_eejs2python_colab.ipynb` in [Colab](https://colab.research.google.com)
