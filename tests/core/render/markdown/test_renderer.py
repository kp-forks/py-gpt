#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2025.07.14 00:00:00                  #
# ================================================== #

from unittest.mock import MagicMock
import platform

from tests.mocks import mock_window
from pygpt_net.core.render.markdown.renderer import Renderer as Render
from pygpt_net.core.render.markdown.body import Body
from pygpt_net.core.render.markdown.helpers import Helpers
from pygpt_net.item.ctx import CtxItem, CtxMeta
from pygpt_net.core.filesystem import Filesystem


def test_clear_input(mock_window):
    """Test clear input"""
    render = Render(mock_window)
    render.get_input_node = MagicMock()
    render.clear_input()
    render.get_input_node().clear.assert_called_once()


def test_reload(mock_window):
    """Test reload render"""
    render = Render(mock_window)
    mock_window.controller.ctx.refresh_output = MagicMock()
    render.reload()
    mock_window.controller.ctx.refresh_output.assert_called_once()


def test_append_context(mock_window):
    """Test append context items"""
    render = Render(mock_window)
    render.append_context_item = MagicMock()
    item1 = CtxItem()
    item2 = CtxItem()
    item3 = CtxItem()
    items = [item1, item2, item3]
    meta = CtxMeta()
    render.append_context(meta, items)
    render.append_context_item.assert_any_call(meta, item1)
    render.append_context_item.assert_any_call(meta, item2)
    render.append_context_item.assert_any_call(meta, item3)


def test_append_input(mock_window):
    """Test append input"""
    render = Render(mock_window)
    render.append_raw = MagicMock()
    item = CtxItem()
    item.input = "test"
    meta = CtxMeta()
    render.append_input(meta, item)
    render.append_raw.assert_called_once_with(meta, item, "> test", "msg-user")


def test_append_output(mock_window):
    """Test append output"""
    render = Render(mock_window)
    render.append_raw = MagicMock()
    item = CtxItem()
    item.output = "test"
    meta = CtxMeta()
    render.append_output(meta, item)
    render.append_raw.assert_called_once_with(meta, item, "test", "msg-bot")


def test_append_extra(mock_window):
    """Test append extra"""
    render = Render(mock_window)
    render.get_output_node = MagicMock()
    mock_window.core.filesystem = Filesystem(mock_window)
    render.images_appended = []
    item = CtxItem()
    item.images = ["test1"]
    item.files = ["test2"]
    item.urls = ["test3"]
    meta = CtxMeta()
    render.append_extra(meta, item)
    render.get_output_node().append.assert_called()


def test_append_chunk(mock_window):
    """Test append chunk"""
    render = Render(mock_window)
    render.append_chunk_start = MagicMock()
    render.append_block = MagicMock()
    item = CtxItem()
    meta = CtxMeta()
    render.append_chunk(meta, item, "test", True)
    render.append_chunk_start.assert_called_once()
    render.append_block.assert_called_once()


def test_append_block(mock_window):
    """Test append block"""
    render = Render(mock_window)
    render.get_output_node = MagicMock()
    cursor = MagicMock()
    cursor.movePosition = MagicMock()
    meta = CtxMeta()
    render.get_output_node().textCursor = MagicMock(return_value=cursor)
    render.append_block(meta)
    render.get_output_node().textCursor.assert_called_once()
    cursor.movePosition.assert_called_once()


def test_to_end(mock_window):
    """Test to end"""
    render = Render(mock_window)
    render.get_output_node = MagicMock()
    cursor = MagicMock()
    cursor.movePosition = MagicMock()
    render.get_output_node().textCursor = MagicMock(return_value=cursor)
    meta = CtxMeta()
    render.to_end(meta)
    render.get_output_node().textCursor.assert_called_once()
    cursor.movePosition.assert_called_once()


def test_append_raw(mock_window):
    """Test append raw"""
    render = Render(mock_window)
    render.get_output_node = MagicMock()
    item = CtxItem()
    meta = CtxMeta()
    render.append_raw(meta, item, "test", "msg-bot")
    render.get_output_node().append.assert_called_once()


def test_append_chunk_start(mock_window):
    """Test append chunk start"""
    render = Render(mock_window)
    render.get_output_node = MagicMock()
    cursor = MagicMock()
    cursor.movePosition = MagicMock()
    render.get_output_node().textCursor = MagicMock(return_value=cursor)
    item = CtxItem()
    meta = CtxMeta()
    render.append_chunk_start(meta, item)
    render.get_output_node().textCursor.assert_called_once()
    cursor.movePosition.assert_called_once()
    render.get_output_node().setTextCursor.assert_called_once()


def test_append_context_item(mock_window):
    """Test append context item"""
    render = Render(mock_window)
    render.append_input = MagicMock()
    render.append_output = MagicMock()
    render.append_extra = MagicMock()
    item = CtxItem()
    meta = CtxMeta()
    render.append_context_item(meta, item)
    render.append_input.assert_called_once_with(meta, item)
    render.append_output.assert_called_once_with(meta, item)
    render.append_extra.assert_called_once_with(meta, item, footer=True)


