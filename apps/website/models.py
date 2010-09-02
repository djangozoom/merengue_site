from south.signals import post_migrate

from merengue.section.models import Menu, ContentLink, AbsoluteLink
from website import lipsum

lipsum_generator = lipsum.Generator()
lipsum_html_generator = lipsum.MarkupGenerator()


def handle_post_migrate(sender, **kwargs):
    if kwargs['app'] == 'website':
        add_portal_menus()
        add_news_items()


def add_portal_menus():
    root_menu = Menu.objects.get(slug='portal_menu')
    menu2 = Menu.objects.create(
        name_en='Menu to News',
        slug='menu-news',
        parent=root_menu,
    )
    link2 = AbsoluteLink.objects.create(
        url='/news/',
        menu=menu2,
    )
    menu1 = Menu.objects.create(
        name_en='Menu to test section',
        slug='menu-test-section',
        parent=root_menu,
        lft=0,
    )
    link1 = AbsoluteLink.objects.create(
        url='/test-section/',
        menu=menu1,
    )
    menu1_2 = Menu.objects.create(
        name_en='Homepage',
        slug='menu-homepage',
        parent=menu1,
    )
    link1_2 = ContentLink.objects.create(
        content_id=1,
        menu=menu1_2,
    )
    menu1_3 = Menu.objects.create(
        name_en='Menu to doc1',
        slug='menu-doc1',
        parent=menu1,
    )
    link1_3 = ContentLink.objects.create(
        content_id=4,
        menu=menu1_3,
    )


def add_news_items():
    from plugins.news.models import NewsItem
    for i in range(100):
        news_item = NewsItem.objects.create(
            slug='news-item-%d' % i,
            name_en='News item %d' % i,
            name_es='Noticia %d' % i,
            status='published',
            description_en=lipsum_generator.generate_paragraph(),
            body_en=lipsum_html_generator.generate_paragraphs_html_li(5),
        )


post_migrate.connect(handle_post_migrate)
