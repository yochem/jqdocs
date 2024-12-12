## Advanced features
Variables are an absolute necessity in most programming languages, but
they're relegated to an "advanced feature" in jq.

In most languages, variables are the only means of passing around
data. If you calculate a value, and you want to use it more than once,
you'll need to store it in a variable. To pass a value to another part
of the program, you'll need that part of the program to define a
variable (as a function parameter, object member, or whatever) in
which to place the data.

It is also possible to define functions in jq, although this is
is a feature whose biggest use is defining jq's standard library
(many jq functions such as `map` and `select` are in fact written
in jq).

Finally, jq has a `reduce` operation, which is very powerful but a
bit tricky. Again, it's mostly used internally, to define some
useful bits of jq's standard library.

### Variables

In jq, all filters have an input and an output, so manual
plumbing is not necessary to pass a value from one part of a program
to the next. Many expressions, for instance `a + b`, pass their input
to two distinct subexpressions (here `a` and `b` are both passed the
same input), so variables aren't usually necessary in order to use a
value twice.

For instance, calculating the average value of an array of numbers
requires a few variables in most languages - at least one to hold the
array, perhaps one for each element or for a loop counter. In jq, it's
simply `add / length` - the `add` expression is given the array and
produces its sum, and the `length` expression is given the array and
produces its length.

So, there's generally a cleaner way to solve most problems in jq than
defining variables. Still, sometimes they do make things easier, so jq
lets you define variables using `expression as $variable`. All
variable names start with `$`. Here's a slightly uglier version of the
array-averaging example:

    length as $array_length | add / $array_length

We'll need a more complicated problem to find a situation where using
variables actually makes our lives easier.


Suppose we have an array of blog posts, with "author" and "title"
fields, and another object which is used to map author usernames to
real names. Our input looks like:

    {"posts": [{"title": "First post", "author": "anon"},
               {"title": "A well-written article", "author": "person1"}],
     "realnames": {"anon": "Anonymous Coward",
                   "person1": "Person McPherson"}}

We want to produce the posts with the author field containing a real
name, as in:

    {"title": "First post", "author": "Anonymous Coward"}
    {"title": "A well-written article", "author": "Person McPherson"}

We use a variable, $names, to store the realnames object, so that we
can refer to it later when looking up author usernames:

    .realnames as $names | .posts[] | {title, author: $names[.author]}

The expression `exp as $x | ...` means: for each value of expression
`exp`, run the rest of the pipeline with the entire original input, and
with `$x` set to that value.  Thus `as` functions as something of a
foreach loop.

Variables are scoped over the rest of the expression that defines
them, so

    .realnames as $names | (.posts[] | {title, author: $names[.author]})

will work, but

    (.realnames as $names | .posts[]) | {title, author: $names[.author]}

won't.

program:
```jq
.bar as $x | .foo | . + $x
```
input:
```json
{"foo":10, "bar":200}
```
output:
```json
210
```
### Defining Functions

You can give a filter a name using "def" syntax:

    def increment: . + 1;

From then on, `increment` is usable as a filter just like a
builtin function (in fact, this is how some of the builtins
are defined). A function may take arguments:

    def map(f): [.[] | f];

Arguments are passed as filters, not as values. The
same argument may be referenced multiple times with
different inputs (here `f` is run for each element of the
input array). Arguments to a function work more like
callbacks than like value arguments.

If you want the value-argument behaviour for defining simple
functions, you can just use a variable:

    def addvalue(f): f as $value | map(. + $value);

With that definition, `addvalue(.foo)` will add the current
input's `.foo` field to each element of the array.

program:
```jq
def addvalue(f): . + [f]; map(addvalue(.[0]))
```
input:
```json
[[1,2],[10,20]]
```
output:
```json
[[1,2,1], [10,20,10]]
```
program:
```jq
def addvalue(f): f as $x | map(. + $x); addvalue(.[0])
```
input:
```json
[[1,2],[10,20]]
```
output:
```json
[[1,2,1,2], [10,20,1,2]]
```
### `reduce`

The `reduce` syntax allows you to combine all of the results of
an expression by accumulating them into a single answer.
The form is `reduce EXP as $var (INIT; UPDATE)`.
As an example, we'll pass `[1,2,3]` to this expression:

    reduce .[] as $item (0; . + $item)

For each result that `.[]` produces, `. + $item` is run to
accumulate a running total, starting from 0 as the input value.
In this example, `.[]` produces the results `1`, `2`, and `3`,
so the effect is similar to running something like this:

    0 | 1 as $item | . + $item |
        2 as $item | . + $item |
        3 as $item | . + $item

program:
```jq
reduce .[] as $item (0; . + $item)
```
input:
```json
[1,2,3,4,5]
```
output:
```json
15
```