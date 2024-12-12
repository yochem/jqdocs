## Invoking jq

jq filters run on a stream of JSON data. The input to jq is
parsed as a sequence of whitespace-separated JSON values which
are passed through the provided filter one at a time. The
output(s) of the filter are written to standard output, as a
sequence of newline-separated JSON data.

You can affect how jq reads and writes its input and output
using some command-line options:

* `--null-input` / `-n`:

  Don't read any input at all. Instead, the filter is run once
  using `null` as the input. This is useful when using jq as a
  simple calculator or to construct JSON data from scratch.

* `--raw-input` / `-R`:

  Don't parse the input as JSON. Instead, each line of text is
  passed to the filter as a string. If combined with `--slurp`,
  then the entire input is passed to the filter as a single long
  string.

* `--slurp` / `-s`:

  Instead of running the filter for each JSON object in the
  input, read the entire input stream into a large array and run
  the filter just once.

* `--compact-output` / `-c`:

  By default, jq pretty-prints JSON output. Using this option
  will result in more compact output by instead putting each
  JSON object on a single line.

* `--raw-output` / `-r`:

  With this option, if the filter's result is a string then it
  will be written directly to standard output rather than being
  formatted as a JSON string with quotes. This can be useful for
  making jq filters talk to non-JSON-based systems.

* `--ascii-output` / `-a`:

  jq usually outputs non-ASCII Unicode codepoints as UTF-8, even
  if the input specified them as escape sequences (like
  "\u03bc"). Using this option, you can force jq to produce pure
  ASCII output with every non-ASCII character replaced with the
  equivalent escape sequence.

* `--color-output` / `-C` and `--monochrome-output` / `-M`:

  By default, jq outputs colored JSON if writing to a
  terminal. You can force it to produce color even if writing to
  a pipe or a file using `-C`, and disable color with `-M`.

* `--arg name value`:

  This option passes a value to the jq program as a predefined
  variable. If you run jq with `--arg foo bar`, then `$foo` is
  available in the program and has the value `"bar"`.
