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
    same key, the object on the right of the `+` wins. (For
    recursive merge use the `*` operator.)

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
### Multiplication, division, modulo: `*`, `/`, `%`

These infix operators behave as expected when given two numbers.
Division by zero raises an error. `x % y` computes x modulo y.

Multiplying a string by a number produces the concatenation of
that string that many times. `"x" * 0` produces **null**.

Dividing a string by another splits the first using the second
as separators.

Multiplying two objects will merge them recursively: this works
like addition but if both objects contain a value for the
same key, and the values are objects, the two are merged with
the same strategy.

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
program:
```jq
. / ", "
```
input:
```json
"a, b,c,d, e"
```
output:
```json
["a","b,c,d","e"]
```
program:
```jq
{"k": {"a": 1, "b": 2}} * {"k": {"a": 0,"c": 3}}
```
input:
```json
null
```
output:
```json
{"k": {"a": 0, "b": 2, "c": 3}}
```
program:
```jq
.[] | (1 / .)?
```
input:
```json
[1,0,-1]
```
output:
```json
1
-1
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
### `keys`, `keys_unsorted`

The builtin function `keys`, when given an object, returns
its keys in an array.

The keys are sorted "alphabetically", by unicode codepoint
order. This is not an order that makes particular sense in
any particular language, but you can count on it being the
same for any two objects with the same set of keys,
regardless of locale settings.

When `keys` is given an array, it returns the valid indices
for that array: the integers from 0 to length-1.

The `keys_unsorted` function is just like `keys`, but if
the input is an object then the keys will not be sorted,
instead the keys will roughly be in insertion order.

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
### `has(key)`

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
### `in`

The builtin function `in` returns whether or not the input key is in the
given object, or the input index corresponds to an element
in the given array. It is, essentially, an inversed version
of `has`.

program:
```jq
.[] | in({"foo": 42})
```
input:
```json
["foo", "bar"]
```
output:
```json
true
false
```
program:
```jq
map(in([0,1]))
```
input:
```json
[2, 0]
```
output:
```json
[false, true]
```
### `path(path_expression)`

Outputs array representations of the given path expression
in `.`.  The outputs are arrays of strings (object keys)
and/or numbers (array indices).

Path expressions are jq expressions like `.a`, but also `.[]`.
There are two types of path expressions: ones that can match
exactly, and ones that cannot.  For example, `.a.b.c` is an
exact match path expression, while `.a[].b` is not.

`path(exact_path_expression)` will produce the array
representation of the path expression even if it does not
exist in `.`, if `.` is `null` or an array or an object.

`path(pattern)` will produce array representations of the
paths matching `pattern` if the paths exist in `.`.

Note that the path expressions are not different from normal
expressions.  The expression
`path(..|select(type=="boolean"))` outputs all the paths to
boolean values in `.`, and only those paths.

program:
```jq
path(.a[0].b)
```
input:
```json
null
```
output:
```json
["a",0,"b"]
```
program:
```jq
[path(..)]
```
input:
```json
{"a":[{"b":1}]}
```
output:
```json
[[],["a"],["a",0],["a",0,"b"]]
```
### `del(path_expression)`

The builtin function `del` removes a key and its corresponding
value from an object.

program:
```jq
del(.foo)
```
input:
```json
{"foo": 42, "bar": 9001, "baz": 42}
```
output:
```json
{"bar": 9001, "baz": 42}
```
program:
```jq
del(.[1, 2])
```
input:
```json
["foo", "bar", "baz"]
```
output:
```json
["foo"]
```
### `to_entries`, `from_entries`, `with_entries(f)`

These functions convert between an object and an array of
key-value pairs. If `to_entries` is passed an object, then
for each `k: v` entry in the input, the output array
includes `{"key": k, "value": v}`.

`from_entries` does the opposite conversion, and
`with_entries(f)` is a shorthand for `to_entries | map(f) |
from_entries`, useful for doing some operation to all keys
and values of an object. `from_entries` accepts `"key"`,
`"Key"`, `"Name"`, `"value"`, and `"Value"` as keys.

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
### `select(boolean_expression)`

The function `select(f)` produces its input unchanged if
`f` returns true for that input, and produces no output
otherwise.

It's useful for filtering lists: `[1,2,3] | map(select(. >= 2))`
will give you `[2,3]`.

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
program:
```jq
.[] | select(.id == "second")
```
input:
```json
[{"id": "first", "val": 1}, {"id": "second", "val": 2}]
```
output:
```json
{"id": "second", "val": 2}
```
### `arrays`, `objects`, `iterables`, `booleans`, `numbers`, `normals`, `finites`, `strings`, `nulls`, `values`, `scalars`

These built-ins select only inputs that are arrays, objects,
iterables (arrays or objects), booleans, numbers, normal
numbers, finite numbers, strings, null, non-null values, and
non-iterables, respectively.

program:
```jq
.[]|numbers
```
input:
```json
[[],{},1,"foo",null,true,false]
```
output:
```json
1
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
### `error`, `error(message)`

