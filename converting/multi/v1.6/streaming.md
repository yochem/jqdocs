## Streaming

With the `--stream` option jq can parse input texts in a streaming
fashion, allowing jq programs to start processing large JSON texts
immediately rather than after the parse completes.  If you have a
single JSON text that is 1GB in size, streaming it will allow you
to process it much more quickly.

However, streaming isn't easy to deal with as the jq program will
have `[<path>, <leaf-value>]` (and a few other forms) as inputs.

Several builtins are provided to make handling streams easier.

The examples below use the streamed form of `[0,[1]]`, which is
`[[0],0],[[1,0],1],[[1,0]],[[1]]`.

Streaming forms include `[<path>, <leaf-value>]` (to indicate any
scalar value, empty array, or empty object), and `[<path>]` (to
indicate the end of an array or object).  Future versions of jq
run with `--stream` and `--seq` may output additional forms such
as `["error message"]` when an input text fails to parse.

### `truncate_stream(stream_expression)`

Consumes a number as input and truncates the corresponding
number of path elements from the left of the outputs of the
given streaming expression.

program:
```jq
truncate_stream([[0],1],[[1,0],2],[[1,0]],[[1]])
```
input:
```json
1
```
output:
```json
[[0],2]
[[0]]
```
### `fromstream(stream_expression)`

Outputs values corresponding to the stream expression's
outputs.

program:
```jq
fromstream(1|truncate_stream([[0],1],[[1,0],2],[[1,0]],[[1]]))
```
input:
```json
null
```
output:
```json
[2]
```
### `tostream`

The `tostream` builtin outputs the streamed form of its input.

program:
```jq
. as $dot|fromstream($dot|tostream)|.==$dot
```
input:
```json
[0,[1,{"a":1},{"b":2}]]
```
output:
```json
true
```