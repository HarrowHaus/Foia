from pril.ids import document_id, new_id


def test_document_id_is_deterministic():
    digest = "a" * 64
    assert document_id(digest) == document_id(digest)
    assert document_id(digest).startswith("doc_")


def test_new_id_prefix():
    assert new_id("clm").startswith("clm_")
