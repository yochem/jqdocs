---
headline: jq 1.3 Manual
manpage_epilogue: |
  ## BUGS

  Presumably. Report them or discuss them at:

      https://github.com/jqlang/jq/issues

  ## AUTHOR

  Stephen Dolan `<mu@netsoc.tcd.ie>`
manpage_intro: |
  jq(1) -- Command-line JSON processor
  ====================================

  ## SYNOPSIS

  `jq` [<options>...] <filter> [<files>...]

  `jq` can transform JSON in various ways, by selecting, iterating,
  reducing and otherwise mangling JSON documents. For instance,
  running the command `jq 'map(.price) | add'` will take an array of
  JSON objects as input and return the sum of their "price" fields.

  By default, `jq` reads a stream of JSON objects (whitespace
  separated) from `stdin`. One or more <files> may be specified, in
  which case `jq` will read input from those instead.

  The <options> are described in the [INVOKING JQ] section, they
  mostly concern input and output formatting. The <filter> is written
  in the jq language and specifies how to transform the input
  document.

  ## FILTERS

---

A jq program is a "filter": it takes an input, and produces an
output. There are a lot of builtin filters for extracting a
particular field of an object, or converting a number to a string,
or various other standard tasks.

Filters can be combined in various ways - you can pipe the output of
one filter into another filter, or collect the output of a filter
into an array.

Some filters produce multiple results, for instance there's one that
produces all the elements of its input array. Piping that filter
into a second runs the second filter for each element of the
array. Generally, things that would be done with loops and iteration
in other languages are just done by gluing filters together in jq.

It's important to remember that every filter has an input and an
output. Even literals like "hello" or 42 are filters - they take an
input but always produce the same literal as output. Operations that
combine two filters, like addition, generally feed the same input to
both and combine the results. So, you can implement an averaging
filter as `add / length` - feeding the input array both to the `add`
filter and the `length` filter and dividing the results.

But that's getting ahead of ourselves. :) Let's start with something
simpler:
