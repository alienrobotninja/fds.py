from ape import convert

from fds.contracts.KeyValueTree import KeyValueTree


def test_load_key_value_tree(owner, key_value_tree):
    kvt = KeyValueTree(owner, key_value_tree.address)

    assert kvt


def test_get_shared_id(kvt):
    assert (
        kvt.getSharedId().hex()
        == "0x23e642b7242469a5e3184a6566020c815689149967703a98c0affc14b9ca9b28"
    )


def test_get_root_id(kvt):
    assert (
        kvt.getRootId().hex()
        == "0xc7f5bbf5fe95923f0691c94f666ac3dfed12456cd33bd018e7620c3d93edd5a6"
    )


def test_set_n_get_key_value(kvt):
    node = 1
    key = 1
    value = 420

    kvt.setKeyValue(node, key, value)

    assert convert(kvt.getKeyValue(node, key).hex(), int) == value


def test_add_child_node(kvt):
    parent_node_id = "0xc7f5bbf5fe95923f0691c94f666ac3dfed12456cd33bd018e7620c3d93edd5a6"
    sub_node_id = "0x23e642b7242469a5e3184a6566020c815689149967703a98c0affc14b9ca9b28"
    kvt.addChildNode(parent_node_id, sub_node_id)

    assert kvt.getChildren(parent_node_id)[-1].hex() == sub_node_id
