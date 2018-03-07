# youthinfront-site

Master branch is visible [here](https://youthinfront.github.io/youthinfront-site/) (gh pages)

## Updating Previous-Next data

First, to try to keep things consistent, the horizontal sections on the homepage are `Post`s, and the cards within them each point to a `Page`.

Navigation between Pages in one Post is hard due to some limitations of our tech stack. Currently the information about which Page belongs in each Post is captured in the Post's `.md` file. For example, in `2018-02-21-1-why-protest.md`

```---
layout: post
title: Why protest?
subtitle: Will it make a difference?
cards:
    - content: 
        title: Nonviolence and Protest
        subtitle: Dr. King's Principles of Non-Violence
        href: /nonviolence-and-protest.html 
    - content: 
        title: Chicago to Parkland
        subtitle: The long history of youth activism and gun violence
        href: /chicago-to-parkland.html
...
---
```

Each of those `card` listings points to a Page, and this list of `cards` in the `Post` `.md` file is the _only_ place where we capture the information about which Pages belong in a Post. We would need that info to have a Previous and Next button (or swipe or any other means of navigation), but when you're viewing a single Page, you only have access to the information in that Page's `.md` file, not the Post that pointed to it.

To get that information on each Page we'd have to work outside the bounds of the framework a little bit.