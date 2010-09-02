from south.signals import post_migrate

from merengue.section.models import Menu, ContentLink, AbsoluteLink


def handle_post_migrate(sender, **kwargs):
    if kwargs['app'] == 'website':
        add_portal_menus()


def add_portal_menus():
    root_menu = Menu.objects.get(slug='portal_menu')
    menu2 = Menu.objects.create(
        name_en='Menu to Django',
        slug='menu-django',
        parent=root_menu,
    )
    link2 = AbsoluteLink.objects.create(
        url='http://www.djangoproject.com/',
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


post_migrate.connect(handle_post_migrate)
