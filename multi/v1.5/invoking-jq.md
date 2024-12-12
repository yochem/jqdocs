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

* `--compact-output` / `-c`:

  By default, jq pretty-prints JSON output. Using this option
  will result in more compact output by instead putting each
  JSON object on a single line.

* `--raw-output` / `-r`:

  With this option, if the filter's result is a string then it
  will be written directly to standard output rather than being
  formatted as a JSON string with quotes. This can be useful for
  making jq filters talk to non-JSON-based systems.

* `--join-output` / `-j`:

  Like `-r` but jq won't print a newline after each output.

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

* `--tab`:

  Use a tab for each indentation level instead of two spaces.

* `--indent n`:

  Use the given number of spaces (no more than 7) for indentation.

* `--unbuffered`:

  Flush the output after each JSON object is printed (useful if
  you're piping a slow data source into jq and piping jq's
  output elsewhere).

* `--stream`:

  Parse the input in streaming fashion, outputting arrays of path
  and leaf values (scalars and empty arrays or empty objects).
  For example, `"a"` becomes `[[],"a"]`, and `[[],"a",["b"]]`
  becomes `[[0],[]]`, `[[1],"a"]`, and `[[2,0],"b"]`.

  This is useful for processing very large inputs.  Use this in
  conjunction with filtering and the `reduce` and `foreach` syntax
  to reduce large inputs incrementally.

* `--seq`:

  Use the `application/json-seq` MIME type scheme for separating
  JSON texts in jq's input and output.  This means that an ASCII
  RS (record separator) character is printed before each value on
  output and an ASCII LF (line feed) is printed after every
  output.  Input JSON texts that fail to parse are ignored (but
  warned about), discarding all subsequent input until the next
  RS.  This mode also parses the output of jq without the `--seq`
  option.

* `-f filename` / `--from-file filename`:

  Read filter from the file rather than from a command line, like
  awk's -f option. You can also use '#' to make comments.

* `-L directory`:

  Prepend `directory` to the search list for modules.  If this
  option is used then no builtin search list is used.  See the
  section on modules below.

* `--arg name value`:

  This option passes a value to the jq program as a predefined
  variable. If you run jq with `--arg foo bar`, then `$foo` is
  available in the program and has the value `"bar"`. Note that
  `value` will be treated as a string, so `--arg foo 123` will
  bind `$foo` to `"123"`.

* `--argjson name JSON-text`:

  This option passes a JSON-encoded value to the jq program as a
  predefined variable. If you run jq with `--argjson foo 123`, then
  `$foo` is available in the program and has the value `123`.

* `--slurpfile variable-name filename`:

  This option reads all the JSON texts in the named file and binds
  an array of the parsed JSON values to the given global variable.
  If you run jq with `--slurpfile foo bar`, then `$foo` is available
  in the program and has an array whose elements correspond to the
  texts in the file named `bar`.

* `--argfile variable-name filename`:

  Do not use.  Use `--slurpfile` instead.

  (This option is like `--slurpfile`, but when the file has just
  one text, then that is used, else an array of texts is used as
  in `--slurpfile`.)

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

* `--run-tests [filename]`:

  Runs the tests in the given file or standard input.  This must
  be the last option given and does not honor all preceding
  options.  The input consists of comment lines, empty lines, and
  program lines followed by one input line, as many lines of
  output as are expected (one per output), and a terminating empty
  line.  Compilation failure tests start with a line containing
  only `%%FAIL`, then a line containing the program to compile,
  then a line containing an error message to compare to the
  actual.

  Be warned that this option can change backwards-incompatibly.
