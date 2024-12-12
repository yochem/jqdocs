## Builtin operators and functions

Some jq operators (for instance, `+`) do different things
depending on the type of their arguments (arrays, numbers,
etc.). However, jq never does implicit type conversions. If you
try to add a string to an object you'll get an error message and
no result.

### Addition: `+`

The operator `+` takes two filters, applies them both
to the same input, and adds the results together. What
"adding" means depends on the types involved:

- **Numbers** are added by normal arithmetic.

- **Arrays** are added by being concatenated into a larger array.

- **Strings** are added by being joined into a larger string.

- **Objects** are added by merging, that is, inserting all
    the key-value pairs from both objects into a single
    combined object. If both objects contain a value for the
    same key, the object on the right of the `+` wins.

`null` can be added to any value, and returns the other
value unchanged.

program:
```jq
.a + 1
```
input:
```json
{"a": 7}
```
output:
```json
8
```
program:
```jq
.a + .b
```
input:
```json
{"a": [1,2], "b": [3,4]}
```
output:
```json
[1,2,3,4]
```
program:
```jq
.a + null
```
input:
```json
{"a": 1}
```
output:
```json
1
```
program:
```jq
.a + 1
```
input:
```json
{}
```
output:
```json
1
```
program:
```jq
{a: 1} + {b: 2} + {c: 3} + {a: 42}
```
input:
```json
null
```
output:
```json
{"a": 42, "b": 2, "c": 3}
```
### Subtraction: `-`

As well as normal arithmetic subtraction on numbers, the `-`
operator can be used on arrays to remove all occurrences of
the second array's elements from the first array.

program:
```jq
4 - .a
```
input:
```json
{"a":3}
```
output:
```json
1
```
program:
```jq
. - ["xml", "yaml"]
```
input:
```json
["xml", "yaml", "json"]
```
output:
```json
["json"]
```
### Multiplication, division: `*` and `/`

These operators only work on numbers, and do the expected.

program:
```jq
10 / . * 3
```
input:
```json
5
```
output:
```json
6
```
### `length`

The builtin function `length` gets the length of various
different types of value:

- The length of a **string** is the number of Unicode
  codepoints it contains (which will be the same as its
  JSON-encoded length in bytes if it's pure ASCII).

- The length of an **array** is the number of elements.

- The length of an **object** is the number of key-value pairs.

- The length of **null** is zero.

program:
```jq
.[] | length
```
input:
```json
[[1,2], "string", {"a":2}, null]
```
output:
```json
2
6
1
0
```
### `keys`

The builtin function `keys`, when given an object, returns
its keys in an array.

The keys are sorted "alphabetically", by unicode codepoint
order. This is not an order that makes particular sense in
any particular language, but you can count on it being the
same for any two objects with the same set of keys,
regardless of locale settings.

When `keys` is given an array, it returns the valid indices
for that array: the integers from 0 to length-1.

program:
```jq
keys
```
input:
```json
{"abc": 1, "abcd": 2, "Foo": 3}
```
output:
```json
["Foo", "abc", "abcd"]
```
program:
```jq
keys
```
input:
```json
[42,3,35]
```
output:
```json
[0,1,2]
```
### `has`

The builtin function `has` returns whether the input object
has the given key, or the input array has an element at the
given index.

`has($key)` has the same effect as checking whether `$key`
is a member of the array returned by `keys`, although `has`
will be faster.

program:
```jq
map(has("foo"))
```
input:
```json
[{"foo": 42}, {}]
```
output:
```json
[true, false]
```
program:
```jq
map(has(2))
```
input:
```json
[[0,1], ["a","b","c"]]
```
output:
```json
[false, true]
```
### `to_entries`, `from_entries`, `with_entries(f)`

These functions convert between an object and an array of
key-value pairs. If `to_entries` is passed an object, then
for each `k: v` entry in the input, the output array
includes `{"key": k, "value": v}`.

`from_entries` does the opposite conversion, and
`with_entries(f)` is a shorthand for `to_entries | map(f) |
from_entries`, useful for doing some operation to all keys
and values of an object.

program:
```jq
to_entries
```
input:
```json
{"a": 1, "b": 2}
```
output:
```json
[{"key":"a", "value":1}, {"key":"b", "value":2}]
```
program:
```jq
from_entries
```
input:
```json
[{"key":"a", "value":1}, {"key":"b", "value":2}]
```
output:
```json
{"a": 1, "b": 2}
```
program:
```jq
with_entries(.key |= "KEY_" + .)
```
input:
```json
{"a": 1, "b": 2}
```
output:
```json
{"KEY_a": 1, "KEY_b": 2}
```
### `select`

The function `select(foo)` produces its input unchanged if
`foo` returns true for that input, and produces no output
otherwise.

It's useful for filtering lists: '`[1,2,3] | map(select(. >= 2))`'
will give you `[3]`.

program:
```jq
map(select(. >= 2))
```
input:
```json
[1,5,3,0,7]
```
output:
```json
[5,3,7]
```
### `empty`

`empty` returns no results. None at all. Not even `null`.

It's useful on occasion. You'll know if you need it :)

