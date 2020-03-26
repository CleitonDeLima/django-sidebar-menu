import pytest
from django.core.exceptions import ImproperlyConfigured

from sidebar_menu import Menu


def test_menu_root(dj_asserts):
    tree = Menu(
        Menu.ROOT, class_name="sidebar-menu", attrs={"data-widget": "tree"}
    )
    expected = '<ul class="sidebar-menu" data-widget="tree"></ul>'
    dj_asserts.html_equal(tree.render(), expected)


def test_menu_attrs(dj_asserts):
    tree = Menu(Menu.ROOT, attrs={"data-attr1": "1", "data-attr2": "2"})
    expected = '<ul data-attr1="1" data-attr2="2"></ul>'
    dj_asserts.html_equal(tree.render(), expected)


def test_invalid_type_menu():

    with pytest.raises(ImproperlyConfigured):
        Menu("invalid_type").render()


def test_plain_menu(dj_asserts):
    menu = Menu(Menu.PLAIN, text="MENU TEXT")
    dj_asserts.html_equal(menu.render(), "<li>MENU TEXT</li>")


def test_plain_menu_with_class(dj_asserts):
    menu = Menu(Menu.PLAIN, text="MENU TEXT", class_name="item")
    dj_asserts.html_equal(menu.render(), '<li class="item">MENU TEXT</li>')


def test_root_with_menus(dj_asserts):
    menu = Menu(
        Menu.ROOT,
        menus=[
            Menu(Menu.LINK, "test1"),
            Menu(Menu.LINK, "test2"),
            Menu(Menu.LINK, "test3", url="/test3/"),
        ],
    )
    expected = (
        "<ul>"
        '<li><a href="#">test1</a></li>'
        '<li><a href="#">test2</a></li>'
        '<li><a href="/test3/">test3</a></li>'
        "</ul>"
    )
    dj_asserts.html_equal(menu.render(), expected)


def test_link_menu(dj_asserts):
    menu = Menu(Menu.LINK, "home", "/")
    expected = '<li><a href="/">home</a></li>'
    dj_asserts.html_equal(menu.render(), expected)


def test_tree_menu(dj_asserts):
    menu = Menu(Menu.TREE, "Tree root")
    expected = '<li><p>Tree root</p><ul class="tree-menu"></ul></li>'
    dj_asserts.html_equal(menu.render(), expected)


def test_tree_menu_with_menus(dj_asserts):
    menu = Menu(
        Menu.TREE,
        "Tree root",
        menus=[
            Menu(Menu.PLAIN, "menu 1"),
            Menu(Menu.LINK, "menu 2", "/menu2/"),
            Menu(Menu.LINK, "menu 3", "/menu3/"),
        ],
    )
    expected = (
        '<li><p>Tree root</p><ul class="tree-menu">'
        "<li>menu 1</li>"
        '<li><a href="/menu2/">menu 2</a></li>'
        '<li><a href="/menu3/">menu 3</a></li>'
        "</ul></li>"
    )
    dj_asserts.html_equal(menu.render(), expected)


def test_complete_menu(dj_asserts):
    menu = Menu(
        Menu.ROOT,
        menus=[
            Menu(Menu.PLAIN, "menu 1"),
            Menu(Menu.LINK, "menu 2", "/menu2/"),
            Menu(
                Menu.TREE,
                "menu 3",
                menus=[
                    Menu(Menu.PLAIN, "menu 3.1"),
                    Menu(Menu.LINK, "menu 3.2", "/menu3.2/"),
                    Menu(
                        Menu.TREE,
                        "menu 3.3",
                        menus=[
                            Menu(Menu.PLAIN, "menu 3.3.1"),
                            Menu(Menu.PLAIN, "menu 3.3.2"),
                        ],
                    ),
                ],
            ),
        ],
    )
    expected = (
        "<ul>"
        "<li>menu 1</li>"
        '<li><a href="/menu2/">menu 2</a></li>'
        '<li><p>menu 3</p><ul class="tree-menu">'
        "<li>menu 3.1</li>"
        '<li><a href="/menu3.2/">menu 3.2</a></li>'
        '<li><p>menu 3.3</p><ul class="tree-menu">'
        "<li>menu 3.3.1</li>"
        "<li>menu 3.3.2</li>"
        "</ul></li>"
        "</ul></li>"
        "</ul>"
    )
    dj_asserts.html_equal(menu.render(), expected)
