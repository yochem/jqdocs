## Basic filters
### Identity: `.`

The absolute simplest filter is `.` .  This is a filter that
takes its input and produces it unchanged as output.  That is,
this is the identity operator.

Since jq by default pretty-prints all output, this trivial
program can be a useful way of formatting JSON output from,
say, `curl`.

program:
```jq
.
```
input:
```json
"Hello, world!"
```
output:
```json
"Hello, world!"
```
### Object Identifier-Index: `.foo`, `.foo.bar`

The simplest *useful* filter is `.foo`. When given a
JSON object (aka dictionary or hash) as input, it produces
the value at the key "foo", or null if there's none present.

A filter of the form `.foo.bar` is equivalent to `.foo|.bar`.

This syntax only works for simple, identifier-like keys, that
is, keys that are all made of alphanumeric characters and
underscore, and which do not start with a digit.

If the key contains special characters or starts with a digit,
you need to surround it with double quotes like this:
`."foo$"`, or else `.["foo$"]`.

For example `.["foo::bar"]` and `.["foo.bar"]` work while
`.foo::bar` does not, and `.foo.bar` means `.["foo"].["bar"]`.

program:
```jq
.foo
```
input:
```json
{"foo": 42, "bar": "less interesting data"}
```
output:
```json
42
```
program:
```jq
.foo
```
input:
```json
{"notfoo": true, "alsonotfoo": false}
```
output:
```json
null
```
program:
```jq
.["foo"]
```
input:
```json
{"foo": 42}
```
output:
```json
42
```
### Optional Object Identifier-Index: `.foo?`

Just like `.foo`, but does not output an error when `.` is not an
object.

program:
```jq
.foo?
```
input:
```json
{"foo": 42, "bar": "less interesting data"}
```
output:
```json
42
```
program:
```jq
.foo?
```
input:
```json
{"notfoo": true, "alsonotfoo": false}
```
output:
```json
null
```
program:
```jq
.["foo"]?
```
input:
```json
{"foo": 42}
```
output:
```json
42
```
program:
```jq
[.foo?]
```
input:
```json
[1,2]
```
output:
```json
[]
```
### Object Index: `.[<string>]`

You can also look up fields of an object using syntax like
`.["foo"]` (`.foo` above is a shorthand version of this, but
only for identifier-like strings).

### Array Index: `.[<number>]`

When the index value is an integer, `.[<number>]` can index
arrays.  Arrays are zero-based, so `.[2]` returns the third
element.

Negative indices are allowed, with -1 referring to the last
element, -2 referring to the next to last element, and so on.

program:
```jq
.[0]
```
input:
```json
[{"name":"JSON", "good":true}, {"name":"XML", "good":false}]
```
output:
```json
{"name":"JSON", "good":true}
```
program:
```jq
.[2]
```
input:
```json
[{"name":"JSON", "good":true}, {"name":"XML", "good":false}]
```
output:
```json
null
```
program:
```jq
.[-2]
```
input:
```json
[1,2,3]
```
output:
```json
2
```
### Array/String Slice: `.[<number>:<number>]`

The `.[<number>:<number>]` syntax can be used to return a
subarray of an array or substring of a string. The array
returned by `.[10:15]` will be of length 5, containing the
elements from index 10 (inclusive) to index 15 (exclusive).
Either index may be negative (in which case it counts
backwards from the end of the array), or omitted (in which
case it refers to the start or end of the array).
Indices are zero-based.

program:
```jq
.[2:4]
```
input:
```json
["a","b","c","d","e"]
```
output:
```json
["c", "d"]
```
program:
```jq
.[2:4]
```
input:
```json
"abcdefghi"
```
output:
```json
"cd"
```
program:
```jq
.[:3]
```
input:
```json
["a","b","c","d","e"]
```
output:
```json
["a", "b", "c"]
```
program:
```jq
.[-2:]
```
input:
```json
["a","b","c","d","e"]
```
output:
```json
["d", "e"]
```
### Array/Object Value Iterator: `.[]`

If you use the `.[index]` syntax, but omit the index
entirely, it will return *all* of the elements of an
array. Running `.[]` with the input `[1,2,3]` will produce the
numbers as three separate results, rather than as a single
array. A filter of the form `.foo[]` is equivalent to
`.foo | .[]`.

You can also use this on an object, and it will return all
the values of the object.

program:
```jq
.[]
```
input:
```json
[{"name":"JSON", "good":true}, {"name":"XML", "good":false}]
```
output:
```json
{"name":"JSON", "good":true}
{"name":"XML", "good":false}
```
program:
```jq
.[]
```
input:
```json
[]
```
output:
```json
```
program:
```jq
.foo[]
```
input:
```json
{"foo":[1,2,3]}
```
output:
```json
1
2
3
```
program:
```jq
.[]
```
input:
```json
{"a": 1, "b": 1}
```
output:
```json
1
1
```
### `.[]?`

Like `.[]`, but no errors will be output if . is not an array
or object. A filter of the form `.foo[]?` is equivalent to
`.foo | .[]?`.

### Comma: `,`

If two filters are separated by a comma, then the
same input will be fed into both and the two filters' output
value streams will be concatenated in order: first, all of the
outputs produced by the left expression, and then all of the
outputs produced by the right. For instance, filter `.foo,
.bar`, produces both the "foo" fields and "bar" fields as
separate outputs.

program:
```jq
.foo, .bar
```
input:
```json
{"foo": 42, "bar": "something else", "baz": true}
```
output:
```json
42
"something else"
```
program:
```jq
.user, .projects[]
```
input:
```json
{"user":"stedolan", "projects": ["jq", "wikiflow"]}
```
output:
```json
"stedolan"
"jq"
"wikiflow"
```
program:
```jq
.[4,2]
```
input:
```json
["a","b","c","d","e"]
```
output:
```json
"e"
"c"
```
### Pipe: `|`

The | operator combines two filters by feeding the output(s) of
the one on the left into the input of the one on the right. It's
pretty much the same as the Unix shell's pipe, if you're used to
that.

If the one on the left produces multiple results, the one on
the right will be run for each of those results. So, the
expression `.[] | .foo` retrieves the "foo" field of each
element of the input array.

Note that `.a.b.c` is the same as `.a | .b | .c`.

Note too that `.` is the input value at the particular stage
in a "pipeline", specifically: where the `.` expression appears.
Thus `.a | . | .b` is the same as `.a.b`, as the `.` in the
middle refers to whatever value `.a` produced.

program:
```jq
.[] | .name
```
input:
```json
[{"name":"JSON", "good":true}, {"name":"XML", "good":false}]
```
output:
```json
"JSON"
"XML"
```
### Parenthesis

Parenthesis work as a grouping operator just as in any typical
programming language.

program:
```jq
(. + 2) * 5
```
input:
```json
1
```
output:
```json
15
```