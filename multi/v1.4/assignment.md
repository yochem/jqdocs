## Assignment

Assignment works a little differently in jq than in most
programming languages. jq doesn't distinguish between references
to and copies of something - two objects or arrays are either
equal or not equal, without any further notion of being "the
same object" or "not the same object".

If an object has two fields which are arrays, `.foo` and `.bar`,
and you append something to `.foo`, then `.bar` will not get
bigger. Even if you've just set `.bar = .foo`. If you're used to
programming in languages like Python, Java, Ruby, JavaScript,
etc. then you can think of it as though jq does a full deep copy
of every object before it does the assignment (for performance,
it doesn't actually do that, but that's the general idea).

### `=`

The filter `.foo = 1` will take as input an object
and produce as output an object with the "foo" field set to
1. There is no notion of "modifying" or "changing" something
in jq - all jq values are immutable. For instance,

 .foo = .bar | .foo.baz = 1

will not have the side-effect of setting .bar.baz to be set
to 1, as the similar-looking program in JavaScript, Python,
Ruby or other languages would. Unlike these languages (but
like Haskell and some other functional languages), there is
no notion of two arrays or objects being "the same array" or
"the same object". They can be equal, or not equal, but if
we change one of them in no circumstances will the other
change behind our backs.

This means that it's impossible to build circular values in
jq (such as an array whose first element is itself). This is
quite intentional, and ensures that anything a jq program
can produce can be represented in JSON.

### `|=`
As well as the assignment operator '=', jq provides the "update"
operator '|=', which takes a filter on the right-hand side and
works out the new value for the property being assigned to by running
the old value through this expression. For instance, .foo |= .+1 will
build an object with the "foo" field set to the input's "foo" plus 1.

This example should show the difference between '=' and '|=':

Provide input '{"a": {"b": 10}, "b": 20}' to the programs:

.a = .b
.a |= .b

The former will set the "a" field of the input to the "b" field of the
input, and produce the output {"a": 20}. The latter will set the "a"
field of the input to the "a" field's "b" field, producing {"a": 10}.

### `+=`, `-=`, `*=`, `/=`, `%=`, `//=`

jq has a few operators of the form `a op= b`, which are all
equivalent to `a |= . op b`. So, `+= 1` can be used to increment values.

program:
```jq
.foo += 1
```
input:
```json
{"foo": 42}
```
output:
```json
{"foo": 43}
```
### Complex assignments
Lots more things are allowed on the left-hand side of a jq assignment
than in most languages. We've already seen simple field accesses on
the left hand side, and it's no surprise that array accesses work just
as well:

    .posts[0].title = "JQ Manual"

What may come as a surprise is that the expression on the left may
produce multiple results, referring to different points in the input
document:

    .posts[].comments |= . + ["this is great"]

That example appends the string "this is great" to the "comments"
array of each post in the input (where the input is an object with a
field "posts" which is an array of posts).

When jq encounters an assignment like 'a = b', it records the "path"
taken to select a part of the input document while executing a. This
path is then used to find which part of the input to change while
executing the assignment. Any filter may be used on the
left-hand side of an equals - whichever paths it selects from the
input will be where the assignment is performed.

This is a very powerful operation. Suppose we wanted to add a comment
to blog posts, using the same "blog" input above. This time, we only
want to comment on the posts written by "stedolan". We can find those
posts using the "select" function described earlier:

    .posts[] | select(.author == "stedolan")

The paths provided by this operation point to each of the posts that
"stedolan" wrote, and we can comment on each of them in the same way
that we did before:

    (.posts[] | select(.author == "stedolan") | .comments) |=
        . + ["terrible."]