def test_get_image_html(mock_window):
    """Test get image html"""
    mock_window.core.config.set("lang", "en")
    mock_window.core.filesystem = Filesystem(mock_window)
    work_dir = mock_window.core.config.get_user_path()
    url = "%workdir%/test.png"
    render = Render(mock_window)
    render.body = Body(mock_window)
    render.helpers = Helpers(mock_window)
    html = render.body.get_image_html(url)
    if platform.system() == 'Windows':
        assert html == \
               '<a href="file:///' + work_dir + '\\test.png"><img src="' + work_dir + '\\test.png" width="400" ' \
                                                                                     'class="image"></a>\n        ' \
                                                                                     '<p><b>Image:</b> <a href="file:///' \
               + work_dir + '\\test.png">' + work_dir + '\\test.png</a></p>'
    else:
        assert html == \
               '<a href="file:///' + work_dir + '/test.png"><img src="' + work_dir + '/test.png" width="400" ' \
                                                                                     'class="image"></a>\n        ' \
                                                                                     '<p><b>Image:</b> <a href="file:///'\
               + work_dir + '/test.png">' + work_dir + '/test.png</a></p>'


def test_get_url_html(mock_window):
    """Test get url html"""
    mock_window.core.config.set("lang", "en")
    mock_window.core.filesystem = Filesystem(mock_window)
    url = "https://google.com"
    render = Render(mock_window)
    render.body = Body(mock_window)
    render.helpers = Helpers(mock_window)
    html = render.body.get_file_html(url)
    assert html == '<div><b>File:</b> <a href="https://google.com">https://google.com</a></div>'


def test_get_file_html(mock_window):
    """Test get file html"""
    mock_window.core.config.set("lang", "en")
    mock_window.core.filesystem = Filesystem(mock_window)
    work_dir = mock_window.core.config.get_user_path()
    url = "%workdir%/test.txt"
    render = Render(mock_window)
    render.body = Body(mock_window)
    render.helpers = Helpers(mock_window)
    html = render.body.get_file_html(url)
    if platform.system() == 'Windows':
        assert html == \
               '<div><b>File:</b> <a href="file:///' + work_dir + '\\test.txt">' + work_dir + '\\test.txt</a></div>'
    else:
        assert html == \
               '<div><b>File:</b> <a href="file:///' + work_dir + '/test.txt">' + work_dir + '/test.txt</a></div>'


def test_append(mock_window):
    """Test append"""
    item = CtxItem()
    meta = CtxMeta()
    render = Render(mock_window)
    render.get_output_node = MagicMock()
    cursor = MagicMock()
    cursor.movePosition = MagicMock()
    render.get_output_node().textCursor = MagicMock(return_value=cursor)
    render.append(meta, item, "test")
    render.get_output_node().textCursor.assert_called_once()


def test_append_timestamp(mock_window):
    """Test append timestamp"""
    render = Render(mock_window)
    render.is_timestamp_enabled = MagicMock(return_value=True)
    text = "test <tool>test</tool> test"
    ctx = CtxItem()
    ctx.input_timestamp = 1234567890
    assert render.append_timestamp(ctx, text, "msg-user").startswith("<span class=\"ts\">") is True


def test_replace_code_tags(mock_window):
    """Test replace code cmd tags"""
    render = Render(mock_window)
    render.body = Body(mock_window)
    render.helpers = Helpers(mock_window)
    text = "test <tool>test</tool> test"
    expected = "test <p class=\"cmd\">test</p> test"
    assert render.helpers.replace_code_tags(text) == expected


def test_pre_format_text(mock_window):
    """Test pre format text"""
    render = Render(mock_window)
    render.body = Body(mock_window)
    render.helpers = Helpers(mock_window)
    text = "test <tool>test</tool> test"
    expected = "test <p class=\"cmd\">test</p> test"
    assert render.helpers.pre_format_text(text) == expected


def test_post_format_text(mock_window):
    """Test post format text"""
    render = Render(mock_window)
    render.body = Body(mock_window)
    render.helpers = Helpers(mock_window)
    text = " test <tool>test</tool> test "
    expected = "test <tool>test</tool> test"
    assert render.helpers.post_format_text(text) == expected


def test_format_user_text(mock_window):
    """Test format user text"""
    render = Render(mock_window)
    render.body = Body(mock_window)
    render.helpers = Helpers(mock_window)
    text = " test <tool>test</tool> test "
    expected = " test &lt;tool&gt;test&lt;/tool&gt; test "  # no strip here
    assert render.helpers.format_user_text(text) == expected


def test_format_chunk(mock_window):
    """Test format chunk"""
    render = Render(mock_window)
    render.body = Body(mock_window)
    render.helpers = Helpers(mock_window)
    text = " abc "
    expected = " abc "
    assert render.helpers.format_chunk(text) == expected


def test_is_timestamp_enabled(mock_window):
    """Test is timestamp enabled"""
    render = Render(mock_window)
    mock_window.core.config.data['output_timestamp'] = True
    assert render.is_timestamp_enabled() is True


def test_get_input_node(mock_window):
    """Test get input node"""
    render = Render(mock_window)
    mock_window.ui.nodes['input'] = MagicMock()
    assert render.get_input_node() == mock_window.ui.nodes['input']
