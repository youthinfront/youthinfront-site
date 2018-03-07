import os

"""
---
layout: page
title: Martin Luther King Jr.'s Six Principles of Nonviolence
---

Martin Luther King Jr.'s Six Principles of Nonviolence
=================

Nonviolent protest has been an essential part of social and political change in American history. Martin Luther King Jr. laid out six principles of nonviolence in his book [*Stride Toward Freedom*](https://www.amazon.com/Stride-Toward-Freedom-Montgomery-Story/dp/0062504908). 

* **PRINCIPLE ONE:** Nonviolence is a way of life for courageous people.
* **PRINCIPLE TWO:** Nonviolence seeks to win friendship and understanding.
* **PRINCIPLE THREE:** Nonviolence seeks to defeat injustice not people.
* **PRINCIPLE FOUR:** Nonviolence holds that suffering can educate and transform.
* **PRINCIPLE FIVE:** Nonviolence chooses love instead of hate.
* **PRINCIPLE SIX:** Nonviolence believes that the universe is on the side of justice.

For more on Martin Luther King's philosophy of nonviolence, visit [The King Center](http://www.thekingcenter.org/king-philosophy).
"""

class Page:
    def __init__(self, filename, path=os.getcwd()):
        self.filename = filename
        self.path = path

    def process(self):
        self.load()
        self.process_lines()
        self.add_title_front_matter()
        print self.front_matter
        self.rewrite()

    def load(self):
        self.raw_lines = []
        handle = open(os.path.join(self.path, self.filename), 'r')
        for line in handle.readlines():
            self.raw_lines.append(line)

    def process_lines(self):
        self.front_matter = {}
        self.front_matter_keys_in_order = []

        first_content_line = 0
        has_hit_opener = False
        has_hit_closer = False
        for i in xrange(0, len(self.raw_lines)):
            line = self.raw_lines[i]
            if has_hit_closer:
                first_content_line = i
                break
            if line.find('---') != -1:
                if not has_hit_opener:
                    has_hit_opener = True
                    continue
                else:
                    has_hit_closer = True
                    continue
            key,value = line.split(':', 1)
            value = value.strip()
            self.front_matter[key] = value
            self.front_matter_keys_in_order.append(key)

        self.content_lines = []
        for i in xrange(first_content_line, len(self.raw_lines)):
            self.content_lines.append(self.raw_lines[i])

    def add_title_front_matter(self):
        tag = 'title'
        if tag in self.front_matter:
            return
        else:
            title = self.extract_first_title()
            self.set_front_matter(tag, title)

    def set_front_matter(self, key, value):
        self.front_matter[key] = value
        if key not in self.front_matter_keys_in_order:
            self.front_matter_keys_in_order.append(key)

    def extract_first_title(self):
        title = ''
        for i in xrange(0, len(self.content_lines)):
            line = self.content_lines[i]
            if line.find('# ') == 0:
                title = line[line.find('# ') + len('# '):]
                break
            if line.find('===') == 0:
                title = self.content_lines[i - 1]
                break
        if title == '':
            print "NO TITLE"
        title = title.strip()
        return title

    def rewrite(self):                
        handle = open(os.path.join(self.path, self.filename), 'w')
        handle.write('---\n')
        for key in self.front_matter_keys_in_order:
            handle.write(key + ': ' + self.front_matter[key] + '\n')
        handle.write('---\n')
        for line in self.content_lines:
            handle.write(line)
        handle.close()

class Post:
    def __init__(self, filename, path=os.getcwd()):
        self.filename = filename
        self.path = path

    def parse(self):
        pass

class Scraper:
    def __init__(self, path=os.getcwd()):
        self.path = path

    def process_pages(self):
        pages = self.get_pages()
        for page in pages:
            print page
            Page(page).process()

    def print_orphaned_pages(self):
        print self.get_orphaned_pages()

    def get_files(self, path=None):
        if (path == None):
            path = self.path
        return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    def get_pages(self):
        files = self.get_files()
        filtered = [x for x in files if x.endswith('.md')]
        return [x for x in filtered if self.is_real_page(x)]

    def get_page_names(self):
        pages = self.get_pages()
        return [x.replace('.md', '') for x in pages]

    def is_real_page(self, page_file_name):
        handle = open(os.path.join(self.path, page_file_name), 'r')
        for line in handle.readlines():
            locale = line.find('layout: page')
            if locale != -1:
                return True
        return False

    def get_post_files(self):
        return self.get_files(self.get_post_path())

    def get_post_path(self):
        post_path = os.path.join(self.path, '_posts')
        post_path = os.path.join(post_path, 'blog')
        return post_path

    def get_pages_in_post_cards(self, post_file):
        SIGNIFIER = 'href: /'
        post_file_path = os.path.join(self.get_post_path(), post_file)
        post_handle = open(post_file_path, "r")
        referenced_pages = []
        for line in post_handle.readlines():
            locale = line.find(SIGNIFIER)
            if locale != -1:
                html_file_name = line[(locale+len(SIGNIFIER)):]
                page_name = html_file_name.replace('.html', '')
                page_name = page_name.replace('\n', '')
                page_name = page_name.replace('\r', '')
                page_name = page_name.strip()
                referenced_pages.append(page_name)
        return referenced_pages

    def get_all_pages_in_post_cards(self):
        posts = self.get_post_files()
        all_pages = []
        for post in posts:
            pages_in_post = self.get_pages_in_post_cards(post)
            all_pages = all_pages + pages_in_post
        return all_pages

    def get_orphaned_pages(self):
        referenced_pages = self.get_all_pages_in_post_cards()
        pages = self.get_page_names()

        orphaned = []
        parented = []

        for page in pages:
            if page in referenced_pages:
                parented.append(page)
            else:
                orphaned.append(page)
        
        return orphaned

if __name__ == '__main__':
    #Scraper().run()
    #Page('pdf-template.md').load()
    #'teachers-after-march-student-feedback.md'
    Scraper().process_pages()


