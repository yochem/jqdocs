> [!IMPORTANT]
> These docs are extracted from https://github.com/jqlang/jq. I do not own any
> of the content in this repository. For the license of the documentation, see
> the jq repository.

See the preview at https://yochem.nl/jqdocs/.

To build it yourself:

1. [Install Hugo](https://gohugo.io/installation/)
2. `git clone https://github.com/yochem/jqdocs && cd jqdocs`
3. `hugo serve`

This is the structure of this repo. Every item is linked to Hugo documentation
where you can read more about it.

- [`content/`](https://gohugo.io/content-management/organization/): All
  markdown content for the website. Extracted and adapted from the jq repo.
- [`layouts/_default/baseof.html`](https://gohugo.io/templates/base/): Base
  template for all pages
- [`layouts/_default/single.html`](https://gohugo.io/templates/single/):
  Template for all single pages (non-index pages)
- [`layouts/_default/home.html`](https://gohugo.io/templates/home/): Template
  for the root index.html
- [`layouts/manual/single.html`](https://gohugo.io/templates/lookup-order/#target-a-template):
  Template for all manual pages
- [`layouts/manual/list.html`](https://gohugo.io/templates/section/): Uses Hugo
  to fill the content of page `manual/` with that of page `manual/v1.7/`
  (version number can be configured in `hugo.yml`
- [`layouts/partials/`](https://gohugo.io/templates/partial/): Like
  `templates/shared/` in the jq repo
- [`layouts/shortcodes/`](https://gohugo.io/templates/shortcode/): Markdown
  extensions. For now only has one to render code examples
- [`static/`](https://gohugo.io/getting-started/directory-structure/#static):
  No explanation needed.
- [`assets/`](https://gohugo.io/getting-started/directory-structure/#assets):
  CSS, JS, images.
- [`hugo.yml`](https://gohugo.io/getting-started/configuration/): Configuration
  file for Hugo. This defines things like the base url, the menu items in the
  navigation bar, and the current jq version. This now only affects the default
  manual to show, but can also be used in the download links and more. I plan
  to add more config here, so the template files do not have to be touched to
  update website content. Ideally, the only files in the content folder and
  this config need to be changed to update content on the website.
