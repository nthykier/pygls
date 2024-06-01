from pygls.server import LanguageServer
from lsprotocol import types


class MyLanguageServer(LanguageServer):

    @LanguageServer.feature(
        types.TEXT_DOCUMENT_COMPLETION,
        types.CompletionOptions(trigger_characters=["."]),
    )
    def completions(self, params: types.CompletionParams):
        document = server.workspace.get_text_document(params.text_document.uri)
        current_line = document.lines[params.position.line].strip()

        if not current_line.endswith("hello."):
            return []

        return [
            types.CompletionItem(label="world"),
            types.CompletionItem(label="friend"),
        ]


server = LanguageServer("example-server", "v0.1")

server.start_io()
