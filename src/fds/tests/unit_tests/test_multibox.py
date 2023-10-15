from fds.contracts.Multibox import MultiBox


def test_multibox_deploy(owner):
    mb = MultiBox(owner)

    assert mb


def test_get_root(owner, multibox):
    mb = MultiBox(owner, multibox.address)

    assert mb.getRoots()[-1] != "0x000000000000000000000000000000000000000"
