from app.agent.tools.executar_python import executar_python


def test_hello_world():
    result = executar_python('print("hello")')
    assert result["success"] is True
    assert "hello" in result["output"]


def test_blocks_import_os_literal():
    result = executar_python("import os\nprint(os.getcwd())")
    assert result["success"] is False
