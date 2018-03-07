import os
import sys

class Page:
    def __init__(self, filename, path=os.getcwd()):
        self.filename = filename
        self.path = path

    def process(self, write=True):
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
        self.front_matter_lines = []

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
            if has_hit_opener and (line.strip() != ''):
                print line
                key,value = line.split(':', 1)
                value = value.strip()
                self.front_matter[key] = value
                self.front_matter_keys_in_order.append(key)
                self.front_matter_lines.append(line)

        self.content_lines = []
        for i in xrange(first_content_line, len(self.raw_lines)):
            self.content_lines.append(self.raw_lines[i])

    def add_title_front_matter(self):
        tag = 'title'
        if tag in self.front_matter:
            self.front_matter[tag] = self.front_matter[tag].replace(':','')
            return
        else:
            title = self.extract_first_title()
            self.set_front_matter(tag, title)

    def set_front_matter(self, key, value):
        self.front_matter[key] = value
        value = value.replace(':', '')
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

class Post(Page):
    def __init__(self, filename, path=os.path.join(os.path.join(os.getcwd(), '_posts'), 'blog')):
        self.filename = filename
        self.path = path

    def process(self):
        self.load()
        self.process_lines()
        print self.front_matter_lines
        #self.rewrite()

    def get_linked_content(self):
        pass
        
class Scraper:
    def __init__(self, path=os.getcwd()):
        self.path = path

    def process_pages(self):
        pages = self.get_pages()
        for page in pages:
            print page
            Page(page).process()

    def process_navigation(self):
        posts = self.get_post_files()
        for post in posts:
            print post
            pages = self.get_pages_in_post_cards(post)
            print pages
            for i in xrange(0, len(pages)):
                page_file = pages[i] + '.md'
                page = Page(page_file)
                page.process(False)
                page.set_front_matter('previous', '/' + pages[i-1] + '.html')
                page.set_front_matter('next', '/' + pages[(i+1) % len(pages)] + '.html')
                page.rewrite()

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
    command = None
    if len(sys.argv) >= 2:
        command = sys.argv[1]

    if command == 'titles':
        Scraper().process_pages()
    elif command == 'navigation':
        Scraper().process_navigation()
    elif command == 'orphans':
        Scraper().print_orphaned_pages()
    else:
        Scraper().process_pages()
        Scraper().process_navigation()