Produces an error with the input value, or with the message
given as the argument. Errors can be caught with try/catch;
see below.

When the error value is `null`, it produces nothing and works
just like `empty`. So `[null | error]` and `[error(null)]` both
emit `[]`.

program:
```jq
try error catch .
```
input:
```json
"error message"
```
output:
```json
"error message"
```
program:
```jq
try error("invalid value: \(.)") catch .
```
input:
```json
42
```
output:
```json
"invalid value: 42"
```
### `$__loc__`

Produces an object with a "file" key and a "line" key, with
the filename and line number where `$__loc__` occurs, as
values.

program:
```jq
try error("\($__loc__)") catch .
```
input:
```json
null
```
output:
```json
"{\"file\":\"<top-level>\",\"line\":1}"
```
### `map(f)`, `map_values(f)`

For any filter `f`, `map(f)` will run that filter for each
element of the input array, and return the outputs in a new
array. `map(.+1)` will increment each element of an array of numbers.

Similarly, `map_values(f)` will run that filter for each element,
but it will return an object when an object is passed.

`map(f)` is equivalent to `[.[] | f]`. In fact, this is how
it's defined. Similarly, `map_values(f)` is defined as `.[] |= f`.

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
program:
```jq
map_values(.+1)
```
input:
```json
{"a": 1, "b": 2, "c": 3}
```
output:
```json
{"a": 2, "b": 3, "c": 4}
```
### `paths`, `paths(node_filter)`, `leaf_paths`

`paths` outputs the paths to all the elements in its input
(except it does not output the empty list, representing .
itself).

`paths(f)` outputs the paths to any values for which `f` is `true`.
That is, `paths(type == "number")` outputs the paths to all numeric
values.

`leaf_paths` is an alias of `paths(scalars)`; `leaf_paths` is
*deprecated* and will be removed in the next major release.

program:
```jq
[paths]
```
input:
```json
[1,[[],{"a":2}]]
```
output:
```json
[[0],[1],[1,0],[1,1],[1,1,"a"]]
```
program:
```jq
[paths(type == "number")]
```
input:
```json
[1,[[],{"a":2}]]
```
output:
```json
[[0],[1,1,"a"]]
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
### `any`, `any(condition)`, `any(generator; condition)`

The filter `any` takes as input an array of boolean values,
and produces `true` as output if any of the elements of
the array are `true`.

If the input is an empty array, `any` returns `false`.

The `any(condition)` form applies the given condition to the
elements of the input array.

The `any(generator; condition)` form applies the given
condition to all the outputs of the given generator.

program:
```jq
any
```
input:
```json
[true, false]
```
output:
```json
true
```
program:
```jq
any
```
input:
```json
[false, false]
```
output:
```json
false
```
program:
```jq
any
```
input:
```json
[]
```
output:
```json
false
```
### `all`, `all(condition)`, `all(generator; condition)`

The filter `all` takes as input an array of boolean values,
and produces `true` as output if all of the elements of
the array are `true`.

The `all(condition)` form applies the given condition to the
elements of the input array.

The `all(generator; condition)` form applies the given
condition to all the outputs of the given generator.

If the input is an empty array, `all` returns `true`.

program:
```jq
all
```
input:
```json
[true, false]
```
output:
```json
false
```
program:
```jq
all
```
input:
```json
[true, true]
```
output:
```json
true
```
program:
```jq
all
```
input:
```json
[]
```
output:
```json
true
```
### `flatten`, `flatten(depth)`

The filter `flatten` takes as input an array of nested arrays,
and produces a flat array in which all arrays inside the original
array have been recursively replaced by their values. You can pass
an argument to it to specify how many levels of nesting to flatten.

`flatten(2)` is like `flatten`, but going only up to two
levels deep.

program:
```jq
flatten
```
input:
```json
[1, [2], [[3]]]
```
output:
```json
[1, 2, 3]
```
program:
```jq
flatten(1)
```
input:
```json
[1, [2], [[3]]]
```
output:
```json
[1, 2, [3]]
```
program:
```jq
flatten
```
input:
```json
[[]]
```
output:
```json
[]
```
program:
```jq
flatten
```
input:
```json
[{"foo": "bar"}, [{"foo": "baz"}]]
```
output:
```json
[{"foo": "bar"}, {"foo": "baz"}]
```
### `range(upto)`, `range(from; upto)`, `range(from; upto; by)`

The `range` function produces a range of numbers. `range(4; 10)`
produces 6 numbers, from 4 (inclusive) to 10 (exclusive). The numbers
are produced as separate outputs. Use `[range(4; 10)]` to get a range as
an array.

The one argument form generates numbers from 0 to the given
number, with an increment of 1.

The two argument form generates numbers from `from` to `upto`
with an increment of 1.

The three argument form generates numbers `from` to `upto`
with an increment of `by`.

program:
```jq
range(2; 4)
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
[range(2; 4)]
```
input:
```json
null
```
output:
```json
[2,3]
```
program:
```jq
[range(4)]
```
input:
```json
null
```
output:
```json
[0,1,2,3]
```
program:
```jq
[range(0; 10; 3)]
```
input:
```json
null
```
output:
```json
[0,3,6,9]
```
program:
```jq
[range(0; 10; -1)]
```
input:
```json
null
```
output:
```json
[]
```
program:
```jq
[range(0; -5; -1)]
```
input:
```json
null
```
output:
```json
[0,-1,-2,-3,-4]
```
### `floor`

The `floor` function returns the floor of its numeric input.

program:
```jq
floor
```
input:
```json
3.14159
```
output:
```json
3
```
### `sqrt`

The `sqrt` function returns the square root of its numeric input.

program:
```jq
sqrt
```
input:
```json
9
```
output:
```json
3
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
### `infinite`, `nan`, `isinfinite`, `isnan`, `isfinite`, `isnormal`

Some arithmetic operations can yield infinities and "not a
number" (NaN) values.  The `isinfinite` builtin returns `true`
if its input is infinite.  The `isnan` builtin returns `true`
if its input is a NaN.  The `infinite` builtin returns a
positive infinite value.  The `nan` builtin returns a NaN.
The `isnormal` builtin returns true if its input is a normal
number.

Note that division by zero raises an error.

Currently most arithmetic operations operating on infinities,
NaNs, and sub-normals do not raise errors.

