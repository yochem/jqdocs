---
title: Tutorial
---

GitHub has a JSON API, so let's play with that. This URL gets us the last
5 commits from the jq repo.

{{< show-result-accordion `curl 'https://api.github.com/repos/jqlang/jq/commits?per_page=5'`>}}
{{< include "result-1.json" >}}
{{< /show-result-accordion >}}


GitHub returns nicely formatted JSON. For servers that don't, it can be
helpful to pipe the response through jq to pretty-print it. The simplest
jq program is the expression `.`, which takes the input and produces it
unchanged as output.

{{< show-result-accordion `curl 'https://api.github.com/repos/jqlang/jq/commits?per_page=5' | jq '.'`>}}
[
  {
    "sha": "cff5336ec71b6fee396a95bb0e4bea365e0cd1e8",
    "node_id": "C_kwDOAE3WVdoAKGNmZjUzMzZlYzcxYjZmZWUzOTZhOTViYjBlNGJlYTM2NWUwY2QxZTg",
    "commit": {
      "author": {
        "name": "Mattias Wadman",
        "email": "mattias.wadman@gmail.com",
        "date": "2021-06-09T14:02:22Z"
      },
      "committer": {
        "name": "Nico Williams",
        "email": "nico@cryptonector.com",
        "date": "2022-05-26T21:04:32Z"
      },
      "message": "docs: Document repeat(exp)",
      "tree": {
        "sha": "d67d5542df1f16d1a48e1fb75749f60482cd874b",
        "url": "https://api.github.com/repos/jqlang/jq/git/trees/d67d5542df1f16d1a48e1fb75749f60482cd874b"
      },
      "url": "https://api.github.com/repos/jqlang/jq/git/commits/cff5336ec71b6fee396a95bb0e4bea365e0cd1e8",
      "comment_count": 0,
      "verification": {
        "verified": false,
        "reason": "unsigned",
        "signature": null,
        "payload": null
      }
    },
    "url": "https://api.github.com/repos/jqlang/jq/commits/cff5336ec71b6fee396a95bb0e4bea365e0cd1e8",
    "html_url": "https://github.com/jqlang/jq/commit/cff5336ec71b6fee396a95bb0e4bea365e0cd1e8",
    "comments_url": "https://api.github.com/repos/jqlang/jq/commits/cff5336ec71b6fee396a95bb0e4bea365e0cd1e8/comments",
    "author": {
...

{{< /show-result-accordion >}}

We can use jq to extract just the first commit.

```
curl 'https://api.github.com/repos/jqlang/jq/commits?per_page=5' | jq '.[0]'
```
```json
{
  "sha": "cff5336ec71b6fee396a95bb0e4bea365e0cd1e8",
  "node_id": "C_kwDOAE3WVdoAKGNmZjUzMzZlYzcxYjZmZWUzOTZhOTViYjBlNGJlYTM2NWUwY2QxZTg",
  "commit": {
    "author": {
      "name": "Mattias Wadman",
      "email": "mattias.wadman@gmail.com",
      "date": "2021-06-09T14:02:22Z"
    },
    "committer": {
      "name": "Nico Williams",
      "email": "nico@cryptonector.com",
      "date": "2022-05-26T21:04:32Z"
    },
    "message": "docs: Document repeat(exp)",
    "tree": {
      "sha": "d67d5542df1f16d1a48e1fb75749f60482cd874b",
      "url": "https://api.github.com/repos/jqlang/jq/git/trees/d67d5542df1f16d1a48e1fb75749f60482cd874b"
    },
    "url": "https://api.github.com/repos/jqlang/jq/git/commits/cff5336ec71b6fee396a95bb0e4bea365e0cd1e8",
    "comment_count": 0,
    "verification": {
      "verified": false,
      "reason": "unsigned",
      "signature": null,
      "payload": null
    }
  },
  "url": "https://api.github.com/repos/jqlang/jq/commits/cff5336ec71b6fee396a95bb0e4bea365e0cd1e8",
  "html_url": "https://github.com/jqlang/jq/commit/cff5336ec71b6fee396a95bb0e4bea365e0cd1e8",
  "comments_url": "https://api.github.com/repos/jqlang/jq/commits/cff5336ec71b6fee396a95bb0e4bea365e0cd1e8/comments",
  "author": {
    "login": "wader",
    "id": 185566,
    "node_id": "MDQ6VXNlcjE4NTU2Ng==",
    "avatar_url": "https://avatars.githubusercontent.com/u/185566?v=4",
    "gravatar_id": "",
    "url": "https://api.github.com/users/wader",
    "html_url": "https://github.com/wader",
    "followers_url": "https://api.github.com/users/wader/followers",
    "following_url": "https://api.github.com/users/wader/following{/other_user}",
    "gists_url": "https://api.github.com/users/wader/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/wader/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/wader/subscriptions",
    "organizations_url": "https://api.github.com/users/wader/orgs",
    "repos_url": "https://api.github.com/users/wader/repos",
    "events_url": "https://api.github.com/users/wader/events{/privacy}",
    "received_events_url": "https://api.github.com/users/wader/received_events",
    "type": "User",
    "site_admin": false
  },
  "committer": {
    "login": "nicowilliams",
    "id": 604851,
    "node_id": "MDQ6VXNlcjYwNDg1MQ==",
    "avatar_url": "https://avatars.githubusercontent.com/u/604851?v=4",
    "gravatar_id": "",
    "url": "https://api.github.com/users/nicowilliams",
    "html_url": "https://github.com/nicowilliams",
    "followers_url": "https://api.github.com/users/nicowilliams/followers",
    "following_url": "https://api.github.com/users/nicowilliams/following{/other_user}",
    "gists_url": "https://api.github.com/users/nicowilliams/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/nicowilliams/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/nicowilliams/subscriptions",
    "organizations_url": "https://api.github.com/users/nicowilliams/orgs",
    "repos_url": "https://api.github.com/users/nicowilliams/repos",
    "events_url": "https://api.github.com/users/nicowilliams/events{/privacy}",
    "received_events_url": "https://api.github.com/users/nicowilliams/received_events",
    "type": "User",
    "site_admin": false
  },
  "parents": [
    {
      "sha": "f2ad9517c72f6267ae317639ab56bbfd4a8653d4",
      "url": "https://api.github.com/repos/jqlang/jq/commits/f2ad9517c72f6267ae317639ab56bbfd4a8653d4",
      "html_url": "https://github.com/jqlang/jq/commit/f2ad9517c72f6267ae317639ab56bbfd4a8653d4"
    }
  ]
}

```

For the rest of the examples, I'll leave out the `curl` command - it's not
going to change.

There's a lot of info we don't care about there, so we'll restrict it down
to the most interesting fields.

```jq
jq '.[0] | {message: .commit.message, name: .commit.committer.name}'
```
```json
{
  "message": "docs: Document repeat(exp)",
  "name": "Nico Williams"
}

```

The `|` operator in jq feeds the output of one filter (`.[0]` which gets
the first element of the array in the response) into the input of another
(`{...}` which builds an object out of those fields). You can access
nested attributes, such as `.commit.message`.

Now let's get the rest of the commits.

```jq
jq '.[] | {message: .commit.message, name: .commit.committer.name}'
```
```json
{
  "message": "docs: Document repeat(exp)",
  "name": "Nico Williams"
}
{
  "message": "Mention -n in IO-section and for input/inputs",
  "name": "Nico Williams"
}
{
  "message": "Fix iteration problem for non decimal string\n\nWhen the string transformation to number failed, all following\ntransformation failed too.\n\nThis happend because status in decNumberFromString function is\nupdated just in error case. Reusing the DEC_CONTEXT that failed\nbefore results into error even if the string is valid number.",
  "name": "Nico Williams"
}
{
  "message": "docs: point to Libera.Chat instead of Freenode",
  "name": "Nico Williams"
}
{
  "message": "Missing \"va_end\" call. This was found by running the cppcheck static analysis where it shows as error.",
  "name": "Nico Williams"
}

```

`.[]` returns each element of the array returned in the response, one at a
time, which are all fed into
`{message: .commit.message, name: .commit.committer.name}`.

Data in jq is represented as streams of JSON values - every jq
expression runs for each value in its input stream, and can
produce any number of values to its output stream.

Streams are serialised by just separating JSON values with
whitespace. This is a `cat`-friendly format - you can just join
two JSON streams together and get a valid JSON stream.

If you want to get the output as a single array, you can tell jq to
"collect" all of the answers by wrapping the filter in square
brackets:

```jq
jq '[.[] | {message: .commit.message, name: .commit.committer.name}]'
```
```json
[
  {
    "message": "docs: Document repeat(exp)",
    "name": "Nico Williams"
  },
  {
    "message": "Mention -n in IO-section and for input/inputs",
    "name": "Nico Williams"
  },
  {
    "message": "Fix iteration problem for non decimal string\n\nWhen the string transformation to number failed, all following\ntransformation failed too.\n\nThis happend because status in decNumberFromString function is\nupdated just in error case. Reusing the DEC_CONTEXT that failed\nbefore results into error even if the string is valid number.",
    "name": "Nico Williams"
  },
  {
    "message": "docs: point to Libera.Chat instead of Freenode",
    "name": "Nico Williams"
  },
  {
    "message": "Missing \"va_end\" call. This was found by running the cppcheck static analysis where it shows as error.",
    "name": "Nico Williams"
  }
]

```

- - -

Next, let's try getting the URLs of the parent commits out of the
API results as well. In each commit, the GitHub API includes information
about "parent" commits. There can be one or many.

    "parents": [
      {
        "sha": "f2ad9517c72f6267ae317639ab56bbfd4a8653d4",
        "url": "https://api.github.com/repos/jqlang/jq/commits/f2ad9517c72f6267ae317639ab56bbfd4a8653d4",
        "html_url": "https://github.com/jqlang/jq/commit/f2ad9517c72f6267ae317639ab56bbfd4a8653d4"
      }
    ]

We want to pull out all of the "html_url" fields inside that array of parent
commits and make a simple list of strings to go along with the
"message" and "author" fields we already have.

```jq
jq '[.[] | {message: .commit.message, name: .commit.committer.name, parents: [.parents[].html_url]}]'
```
```json
[
  {
    "message": "docs: Document repeat(exp)",
    "name": "Nico Williams",
    "parents": [
      "https://github.com/jqlang/jq/commit/f2ad9517c72f6267ae317639ab56bbfd4a8653d4"
    ]
  },
  {
    "message": "Mention -n in IO-section and for input/inputs",
    "name": "Nico Williams",
    "parents": [
      "https://github.com/jqlang/jq/commit/c4d39c4d22f2b12225ca1b311708f7e084ad9ff8"
    ]
  },
  {
    "message": "Fix iteration problem for non decimal string\n\nWhen the string transformation to number failed, all following\ntransformation failed too.\n\nThis happend because status in decNumberFromString function is\nupdated just in error case. Reusing the DEC_CONTEXT that failed\nbefore results into error even if the string is valid number.",
    "name": "Nico Williams",
    "parents": [
      "https://github.com/jqlang/jq/commit/174db0f93552bdb551ae1f3c5c64744df0ad8e2f"
    ]
  },
  {
    "message": "docs: point to Libera.Chat instead of Freenode",
    "name": "Nico Williams",
    "parents": [
      "https://github.com/jqlang/jq/commit/29cf77977ef52eec708982b19bf9d2ec17443337"
    ]
  },
  {
    "message": "Missing \"va_end\" call. This was found by running the cppcheck static analysis where it shows as error.",
    "name": "Nico Williams",
    "parents": [
      "https://github.com/jqlang/jq/commit/55e6e2c21829bd866bd4b18ee254b05c9020320a"
    ]
  }
]

```

Here we're making an object as before, but this time the `parents`
field is being set to `[.parents[].html_url]`, which collects
all of the parent commit URLs defined in the parents object.


- - -

Here endeth the tutorial! There's lots more to play with. Go
read [the manual](../manual/) if you're interested, and [download
jq](../download/) if you haven't already.

