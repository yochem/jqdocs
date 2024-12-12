## Comments

You can write comments in your jq filters using `#`.

A `#` character (not part of a string) starts a comment.
All characters from `#` to the end of the line are ignored.

If the end of the line is preceded by an odd number of backslash
characters, the following line is also considered part of the
comment and is ignored.

For example, the following code outputs `[1,3,4,7]`

    [
      1,
      # foo \
      2,
      # bar \\
      3,
      4, # baz \\\
      5, \
      6,
      7
      # comment \
        comment \
        comment
    ]

Backslash continuing the comment on the next line can be useful
when writing the "shebang" for a jq script:

    #!/bin/sh --
    # total - Output the sum of the given arguments (or stdin)
    # usage: total [numbers...]
    # \
    exec jq --args -MRnf -- "$0" "$@"

    $ARGS.positional |
    reduce (
      if . == []
        then inputs
        else .[]
      end |
      . as $dot |
      try tonumber catch false |
      if not or isnan then
        @json "total: Invalid number \($dot).\n" | halt_error(1)
      end
    ) as $n (0; . + $n)

The `exec` line is considered a comment by jq, so it is ignored.
But it is not ignored by `sh`, since in `sh` a backslash at the
end of the line does not continue the comment.
With this trick, when the script is invoked as `total 1 2`,
`/bin/sh -- /path/to/total 1 2` will be run, and `sh` will then
run `exec jq --args -MRnf -- /path/to/total 1 2` replacing itself
with a `jq` interpreter invoked with the specified options (`-M`,
`-R`, `-n`, `--args`), that evaluates the current file (`$0`),
with the arguments (`$@`) that were passed to `sh`.
