## Math

jq currently only has IEEE754 double-precision (64-bit) floating
point number support.

Besides simple arithmetic operators such as `+`, jq also has most
standard math functions from the C math library.  C math functions
that take a single input argument (e.g., `sin()`) are available as
zero-argument jq functions.  C math functions that take two input
arguments (e.g., `pow()`) are available as two-argument jq
functions that ignore `.`.

Availability of standard math functions depends on the
availability of the corresponding math functions in your operating
system and C math library.  Unavailable math functions will be
defined but will raise an error.
