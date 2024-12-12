## Regular expressions

jq uses the Oniguruma regular expression library, as do PHP,
Ruby, TextMate, Sublime Text, etc, so the description here
will focus on jq specifics.

The jq regex filters are defined so that they can be used using
one of these patterns:

    STRING | FILTER(REGEX)
    STRING | FILTER(REGEX; FLAGS)
    STRING | FILTER([REGEX])
    STRING | FILTER([REGEX, FLAGS])

where:

* STRING, REGEX, and FLAGS are jq strings and subject to jq string interpolation;
* REGEX, after string interpolation, should be a valid regular expression;
* FILTER is one of `test`, `match`, or `capture`, as described below.

FLAGS is a string consisting of one of more of the supported flags:

* `g` - Global search (find all matches, not just the first)
* `i` - Case insensitive search
* `m` - Multi line mode (`.` will match newlines)
* `n` - Ignore empty matches
* `p` - Both s and m modes are enabled
* `s` - Single line mode (`^` -> `\A`, `$` -> `\Z`)
* `l` - Find longest possible matches
* `x` - Extended regex format (ignore whitespace and comments)

To match a whitespace with the `x` flag, use `\s`, e.g.

    jq -n '"a b" | test("a\\sb"; "x")'

Note that certain flags may also be specified within REGEX, e.g.

    jq -n '("test", "TEst", "teST", "TEST") | test("(?i)te(?-i)st")'

evaluates to: `true`, `true`, `false`, `false`.

### `test(val)`, `test(regex; flags)`

Like `match`, but does not return match objects, only `true` or `false`
for whether or not the regex matches the input.

program:
```jq
test("foo")
```
input:
```json
"foo"
```
output:
```json
true
```
program:
```jq
.[] | test("a b c # spaces are ignored"; "ix")
```
input:
```json
["xabcd", "ABC"]
```
output:
```json
true
true
```
### `match(val)`, `match(regex; flags)`

**match** outputs an object for each match it finds.  Matches have
the following fields:

* `offset` - offset in UTF-8 codepoints from the beginning of the input
* `length` - length in UTF-8 codepoints of the match
* `string` - the string that it matched
* `captures` - an array of objects representing capturing groups.

Capturing group objects have the following fields:

* `offset` - offset in UTF-8 codepoints from the beginning of the input
* `length` - length in UTF-8 codepoints of this capturing group
* `string` - the string that was captured
* `name` - the name of the capturing group (or `null` if it was unnamed)

Capturing groups that did not match anything return an offset of -1

program:
```jq
match("(abc)+"; "g")
```
input:
```json
"abc abc"
```
output:
```json
{"offset": 0, "length": 3, "string": "abc", "captures": [{"offset": 0, "length": 3, "string": "abc", "name": null}]}
{"offset": 4, "length": 3, "string": "abc", "captures": [{"offset": 4, "length": 3, "string": "abc", "name": null}]}
```
program:
```jq
match("foo")
```
input:
```json
"foo bar foo"
```
output:
```json
{"offset": 0, "length": 3, "string": "foo", "captures": []}
```
program:
```jq
match(["foo", "ig"])
```
input:
```json
"foo bar FOO"
```
output:
```json
{"offset": 0, "length": 3, "string": "foo", "captures": []}
{"offset": 8, "length": 3, "string": "FOO", "captures": []}
```
program:
```jq
match("foo (?<bar123>bar)? foo"; "ig")
```
input:
```json
"foo bar foo foo  foo"
```
output:
```json
{"offset": 0, "length": 11, "string": "foo bar foo", "captures": [{"offset": 4, "length": 3, "string": "bar", "name": "bar123"}]}
{"offset": 12, "length": 8, "string": "foo  foo", "captures": [{"offset": -1, "length": 0, "string": null, "name": "bar123"}]}
```
program:
```jq
[ match("."; "g")] | length
```
input:
```json
"abc"
```
output:
```json
3
```
### `capture(val)`, `capture(regex; flags)`

Collects the named captures in a JSON object, with the name
of each capture as the key, and the matched string as the
corresponding value.

program:
```jq
capture("(?<a>[a-z]+)-(?<n>[0-9]+)")
```
input:
```json
"xyzzy-14"
```
output:
```json
{ "a": "xyzzy", "n": "14" }
```
### `scan(regex)`, `scan(regex; flags)`

Emit a stream of the non-overlapping substrings of the input
that match the regex in accordance with the flags, if any
have been specified.  If there is no match, the stream is empty.
To capture all the matches for each input string, use the idiom
`[ expr ]`, e.g. `[ scan(regex) ]`.

program:
```jq
scan("c")
```
input:
```json
"abcdefabc"
```
output:
```json
"c"
"c"
```
### `split(regex; flags)`

For backwards compatibility, `split` splits on a string, not a regex.

program:
```jq
split(", *"; null)
```
input:
```json
"ab,cd, ef"
```
output:
```json
["ab","cd","ef"]
```
### `splits(regex)`, `splits(regex; flags)`

These provide the same results as their `split` counterparts,
but as a stream instead of an array.

program:
```jq
splits(", *")
```
input:
```json
"ab,cd,   ef, gh"
```
output:
```json
"ab"
"cd"
"ef"
"gh"
```
### `sub(regex; tostring)` `sub(regex; string; flags)`

Emit the string obtained by replacing the first match of regex in the
input string with `tostring`, after interpolation.  `tostring` should
be a jq string, and may contain references to named captures. The
named captures are, in effect, presented as a JSON object (as
constructed by `capture`) to `tostring`, so a reference to a captured
variable named "x" would take the form: `"\(.x)"`.

program:
```jq
sub("[^a-z]*(?<x>[a-z]+)"; "Z\(.x)"; "g")
```
input:
```json
"123abc456def"
```
output:
```json
"ZabcZdef"
```
### `gsub(regex; string)`, `gsub(regex; string; flags)`

`gsub` is like `sub` but all the non-overlapping occurrences of the regex are
replaced by the string, after interpolation.

program:
```jq
gsub("(?<x>.)[^a]*"; "+\(.x)-")
```
input:
```json
"Abcabc"
```
output:
```json
"+A-+a-"
```