program:
```jq
1, empty, 2
```
input:
```json
null
```
output:
```json
1
2
```
program:
```jq
[1,2,empty,3]
```
input:
```json
null
```
output:
```json
[1,2,3]
```
### `map(f)`

For any filter `f`, `map(f)` will run that filter for each
element of the input array, and produce the outputs a new
array. `map(.+1)` will increment each element of an array of numbers.

`map(f)` is equivalent to `[.[] | f]`. In fact, this is how
it's defined.

program:
```jq
map(.+1)
```
input:
```json
[1,2,3]
```
output:
```json
[2,3,4]
```
### `add`

The filter `add` takes as input an array, and produces as
output the elements of the array added together. This might
mean summed, concatenated or merged depending on the types
of the elements of the input array - the rules are the same
as those for the `+` operator (described above).

If the input is an empty array, `add` returns `null`.

program:
```jq
add
```
input:
```json
["a","b","c"]
```
output:
```json
"abc"
```
program:
```jq
add
```
input:
```json
[1, 2, 3]
```
output:
```json
6
```
program:
```jq
add
```
input:
```json
[]
```
output:
```json
null
```
### `range`

The `range` function produces a range of numbers. `range(4;10)`
produces 6 numbers, from 4 (inclusive) to 10 (exclusive). The numbers
are produced as separate outputs. Use `[range(4;10)]` to get a range as
an array.

program:
```jq
range(2;4)
```
input:
```json
null
```
output:
```json
2
3
```
program:
```jq
[range(2;4)]
```
input:
```json
null
```
output:
```json
[2,3]
```
### `tonumber`

The `tonumber` function parses its input as a number. It
will convert correctly-formatted strings to their numeric
equivalent, leave numbers alone, and give an error on all other input.

program:
```jq
.[] | tonumber
```
input:
```json
[1, "1"]
```
output:
```json
1
1
```
### `tostring`

The `tostring` function prints its input as a
string. Strings are left unchanged, and all other values are
JSON-encoded.

program:
```jq
.[] | tostring
```
input:
```json
[1, "1", [1]]
```
output:
```json
"1"
"1"
"[1]"
```
### `type`

The `type` function returns the type of its argument as a
string, which is one of null, boolean, number, string, array
or object.

program:
```jq
map(type)
```
input:
```json
[0, false, [], {}, null, "hello"]
```
output:
```json
["number", "boolean", "array", "object", "null", "string"]
```
### `sort`, `sort_by`

The `sort` functions sorts its input, which must be an
array. Values are sorted in the following order:

* `null`
* `false`
* `true`
* numbers
* strings, in alphabetical order (by unicode codepoint value)
* arrays, in lexical order
* objects

The ordering for objects is a little complex: first they're
compared by comparing their sets of keys (as arrays in
sorted order), and if their keys are equal then the values
are compared key by key.

`sort_by` may be used to sort by a particular field of an
object, or by applying any jq filter. `sort_by(foo)`
compares two elements by comparing the result of `foo` on
each element.

program:
```jq
sort
```
input:
```json
[8,3,null,6]
```
output:
```json
[null,3,6,8]
```
program:
```jq
sort_by(.foo)
```
input:
```json
[{"foo":4, "bar":10}, {"foo":3, "bar":100}, {"foo":2, "bar":1}]
```
output:
```json
[{"foo":2, "bar":1}, {"foo":3, "bar":100}, {"foo":4, "bar":10}]
```
### `group_by`

`group_by(.foo)` takes as input an array, groups the
elements having the same `.foo` field into separate arrays,
and produces all of these arrays as elements of a larger
array, sorted by the value of the `.foo` field.

Any jq expression, not just a field access, may be used in
place of `.foo`. The sorting order is the same as described
in the `sort` function above.

program:
```jq
group_by(.foo)
```
input:
```json
[{"foo":1, "bar":10}, {"foo":3, "bar":100}, {"foo":1, "bar":1}]
```
output:
```json
[[{"foo":1, "bar":10}, {"foo":1, "bar":1}], [{"foo":3, "bar":100}]]
```
### `min`, `max`, `min_by`, `max_by`

Find the minimum or maximum element of the input array. The
`_by` versions allow you to specify a particular field or
property to examine, e.g. `min_by(.foo)` finds the object
with the smallest `foo` field.

program:
```jq
min
```
input:
```json
[5,4,2,7]
```
output:
```json
2
```
program:
```jq
max_by(.foo)
```
input:
```json
[{"foo":1, "bar":14}, {"foo":2, "bar":3}]
```
output:
```json
{"foo":2, "bar":3}
```
### `unique`

