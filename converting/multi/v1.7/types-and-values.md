## Types and Values

jq supports the same set of datatypes as JSON - numbers,
strings, booleans, arrays, objects (which in JSON-speak are
hashes with only string keys), and "null".

Booleans, null, strings and numbers are written the same way as
in JSON. Just like everything else in jq, these simple
values take an input and produce an output - `42` is a valid jq
expression that takes an input, ignores it, and returns 42
instead.

Numbers in jq are internally represented by their IEEE754 double
precision approximation. Any arithmetic operation with numbers,
whether they are literals or results of previous filters, will
produce a double precision floating point result.

However, when parsing a literal jq will store the original literal
string. If no mutation is applied to this value then it will make
to the output in its original form, even if conversion to double
would result in a loss.

### Array construction: `[]`

As in JSON, `[]` is used to construct arrays, as in
`[1,2,3]`. The elements of the arrays can be any jq
expression, including a pipeline. All of the results produced
by all of the expressions are collected into one big array.
You can use it to construct an array out of a known quantity
of values (as in `[.foo, .bar, .baz]`) or to "collect" all the
results of a filter into an array (as in `[.items[].name]`)

Once you understand the "," operator, you can look at jq's array
syntax in a different light: the expression `[1,2,3]` is not using a
built-in syntax for comma-separated arrays, but is instead applying
the `[]` operator (collect results) to the expression 1,2,3 (which
produces three different results).

If you have a filter `X` that produces four results,
then the expression `[X]` will produce a single result, an
array of four elements.

program:
```jq
[.user, .projects[]]
```
input:
```json
{"user":"stedolan", "projects": ["jq", "wikiflow"]}
```
output:
```json
["stedolan", "jq", "wikiflow"]
```
program:
```jq
[ .[] | . * 2]
```
input:
```json
[1, 2, 3]
```
output:
```json
[2, 4, 6]
```
### Object Construction: `{}`

Like JSON, `{}` is for constructing objects (aka
dictionaries or hashes), as in: `{"a": 42, "b": 17}`.

If the keys are "identifier-like", then the quotes can be left
off, as in `{a:42, b:17}`.  Variable references as key
expressions use the value of the variable as the key.  Key
expressions other than constant literals, identifiers, or
variable references, need to be parenthesized, e.g.,
`{("a"+"b"):59}`.

The value can be any expression (although you may need to wrap
it in parentheses if, for example, it contains colons), which
gets applied to the {} expression's input (remember, all
filters have an input and an output).

    {foo: .bar}

will produce the JSON object `{"foo": 42}` if given the JSON
object `{"bar":42, "baz":43}` as its input. You can use this
to select particular fields of an object: if the input is an
object with "user", "title", "id", and "content" fields and
you just want "user" and "title", you can write

    {user: .user, title: .title}

Because that is so common, there's a shortcut syntax for it:
`{user, title}`.

If one of the expressions produces multiple results,
multiple dictionaries will be produced. If the input's

    {"user":"stedolan","titles":["JQ Primer", "More JQ"]}

then the expression

    {user, title: .titles[]}

will produce two outputs:

    {"user":"stedolan", "title": "JQ Primer"}
    {"user":"stedolan", "title": "More JQ"}

Putting parentheses around the key means it will be evaluated as an
expression. With the same input as above,

    {(.user): .titles}

produces

    {"stedolan": ["JQ Primer", "More JQ"]}

Variable references as keys use the value of the variable as
the key.  Without a value then the variable's name becomes the
key and its value becomes the value,

    "f o o" as $foo | "b a r" as $bar | {$foo, $bar:$foo}

produces

    {"foo":"f o o","b a r":"f o o"}

program:
```jq
{user, title: .titles[]}
```
input:
```json
{"user":"stedolan","titles":["JQ Primer", "More JQ"]}
```
output:
```json
{"user":"stedolan", "title": "JQ Primer"}
{"user":"stedolan", "title": "More JQ"}
```
program:
```jq
{(.user): .titles}
```
input:
```json
{"user":"stedolan","titles":["JQ Primer", "More JQ"]}
```
output:
```json
{"stedolan": ["JQ Primer", "More JQ"]}
```
### Recursive Descent: `..`

Recursively descends `.`, producing every value.  This is the
same as the zero-argument `recurse` builtin (see below).  This
is intended to resemble the XPath `//` operator.  Note that
`..a` does not work; use `.. | .a` instead.  In the example
below we use `.. | .a?` to find all the values of object keys
"a" in any object found "below" `.`.

This is particularly useful in conjunction with `path(EXP)`
(also see below) and the `?` operator.

program:
```jq
.. | .a?
```
input:
```json
[[{"a":1}]]
```
output:
```json
1
```