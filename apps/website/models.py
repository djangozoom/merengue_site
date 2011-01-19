from south.signals import post_migrate

from django.db import transaction

from merengue.base.models import BaseContent
from merengue.section.models import Menu, ContentLink, AbsoluteLink
from website import lipsum

lipsum_generator = lipsum.Generator()
lipsum_html_generator = lipsum.MarkupGenerator()


def handle_post_migrate(sender, **kwargs):
    if kwargs['app'] == 'website':
        transaction.commit()
        add_portal_menus()
        add_news_items()


def add_portal_menus():
    root_menu = Menu.objects.get(slug='portal_menu')
    menu2, created = Menu.objects.get_or_create(
        name_en='Menu to News',
        slug='menu-news',
    )
    if created:
        menu2.parent = root_menu
        menu2.lft = 1
        menu2.save()
    link2, created = AbsoluteLink.objects.get_or_create(
        url='/news/',
        menu = menu2,
    )
    menu1, created = Menu.objects.get_or_create(
        name_en='Menu to test section',
        slug='menu-test-section',
    )
    if created:
        menu1.parent = root_menu
        menu1.lft = 0
        menu1.save()
    link1, created = AbsoluteLink.objects.get_or_create(
        url='/test-section/',
        menu=menu1,
    )
    link1.save()
    menu1_2, created = Menu.objects.get_or_create(
        slug='menu-homepage',
    )
    if created:
        menu1_2.name_en = 'Homepage'
        menu1_2.parent = menu1
        menu1_2.save()
    welcome_doc = BaseContent.objects.get(id=32)
    other_doc = BaseContent.objects.get(id=33)
    link1_2, created = ContentLink.objects.get_or_create(
        menu=menu1_2,
        content=welcome_doc,
    )
    menu1_3, created = Menu.objects.get_or_create(
        name_en='Menu to doc1',
        slug='menu-doc1',
        parent=menu1,
    )
    link1_3, created = ContentLink.objects.get_or_create(
        menu=menu1_3,
        content=other_doc,
    )
    root_menu.rght = 19
    root_menu.save()


def add_news_items():
    from plugins.news.models import NewsItem
    for i in range(100):
        news_item, created = NewsItem.objects.get_or_create(
            slug='news-item-%d' % i,
        )
        news_item.name_en = 'News item %d' % i
        news_item.name_es = 'Noticia %d' % i
        news_item.status = 'published'
        news_item.description_en = lipsum_generator.generate_paragraph()
        news_item.body_en = lipsum_html_generator.generate_paragraphs_html_li(5)
        news_item.save()


post_migrate.connect(handle_post_migrate)
