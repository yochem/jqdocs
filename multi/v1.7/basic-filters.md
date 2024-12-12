## Basic filters
### Identity: `.`

The absolute simplest filter is `.` .  This filter takes its
input and produces the same value as output.  That is, this
is the identity operator.

Since jq by default pretty-prints all output, a trivial
program consisting of nothing but `.` can be used to format
JSON output from, say, `curl`.

Although the identity filter never modifies the value of its
input, jq processing can sometimes make it appear as though
it does.  For example, using the current implementation of
jq, we would see that the expression:

    1E1234567890 | .

produces `1.7976931348623157e+308` on at least one platform.
This is because, in the process of parsing the number, this
particular version of jq has converted it to an IEEE754
double-precision representation, losing precision.

The way in which jq handles numbers has changed over time
and further changes are likely within the parameters set by
the relevant JSON standards.  The following remarks are
therefore offered with the understanding that they are
intended to be descriptive of the current version of jq and
should not be interpreted as being prescriptive:

(1) Any arithmetic operation on a number that has not
already been converted to an IEEE754 double precision
representation will trigger a conversion to the IEEE754
representation.

(2) jq will attempt to maintain the original decimal
precision of number literals, but in expressions such
`1E1234567890`, precision will be lost if the exponent is
too large.

(3) In jq programs, a leading minus sign will trigger the
conversion of the number to an IEEE754 representation.

(4) Comparisons are carried out using the untruncated
big decimal representation of numbers if available, as
illustrated in one of the following examples.

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
program:
```jq
.
```
input:
```json
0.12345678901234567890123456789
```
output:
```json
0.12345678901234567890123456789
```
program:
```jq
[., tojson]
```
input:
```json
12345678909876543212345
```
output:
```json
[12345678909876543212345,"12345678909876543212345"]
```
program:
```jq
. < 0.12345678901234567890123456788
```
input:
```json
0.12345678901234567890123456789
```
output:
```json
false
```
program:
```jq
map([., . == 1]) | tojson
```
input:
```json
[1, 1.000, 1.0, 100e-2]
```
output:
```json
"[[1,true],[1.000,true],[1.0,true],[1.00,true]]"
```
program:
```jq
. as $big | [$big, $big + 1] | map(. > 10000000000000000000000000000000)
```
input:
```json
10000000000000000000000000000001
```
output:
```json
[true, false]
```
### Object Identifier-Index: `.foo`, `.foo.bar`

The simplest *useful* filter has the form `.foo`. When given a
JSON object (aka dictionary or hash) as input, `.foo` produces
the value at the key "foo" if the key is present, or null otherwise.

A filter of the form `.foo.bar` is equivalent to `.foo | .bar`.

The `.foo` syntax only works for simple, identifier-like keys, that
is, keys that are all made of alphanumeric characters and
underscore, and which do not start with a digit.

If the key contains special characters or starts with a digit,
you need to surround it with double quotes like this:
`."foo$"`, or else `.["foo$"]`.

For example `.["foo::bar"]` and `.["foo.bar"]` work while
`.foo::bar` does not.

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

Note that the iterator operator is a generator of values.

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

The `,` operator is one way to construct generators.

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
similar to the Unix shell's pipe, if you're used to that.

If the one on the left produces multiple results, the one on
the right will be run for each of those results. So, the
expression `.[] | .foo` retrieves the "foo" field of each
element of the input array.  This is a cartesian product,
which can be surprising.

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