The `unique` function takes as input an array and produces
an array of the same elements, in sorted order, with
duplicates removed.

program:
```jq
unique
```
input:
```json
[1,2,5,3,5,3,1,3]
```
output:
```json
[1,2,3,5]
```
### `reverse`

This function reverses an array.

program:
```jq
reverse
```
input:
```json
[1,2,3,4]
```
output:
```json
[4,3,2,1]
```
### `contains`

The filter `contains(b)` will produce true if b is
completely contained within the input. A string B is
contained in a string A if B is a substring of A. An array B
is contained in an array A is all elements in B are
contained in any element in A. An object B is contained in
object A if all of the values in B are contained in the
value in A with the same key. All other types are assumed to
be contained in each other if they are equal.

program:
```jq
contains("bar")
```
input:
```json
"foobar"
```
output:
```json
true
```
program:
```jq
contains(["baz", "bar"])
```
input:
```json
["foobar", "foobaz", "blarp"]
```
output:
```json
true
```
program:
```jq
contains(["bazzzzz", "bar"])
```
input:
```json
["foobar", "foobaz", "blarp"]
```
output:
```json
false
```
program:
```jq
contains({foo: 12, bar: [{barp: 12}]})
```
input:
```json
{"foo": 12, "bar":[1,2,{"barp":12, "blip":13}]}
```
output:
```json
true
```
program:
```jq
contains({foo: 12, bar: [{barp: 15}]})
```
input:
```json
{"foo": 12, "bar":[1,2,{"barp":12, "blip":13}]}
```
output:
```json
false
```
### `recurse`

The `recurse` function allows you to search through a
recursive structure, and extract interesting data from all
levels. Suppose your input represents a filesystem:

    {"name": "/", "children": [
      {"name": "/bin", "children": [
        {"name": "/bin/ls", "children": []},
        {"name": "/bin/sh", "children": []}]},
      {"name": "/home", "children": [
        {"name": "/home/stephen", "children": [
          {"name": "/home/stephen/jq", "children": []}]}]}]}

Now suppose you want to extract all of the filenames
present. You need to retrieve `.name`, `.children[].name`,
`.children[].children[].name`, and so on. You can do this
with:

    recurse(.children[]) | .name

program:
```jq
recurse(.foo[])
```
input:
```json
{"foo":[{"foo": []}, {"foo":[{"foo":[]}]}]}
```
output:
```json
{"foo":[{"foo":[]},{"foo":[{"foo":[]}]}]}
{"foo":[]}
{"foo":[{"foo":[]}]}
{"foo":[]}
```
### String interpolation: `\(exp)`

Inside a string, you can put an expression inside parens
after a backslash. Whatever the expression returns will be
interpolated into the string.

program:
```jq
"The input was \(.), which is one less than \(.+1)"
```
input:
```json
42
```
output:
```json
"The input was 42, which is one less than 43"
```
### Format strings and escaping

The `@foo` syntax is used to format and escape strings,
which is useful for building URLs, documents in a language
like HTML or XML, and so forth. `@foo` can be used as a
filter on its own, the possible escapings are:

* `@text`:

  Calls `tostring`, see that function for details.

* `@json`:

  Serialises the input as JSON.

* `@html`:

  Applies HTML/XML escaping, by mapping the characters
  `<>&'"` to their entity equivalents `&lt;`, `&gt;`,
  `&amp;`, `&apos;`, `&quot;`.

* `@uri`:

  Applies percent-encoding, by mapping all reserved URI
  characters to a `%xx` sequence.

* `@csv`:

  The input must be an array, and it is rendered as CSV
  with double quotes for strings, and quotes escaped by
  repetition.

* `@sh`:

  The input is escaped suitable for use in a command-line
  for a POSIX shell. If the input is an array, the output
  will be a series of space-separated strings.

* `@base64`:

  The input is converted to base64 as specified by RFC 4648.

This syntax can be combined with string interpolation in a
useful way. You can follow a `@foo` token with a string
literal. The contents of the string literal will *not* be
escaped. However, all interpolations made inside that string
literal will be escaped. For instance,

    @uri "https://www.google.com/search?q=\(.search)"

will produce the following output for the input
`{"search":"jq!"}`:

    https://www.google.com/search?q=jq%21

Note that the slashes, question mark, etc. in the URL are
not escaped, as they were part of the string literal.

program:
```jq
@html
```
input:
```json
"This works if x < y"
```
output:
```json
"This works if x &lt; y"
```
program:
```jq
@sh "echo \(.)"
```
input:
```json
"O'Hara's Ale"
```
output:
```json
"echo 'O'\\''Hara'\\''s Ale'"
```