program:
```jq
.[] | (infinite * .) < 0
```
input:
```json
[-1, 1]
```
output:
```json
true
false
```
program:
```jq
infinite, nan | type
```
input:
```json
null
```
output:
```json
"number"
"number"
```
### `sort`, `sort_by(path_expression)`

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
object, or by applying any jq filter. `sort_by(f)` compares
two elements by comparing the result of `f` on each element.
When `f` produces multiple values, it firstly compares the
first values, and the second values if the first values are
equal, and so on.

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
[{"foo":4, "bar":10}, {"foo":3, "bar":10}, {"foo":2, "bar":1}]
```
output:
```json
[{"foo":2, "bar":1}, {"foo":3, "bar":10}, {"foo":4, "bar":10}]
```
program:
```jq
sort_by(.foo, .bar)
```
input:
```json
[{"foo":4, "bar":10}, {"foo":3, "bar":20}, {"foo":2, "bar":1}, {"foo":3, "bar":10}]
```
output:
```json
[{"foo":2, "bar":1}, {"foo":3, "bar":10}, {"foo":3, "bar":20}, {"foo":4, "bar":10}]
```
### `group_by(path_expression)`

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
### `min`, `max`, `min_by(path_exp)`, `max_by(path_exp)`

Find the minimum or maximum element of the input array.

The `min_by(path_exp)` and `max_by(path_exp)` functions allow
you to specify a particular field or property to examine, e.g.
`min_by(.foo)` finds the object with the smallest `foo` field.

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
### `unique`, `unique_by(path_exp)`

The `unique` function takes as input an array and produces
an array of the same elements, in sorted order, with
duplicates removed.

The `unique_by(path_exp)` function will keep only one element
for each value obtained by applying the argument. Think of it
as making an array by taking one element out of every group
produced by `group`.

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
program:
```jq
unique_by(.foo)
```
input:
```json
[{"foo": 1, "bar": 2}, {"foo": 1, "bar": 3}, {"foo": 4, "bar": 5}]
```
output:
```json
[{"foo": 1, "bar": 2}, {"foo": 4, "bar": 5}]
```
program:
```jq
unique_by(length)
```
input:
```json
["chunky", "bacon", "kitten", "cicada", "asparagus"]
```
output:
```json
["bacon", "chunky", "asparagus"]
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
### `contains(element)`

The filter `contains(b)` will produce true if b is
completely contained within the input. A string B is
contained in a string A if B is a substring of A. An array B
is contained in an array A if all elements in B are
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
### `indices(s)`

Outputs an array containing the indices in `.` where `s`
occurs.  The input may be an array, in which case if `s` is an
array then the indices output will be those where all elements
in `.` match those of `s`.

program:
```jq
indices(", ")
```
input:
```json
"a,b, cd, efg, hijk"
```
output:
```json
[3,7,12]
```
program:
```jq
indices(1)
```
input:
```json
[0,1,2,1,3,1,4]
```
output:
```json
[1,3,5]
```
program:
```jq
indices([1,2])
```
input:
```json
[0,1,2,3,1,4,2,5,1,2,6,7]
```
output:
```json
[1,8]
```
### `index(s)`, `rindex(s)`

Outputs the index of the first (`index`) or last (`rindex`)
occurrence of `s` in the input.

program:
```jq
index(", ")
```
input:
```json
"a,b, cd, efg, hijk"
```
output:
```json
3
```
program:
```jq
index(1)
```
input:
```json
[0,1,2,1,3,1,4]
```
output:
```json
1
```
program:
```jq
index([1,2])
```
input:
```json
[0,1,2,3,1,4,2,5,1,2,6,7]
```
output:
```json
1
```
program:
```jq
rindex(", ")
```
input:
```json
"a,b, cd, efg, hijk"
```
output:
```json
12
```
program:
```jq
rindex(1)
```
input:
```json
[0,1,2,1,3,1,4]
```
output:
```json
5
```
program:
```jq
rindex([1,2])
```
input:
```json
[0,1,2,3,1,4,2,5,1,2,6,7]
```
output:
```json
8
```
### `inside`

The filter `inside(b)` will produce true if the input is
completely contained within b. It is, essentially, an
inversed version of `contains`.

