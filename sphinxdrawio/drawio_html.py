from xml.dom import minidom

import os.path
import platform
from hashlib import sha1
from typing import Dict, Any, List
import uuid

import sphinx
from docutils import nodes
from docutils.nodes import Node
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.errors import SphinxError
from sphinx.util import logging, ensuredir
from sphinx.util.docutils import SphinxDirective, SphinxTranslator
from sphinx.util.fileutil import copy_asset
from sphinx.writers.html import HTMLTranslator

logger = logging.getLogger(__name__)

styleset = set()

class DrawIOError(SphinxError):
    category = 'DrawIO-HTML Error'

# noinspection PyPep8Naming
class drawio_html(nodes.General, nodes.Inline, nodes.Element):
    pass

class DrawIOHTML(SphinxDirective):
    has_content = True
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        "page"  : directives.split_escaped_whitespace,
        "expanded"  : directives.flag,
        "hide-nav": directives.flag,
        "force-name": directives.flag,
    }

    def run(self) -> List[Node]:
        if self.arguments:
            rel_filename, filename = self.env.relfn2path(self.arguments[0])
            self.env.note_dependency(rel_filename)
            if not os.path.exists(filename):
                return [self.state.document.reporter.warning(
                    "External draw.io file {} not found.".format(filename),
                    lineno=self.lineno
                )]

        else:
            return [self.state_machine.reporter.warning(
                "Ignoring 'drawio-html' directive without argument.",
                line=self.lineno,
            )]

        node = drawio_html()
        node["filename"] = filename
        if "page" in self.options:
            node["page"] = self.options["page"]
        node["doc_name"] = self.env.docname
        
        if "hide-nav" in self.options:
            node["hide-nav"] = True
            node["expanded"] = True
        else:
            node["hide-nav"] = False
            if "expanded" in self.options:
                node["expanded"] = True
            else:
                node["expanded"] = False
        
        if "force-name" in self.options:
            node["force-name"] = True
        else:
            node["force-name"] = False

        if self.content:
            node["styles"] = self.content

        self.add_name(node)
        return [node]

def render_drawio_html(self: HTMLTranslator, node: drawio_html):
    """
        self -> HTMLTranslator
        node -> drawio_html object
    """
    filename = node["filename"]
    print("\n\n\n")
    print(type(self))
    print("\n\n\n")
    try:
        with open(filename) as fp:
            content = minidom.parse(filename).firstChild

            if 'page' in node:
                to_remove = [
                    (d.getAttribute('name'), d) for d in content.getElementsByTagName('diagram') 
                               if d.getAttribute('name') not in node["page"]
                ]
                for _dummy, n in to_remove:
                    content.removeChild(n)
            main_id = uuid.uuid4().hex[:8]

            self.body.append('<div id="{id}" '.format(id=main_id))
            if node["expanded"]:
                self.body.append("drawio-expanded=1 ")
            if node["hide-nav"]:
                self.body.append("drawio-nonav=1 ")
            if node["force-name"]:
                self.body.append("drawio-show-name=1 ")
            self.body.append('class="drawio-html-container-div">\n')
            
            if "styles" in node:
                for s, o, value in node["styles"].xitems():
                    styleset.add("div#{id} {style}\n".format(id=main_id, style=value))

            self.body.append('<div class="drawio-data">\n')
            # Format of the content is <mxfile> <diagram></diagram></mxfile>
            self.body.append(content.toxml())
            self.body.append('</div>\n')
            self.body.append('</div>\n')

    except DrawIOError as e:
        logger.warning("drawio filename: {}: {}".format(filename, e))
        raise nodes.SkipNode
    raise nodes.SkipNode


def on_build_finished(app: Sphinx, exc: Exception) -> None:
    if exc is None:
        this_file_path = os.path.dirname(os.path.realpath(__file__))
        src = os.path.join(this_file_path, "drawio_html.js")
        dst = os.path.join(app.outdir, "_static")
        copy_asset(src, dst)

        src = os.path.join(this_file_path, "drawio_html.css")
        dst = os.path.join(app.outdir, "_static")
        copy_asset(src, dst)

        # Add the styles
        with open(os.path.join(dst, "drawio_html.css"), "a") as fp:
            for s in styleset:
                fp.write(s)

def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_node(drawio_html, html=(render_drawio_html, None))
    app.add_directive("drawio-html", DrawIOHTML)

    # Add CSS file to the HTML static path for add_css_file
    app.connect("build-finished", on_build_finished)
    app.add_js_file("drawio_html.js")
    app.add_css_file("drawio_html.css")

    return {"version": "0.1"}
