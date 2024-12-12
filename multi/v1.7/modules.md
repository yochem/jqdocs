## Modules

jq has a library/module system.  Modules are files whose names end
in `.jq`.

Modules imported by a program are searched for in a default search
path (see below).  The `import` and `include` directives allow the
importer to alter this path.

Paths in the search path are subject to various substitutions.

For paths starting with `~/`, the user's home directory is
substituted for `~`.

For paths starting with `$ORIGIN/`, the directory where the jq
executable is located is substituted for `$ORIGIN`.

For paths starting with `./` or paths that are `.`, the path of
the including file is substituted for `.`.  For top-level programs
given on the command-line, the current directory is used.

Import directives can optionally specify a search path to which
the default is appended.

The default search path is the search path given to the `-L`
command-line option, else `["~/.jq", "$ORIGIN/../lib/jq",
"$ORIGIN/../lib"]`.

Null and empty string path elements terminate search path
processing.

A dependency with relative path `foo/bar` would be searched for in
`foo/bar.jq` and `foo/bar/bar.jq` in the given search path. This
is intended to allow modules to be placed in a directory along
with, for example, version control files, README files, and so on,
but also to allow for single-file modules.

Consecutive components with the same name are not allowed to avoid
ambiguities (e.g., `foo/foo`).

For example, with `-L$HOME/.jq` a module `foo` can be found in
`$HOME/.jq/foo.jq` and `$HOME/.jq/foo/foo.jq`.

If `$HOME/.jq` is a file, it is sourced into the main program.

### `import RelativePathString as NAME [<metadata>];`

Imports a module found at the given path relative to a
directory in a search path.  A `.jq` suffix will be added to
the relative path string.  The module's symbols are prefixed
with `NAME::`.

The optional metadata must be a constant jq expression.  It
should be an object with keys like `homepage` and so on.  At
this time jq only uses the `search` key/value of the metadata.
The metadata is also made available to users via the
`modulemeta` builtin.

The `search` key in the metadata, if present, should have a
string or array value (array of strings); this is the search
path to be prefixed to the top-level search path.

### `include RelativePathString [<metadata>];`

Imports a module found at the given path relative to a
directory in a search path as if it were included in place.  A
`.jq` suffix will be added to the relative path string.  The
module's symbols are imported into the caller's namespace as
if the module's content had been included directly.

The optional metadata must be a constant jq expression.  It
should be an object with keys like `homepage` and so on.  At
this time jq only uses the `search` key/value of the metadata.
The metadata is also made available to users via the
`modulemeta` builtin.

### `import RelativePathString as $NAME [<metadata>];`

Imports a JSON file found at the given path relative to a
directory in a search path.  A `.json` suffix will be added to
the relative path string.  The file's data will be available
as `$NAME::NAME`.

The optional metadata must be a constant jq expression.  It
should be an object with keys like `homepage` and so on.  At
this time jq only uses the `search` key/value of the metadata.
The metadata is also made available to users via the
`modulemeta` builtin.

The `search` key in the metadata, if present, should have a
string or array value (array of strings); this is the search
path to be prefixed to the top-level search path.

### `module <metadata>;`

This directive is entirely optional.  It's not required for
proper operation.  It serves only the purpose of providing
metadata that can be read with the `modulemeta` builtin.

The metadata must be a constant jq expression.  It should be
an object with keys like `homepage`.  At this time jq doesn't
use this metadata, but it is made available to users via the
`modulemeta` builtin.

### `modulemeta`

Takes a module name as input and outputs the module's metadata
as an object, with the module's imports (including metadata)
as an array value for the `deps` key and the module's defined
functions as an array value for the `defs` key.

Programs can use this to query a module's metadata, which they
could then use to, for example, search for, download, and
install missing dependencies.