program:
```jq
inside("foobar")
```
input:
```json
"bar"
```
output:
```json
true
```
program:
```jq
inside(["foobar", "foobaz", "blarp"])
```
input:
```json
["baz", "bar"]
```
output:
```json
true
```
program:
```jq
inside(["foobar", "foobaz", "blarp"])
```
input:
```json
["bazzzzz", "bar"]
```
output:
```json
false
```
program:
```jq
inside({"foo": 12, "bar":[1,2,{"barp":12, "blip":13}]})
```
input:
```json
{"foo": 12, "bar": [{"barp": 12}]}
```
output:
```json
true
```
program:
```jq
inside({"foo": 12, "bar":[1,2,{"barp":12, "blip":13}]})
```
input:
```json
{"foo": 12, "bar": [{"barp": 15}]}
```
output:
```json
false
```
### `startswith(str)`

Outputs `true` if . starts with the given string argument.

program:
```jq
[.[]|startswith("foo")]
```
input:
```json
["fo", "foo", "barfoo", "foobar", "barfoob"]
```
output:
```json
[false, true, false, true, false]
```
### `endswith(str)`

Outputs `true` if . ends with the given string argument.

program:
```jq
[.[]|endswith("foo")]
```
input:
```json
["foobar", "barfoo"]
```
output:
```json
[false, true]
```
### `combinations`, `combinations(n)`

Outputs all combinations of the elements of the arrays in the
input array. If given an argument `n`, it outputs all combinations
of `n` repetitions of the input array.

program:
```jq
combinations
```
input:
```json
[[1,2], [3, 4]]
```
output:
```json
[1, 3]
[1, 4]
[2, 3]
[2, 4]
```
program:
```jq
combinations(2)
```
input:
```json
[0, 1]
```
output:
```json
[0, 0]
[0, 1]
[1, 0]
[1, 1]
```
### `ltrimstr(str)`

Outputs its input with the given prefix string removed, if it
starts with it.

program:
```jq
[.[]|ltrimstr("foo")]
```
input:
```json
["fo", "foo", "barfoo", "foobar", "afoo"]
```
output:
```json
["fo","","barfoo","bar","afoo"]
```
### `rtrimstr(str)`

Outputs its input with the given suffix string removed, if it
ends with it.

program:
```jq
[.[]|rtrimstr("foo")]
```
input:
```json
["fo", "foo", "barfoo", "foobar", "foob"]
```
output:
```json
["fo","","bar","foobar","foob"]
```
### `explode`

Converts an input string into an array of the string's
codepoint numbers.

program:
```jq
explode
```
input:
```json
"foobar"
```
output:
```json
[102,111,111,98,97,114]
```
### `implode`

The inverse of explode.

program:
```jq
implode
```
input:
```json
[65, 66, 67]
```
output:
```json
"ABC"
```
### `split`

Splits an input string on the separator argument.

program:
```jq
split(", ")
```
input:
```json
"a, b,c,d, e, "
```
output:
```json
["a","b,c,d","e",""]
```
### `join(str)`

Joins the array of elements given as input, using the
argument as separator. It is the inverse of `split`: that is,
running `split("foo") | join("foo")` over any input string
returns said input string.

program:
```jq
join(", ")
```
input:
```json
["a","b,c,d","e"]
```
output:
```json
"a, b,c,d, e"
```
### `ascii_downcase`, `ascii_upcase`

Emit a copy of the input string with its alphabetic characters (a-z and A-Z)
converted to the specified case.

program:
```jq
ascii_upcase
```
input:
```json
"useful but not for é"
```
output:
```json
"USEFUL BUT NOT FOR é"
```
### `while(cond; update)`

The `while(cond; update)` function allows you to repeatedly
apply an update to `.` until `cond` is false.

Note that `while(cond; update)` is internally defined as a
recursive jq function.  Recursive calls within `while` will
not consume additional memory if `update` produces at most one
output for each input.  See advanced topics below.

program:
```jq
[while(.<100; .*2)]
```
input:
```json
1
```
output:
```json
[1,2,4,8,16,32,64]
```
### `until(cond; next)`

The `until(cond; next)` function allows you to repeatedly
apply the expression `next`, initially to `.` then to its own
output, until `cond` is true.  For example, this can be used
to implement a factorial function (see below).

Note that `until(cond; next)` is internally defined as a
recursive jq function.  Recursive calls within `until()` will
not consume additional memory if `next` produces at most one
output for each input.  See advanced topics below.

program:
```jq
[.,1]|until(.[0] < 1; [.[0] - 1, .[1] * .[0]])|.[1]
```
input:
```json
4
```
output:
```json
24
```
### `recurse(f)`, `recurse`, `recurse(f; condition)`, `recurse_down`

The `recurse(f)` function allows you to search through a
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

When called without an argument, `recurse` is equivalent to
`recurse(.[]?)`.

`recurse(f)` is identical to `recurse(f; . != null)` and can be
used without concerns about recursion depth.

`recurse(f; condition)` is a generator which begins by
emitting . and then emits in turn .|f, .|f|f, .|f|f|f, ...  so long
as the computed value satisfies the condition. For example,
to generate all the integers, at least in principle, one
could write `recurse(.+1; true)`.

For legacy reasons, `recurse_down` exists as an alias to
calling `recurse` without arguments. This alias is considered
*deprecated* and will be removed in the next major release.

The recursive calls in `recurse` will not consume additional
memory whenever `f` produces at most a single output for each
input.

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
program:
```jq
recurse
```
input:
```json
{"a":0,"b":[1]}
```
output:
```json
{"a":0,"b":[1]}
0
[1]
1
```
program:
```jq
recurse(. * .; . < 20)
```
input:
```json
2
```
output:
```json
2
4
16
```
### `..`

Short-hand for `recurse` without arguments.  This is intended
to resemble the XPath `//` operator.  Note that `..a` does not
work; use `..|a` instead.  In the example below we use
`..|.a?` to find all the values of object keys "a" in any
object found "below" `.`.

program:
```jq
..|.a?
```
input:
```json
[[{"a":1}]]
```
output:
```json
1
```
### `env`

Outputs an object representing jq's environment.

program:
```jq
env.PAGER
```
input:
```json
null
```
output:
```json
"less"
```
### `transpose`

Transpose a possibly jagged matrix (an array of arrays).
Rows are padded with nulls so the result is always rectangular.

program:
```jq
transpose
```
input:
```json
[[1], [2,3]]
```
output:
```json
[[1,2],[null,3]]
```
### `bsearch(x)`

`bsearch(x)` conducts a binary search for x in the input
array.  If the input is sorted and contains x, then
`bsearch(x)` will return its index in the array; otherwise, if
the array is sorted, it will return (-1 - ix) where ix is an
insertion point such that the array would still be sorted
after the insertion of x at ix.  If the array is not sorted,
`bsearch(x)` will return an integer that is probably of no
interest.

program:
```jq
bsearch(0)
```
input:
```json
[0,1]
```
output:
```json
0
```
program:
```jq
bsearch(0)
```
input:
```json
[1,2,3]
```
output:
```json
-1
```
program:
```jq
bsearch(4) as $ix | if $ix < 0 then .[-(1+$ix)] = 4 else . end
```
input:
```json
[1,2,3]
```
output:
```json
[1,2,3,4]
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
### Convert to/from JSON

The `tojson` and `fromjson` builtins dump values as JSON texts
or parse JSON texts into values, respectively.  The tojson
builtin differs from tostring in that tostring returns strings
unmodified, while tojson encodes strings as JSON strings.

program:
```jq
[.[]|tostring]
```
input:
```json
[1, "foo", ["foo"]]
```
output:
```json
["1","foo","[\"foo\"]"]
```
program:
```jq
[.[]|tojson]
```
input:
```json
[1, "foo", ["foo"]]
```
output:
```json
["1","\"foo\"","[\"foo\"]"]
```
program:
```jq
[.[]|tojson|fromjson]
```
input:
```json
[1, "foo", ["foo"]]
```
output:
```json
[1,"foo",["foo"]]
```
### Format strings and escaping

The `@foo` syntax is used to format and escape strings,
which is useful for building URLs, documents in a language
like HTML or XML, and so forth. `@foo` can be used as a
filter on its own, the possible escapings are:

* `@text`:

  Calls `tostring`, see that function for details.

* `@json`:

  Serializes the input as JSON.

* `@html`:

  Applies HTML/XML escaping, by mapping the characters
  `<>&'"` to their entity equivalents `&lt;`, `&gt;`,
  `&amp;`, `&apos;`, `&quot;`.

