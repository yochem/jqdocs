## I/O

At this time jq has minimal support for I/O, mostly in the
form of control over when inputs are read.  Two builtins functions
are provided for this, `input` and `inputs`, that read from the
same sources (e.g., `stdin`, files named on the command-line) as
jq itself.  These two builtins, and jq's own reading actions, can
be interleaved with each other.  They are commonly used in combination
with the null input option `-n` to prevent one input from being read
implicitly.

Two builtins provide minimal output capabilities, `debug`, and
`stderr`.  (Recall that a jq program's output values are always
output as JSON texts on `stdout`.) The `debug` builtin can have
application-specific behavior, such as for executables that use
the libjq C API but aren't the jq executable itself.  The `stderr`
builtin outputs its input in raw mode to stder with no additional
decoration, not even a newline.

Most jq builtins are referentially transparent, and yield constant
and repeatable value streams when applied to constant inputs.
This is not true of I/O builtins.

### `input`

Outputs one new input.

Note that when using `input` it is generally be necessary to
invoke jq with the `-n` command-line option, otherwise
the first entity will be lost.

    echo 1 2 3 4 | jq '[., input]' # [1,2] [3,4]

### `inputs`

Outputs all remaining inputs, one by one.

This is primarily useful for reductions over a program's
inputs.  Note that when using `inputs` it is generally necessary
to invoke jq with the `-n` command-line option, otherwise
the first entity will be lost.

    echo 1 2 3 | jq -n 'reduce inputs as $i (0; . + $i)' # 6

### `debug`, `debug(msgs)`

These two filters are like `.` but have as a side-effect the
production of one or more messages on stderr.

The message produced by the `debug` filter has the form

    ["DEBUG:",<input-value>]

where `<input-value>` is a compact rendition of the input
value.  This format may change in the future.

The `debug(msgs)` filter is defined as `(msgs | debug | empty), .`
thus allowing great flexibility in the content of the message,
while also allowing multi-line debugging statements to be created.

For example, the expression:

    1 as $x | 2 | debug("Entering function foo with $x == \($x)", .) | (.+1)

would produce the value 3 but with the following two lines
being written to stderr:

    ["DEBUG:","Entering function foo with $x == 1"]
    ["DEBUG:",2]

### `stderr`

Prints its input in raw and compact mode to stderr with no
additional decoration, not even a newline.

### `input_filename`

Returns the name of the file whose input is currently being
filtered.  Note that this will not work well unless jq is
running in a UTF-8 locale.

### `input_line_number`

Returns the line number of the input currently being filtered.
