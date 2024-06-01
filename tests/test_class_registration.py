import pytest
from lsprotocol.types import TEXT_DOCUMENT_COMPLETION

from pygls.server import LanguageServer


def test_instance_based_registration() -> None:

    class TestLanguageServer(LanguageServer):
        pass

    ls = TestLanguageServer("test", "v1.0")
    assert TEXT_DOCUMENT_COMPLETION not in ls.lsp.fm.features

    @ls.feature(TEXT_DOCUMENT_COMPLETION)
    def do_nothing(ls, param):
        return None

    assert TEXT_DOCUMENT_COMPLETION in ls.lsp.fm.features


def test_class_based_registration() -> None:

    class TestLanguageServer(LanguageServer):
        @LanguageServer.feature(TEXT_DOCUMENT_COMPLETION)
        def do_nothing(self, param):
            return None

    ls = TestLanguageServer("test", "v1.0")
    assert TEXT_DOCUMENT_COMPLETION in ls.lsp.fm.features


def test_class_based_registration_incorrect() -> None:

    @LanguageServer.feature(TEXT_DOCUMENT_COMPLETION)
    def do_nothing(ls, param):
        pass

    with pytest.raises(TypeError):
        # The __init_subclass__ hook will catch this one.
        class TestLanguageServer(LanguageServer):
            pass


def test_class_based_registration_incorrect() -> None:

    class TestLanguageServer(LanguageServer):
        pass

    @LanguageServer.feature(TEXT_DOCUMENT_COMPLETION)
    def do_nothing(ls, param):
        pass

    ls = TestLanguageServer("test", "v1.0")
    with pytest.raises(TypeError):
        # Ideally we would use ls.start_io or so here, but that would require more setup
        # in case the self-check does not abort as/when it should.
        ls._start_self_check()