* `@uri`:

  Applies percent-encoding, by mapping all reserved URI
  characters to a `%XX` sequence.

* `@csv`:

  The input must be an array, and it is rendered as CSV
  with double quotes for strings, and quotes escaped by
  repetition.

* `@tsv`:

  The input must be an array, and it is rendered as TSV
  (tab-separated values). Each input array will be printed as
  a single line. Fields are separated by a single
  tab (ascii `0x09`). Input characters line-feed (ascii `0x0a`),
  carriage-return (ascii `0x0d`), tab (ascii `0x09`) and
  backslash (ascii `0x5c`) will be output as escape sequences
  `\n`, `\r`, `\t`, `\\` respectively.

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
`{"search":"what is jq?"}`:

    "https://www.google.com/search?q=what%20is%20jq%3F"

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
### Dates

jq provides some basic date handling functionality, with some
high-level and low-level builtins.  In all cases these
builtins deal exclusively with time in UTC.

The `fromdateiso8601` builtin parses datetimes in the ISO 8601
format to a number of seconds since the Unix epoch
(1970-01-01T00:00:00Z).  The `todateiso8601` builtin does the
inverse.

The `fromdate` builtin parses datetime strings.  Currently
`fromdate` only supports ISO 8601 datetime strings, but in the
future it will attempt to parse datetime strings in more
formats.

The `todate` builtin is an alias for `todateiso8601`.

The `now` builtin outputs the current time, in seconds since
the Unix epoch.

Low-level jq interfaces to the C-library time functions are
also provided: `strptime`, `strftime`, `mktime`, and `gmtime`.
Refer to your host operating system's documentation for the
format strings used by `strptime` and `strftime`.  Note: these
are not necessarily stable interfaces in jq, particularly as
to their localization functionality.

The `gmtime` builtin consumes a number of seconds since the
Unix epoch and outputs a "broken down time" representation of
time as an array of numbers representing (in this order): the
year, the month (zero-based), the day of the month, the hour
of the day, the minute of the hour, the second of the minute,
the day of the week, and the day of the year -- all one-based
unless otherwise stated.

The `mktime` builtin consumes "broken down time"
representations of time output by `gmtime` and `strptime`.

The `strptime(fmt)` builtin parses input strings matching the
`fmt` argument.  The output is in the "broken down time"
representation consumed by `mktime` and output by `gmtime`.

The `strftime(fmt)` builtin formats a time with the given
format.

The format strings for `strptime` and `strftime` are described
in typical C library documentation.  The format string for ISO
8601 datetime is `"%Y-%m-%dT%H:%M:%SZ"`.

jq may not support some or all of this date functionality on
some systems.

program:
```jq
fromdate
```
input:
```json
"2015-03-05T23:51:47Z"
```
output:
```json
1425599507
```
program:
```jq
strptime("%Y-%m-%dT%H:%M:%SZ")
```
input:
```json
"2015-03-05T23:51:47Z"
```
output:
```json
[2015,2,5,23,51,47,4,63]
```
program:
```jq
strptime("%Y-%m-%dT%H:%M:%SZ")|mktime
```
input:
```json
"2015-03-05T23:51:47Z"
```
output:
```json
1425599507
```