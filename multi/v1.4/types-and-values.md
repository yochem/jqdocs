## Types and Values

jq supports the same set of datatypes as JSON - numbers,
strings, booleans, arrays, objects (which in JSON-speak are
hashes with only string keys), and "null".

Booleans, null, strings and numbers are written the same way as
in JSON. Just like everything else in jq, these simple
values take an input and produce an output - `42` is a valid jq
expression that takes an input, ignores it, and returns 42
instead.

### Array construction: `[]`

As in JSON, `[]` is used to construct arrays, as in
`[1,2,3]`. The elements of the arrays can be any jq
expression. All of the results produced by all of the
expressions are collected into one big array. You can use it
to construct an array out of a known quantity of values (as
in `[.foo, .bar, .baz]`) or to "collect" all the results of a
filter into an array (as in `[.items[].name]`)

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
### Objects: `{}`

Like JSON, `{}` is for constructing objects (aka
dictionaries or hashes), as in: `{"a": 42, "b": 17}`.

If the keys are "sensible" (all alphabetic characters), then
the quotes can be left off. The value can be any expression
(although you may need to wrap it in parentheses if it's a
complicated one), which gets applied to the {} expression's
input (remember, all filters have an input and an
output).

    {foo: .bar}

will produce the JSON object `{"foo": 42}` if given the JSON
object `{"bar":42, "baz":43}`. You can use this to select
particular fields of an object: if the input is an object
with "user", "title", "id", and "content" fields and you
just want "user" and "title", you can write

    {user: .user, title: .title}

Because that's so common, there's a shortcut syntax: `{user, title}`.

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