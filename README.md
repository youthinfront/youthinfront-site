# youthinfront-site

Master branch is visible [here](https://youthinfront.github.io/youthinfront-site/) (gh pages)

## Updating Previous-Next data

We have a python script to do some cleanup work before deploying. The primary tasks of this script are:

1. Pull card order from the Posts and use that to add `previous` and `next` frontmatter to pages for navigation.
2. Pull the first title from each page and ensure that it ends up in the frontmatter's `title` key.

To do this, you need but run one command:

`python scraper.py`

Then commit any changes and push to master

If you want a little more granularity, you can accomplish the specific tasks above via

`python scraper.py navigation`

`python scraper.py titles`

There's one more fun little maintenance task the script can do: finding top-level `.md` pages that aren't referenced in any posts/cards. You can print these to the console via

`python scraper.py orphans`

#### Scraper Motivation

The information about which Page belongs in each Post is captured in the Post's `.md` file. Each of those `card` listings points to a Page, and this list of `cards` in the `Post` `.md` file is the _only_ place where we capture the information about which Pages belong in a Post. We would need that info to have a Previous and Next button (or swipe or any other means of navigation), but when you're viewing a single Page, you only have access to the information in that Page's `.md` file, not the Post that pointed to it.

To get that information on each Page we'd have to work outside the bounds of the framework a little bit. This is where the python script comes in.