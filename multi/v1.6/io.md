## I/O

At this time jq has minimal support for I/O, mostly in the
form of control over when inputs are read.  Two builtins functions
are provided for this, `input` and `inputs`, that read from the
same sources (e.g., `stdin`, files named on the command-line) as
jq itself.  These two builtins, and jq's own reading actions, can
be interleaved with each other.

Two builtins provide minimal output capabilities, `debug`, and
`stderr`.  (Recall that a jq program's output values are always
output as JSON texts on `stdout`.)  The `debug` builtin can have
application-specific behavior, such as for executables that use
the libjq C API but aren't the jq executable itself.  The `stderr`
builtin outputs its input in raw mode to stder with no additional
decoration, not even a newline.

Most jq builtins are referentially transparent, and yield constant
and repeatable value streams when applied to constant inputs.
This is not true of I/O builtins.

### `input`

Outputs one new input.

    echo 1 2 3 4 | jq '[., input]' # [1,2] [3,4]

### `inputs`

Outputs all remaining inputs, one by one.

This is primarily useful for reductions over a program's
inputs.

    echo 1 2 3 | jq -n 'reduce inputs as $i (0; . + $i)' # 6

### `debug`

Causes a debug message based on the input value to be
produced.  The jq executable wraps the input value with
`["DEBUG:", <input-value>]` and prints that and a newline on
stderr, compactly.  This may change in the future.

### `stderr`

Prints its input in raw and compact mode to stderr with no
additional decoration, not even a newline.

### `input_filename`

Returns the name of the file whose input is currently being
filtered.  Note that this will not work well unless jq is
running in a UTF-8 locale.

### `input_line_number`

Returns the line number of the input currently being filtered.
