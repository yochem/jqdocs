## Invoking jq

jq filters run on a stream of JSON data. The input to jq is
parsed as a sequence of whitespace-separated JSON values which
are passed through the provided filter one at a time. The
output(s) of the filter are written to standard output, as a
sequence of newline-separated JSON data.

Note: it is important to mind the shell's quoting rules.  As a
general rule it's best to always quote (with single-quote
characters) the jq program, as too many characters with special
meaning to jq are also shell meta-characters.  For example, `jq
"foo"` will fail on most Unix shells because that will be the same
as `jq foo`, which will generally fail because `foo is not
defined`.  When using the Windows command shell (cmd.exe) it's
best to use double quotes around your jq program when given on the
command-line (instead of the `-f program-file` option), but then
double-quotes in the jq program need backslash escaping.

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

* `--online-input` / `-I`:

  When the top-level input value is an array produce its elements
  instead of the array.  This allows on-line processing of
  potentially very large top-level arrays' elements.

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

* `--sort-keys` / `-S`:

  Output the fields of each object with the keys in sorted order.

* `--color-output` / `-C` and `--monochrome-output` / `-M`:

  By default, jq outputs colored JSON if writing to a
  terminal. You can force it to produce color even if writing to
  a pipe or a file using `-C`, and disable color with `-M`.

* `--unbuffered`:

  Flush the output after each JSON object is printed (useful if
  you're piping a slow data source into jq and piping jq's
  output elsewhere).

* `-f filename` / `--from-file filename`:

  Read filter from the file rather than from a command line, like
  awk's -f option. You can also use '#' to make comments.

* `--arg name value`:

  This option passes a value to the jq program as a predefined
  variable. If you run jq with `--arg foo bar`, then `$foo` is
  available in the program and has the value `"bar"`.

* `--argfile name filename`:

  This option passes the first value from the named file as a
  value to the jq program as a predefined variable. If you run jq
  with `--argfile foo bar`, then `$foo` is available in the
  program and has the value resulting from parsing the content of
  the file named `bar`.

* `--exit-status` / `-e`:

  Sets the exit status of jq to 0 if the last output value was
  neither `false` nor `null`, 1 if the last output value was
  either `false` or `null`, or 4 if no valid result was ever
  produced.  Normally jq exits with 2 if there was any usage
  problem or system error, 3 if there was a jq program compile
  error, or 0 if the jq program ran.

* `--version` / `-V`:

  Output the jq version and exit with zero.

* `--help` / `-h`:

  Output the jq help and exit with zero.
