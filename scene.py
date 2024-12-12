from typing import Hashable, Tuple

from manim import *
from manim.mobject.text.text_mobject import remove_invisible_chars
from networkx.algorithms.bipartite.basic import color


class BinarySearchTreeTraversal(Scene):
    highlights = None
    arrow = None

    def construct(self):
        # TODO: Change these vertices & edges into actual binary tree
        vertices = ["L", "C", "P", "D"]
        nilVertices = ["T1", "T2", "T3", "T4", "T5"]
        edges = [
            ("L", "P"),
            ("L", "C"),
            ("C", "D")
        ]
        nilEdges = [
            ("C", "T1"),
            ("D", "T3"), ("D", "T2"),
            ("P", "T5"), ("P", "T4"),
        ]

        g1 = self.getGraph(vertices, edges)
        for vertice in nilVertices:
            g1.add_vertices(
                vertice,
                labels=True,
                vertex_config={
                    "fill_color": GRAY
            })

        for edge in nilEdges:
            g1.add_edges(edge)

        g1.change_layout('tree', root_vertex="L")

        # g1['D'].shift(RIGHT)

        title = Text("Binary Search Tree - In Order Traversal")

        self.play(Write(title))
        self.play(title.animate.to_edge(UP).scale(0.5))
        self.play(Write(g1))
        self.play(g1.animate.to_edge(RIGHT))
        self.wait()

        codeGroup = self.getPseudocode().to_edge(LEFT)
        self.play(
            Write(codeGroup)
        )

        self.highlights = self.getHighlighters(codeGroup)
        self.add(self.highlights)

        self.arrow = Arrow(
            start = (1, 2, 0),
            end = g1.vertices['L'].get_left(),
            color = YELLOW,
        )

        # Traverse from L (first) node
        self.play(
            *self.moveHighlight(0, 0),
            Write(self.arrow)
        )
        self.wait()
        self.moveHighlightAndPlay(0, 1)
        self.moveHighlightAndPlay(1, 4)
        self.wait()

        # L -> C
        self.play(
            *self.moveHighlight(4, 0),
            self.arrow.animate.put_start_and_end_on(
                start = (1, 2, 0),
                end = g1.vertices['C'].get_left(),
            )
        )
        self.wait()
        self.moveHighlightAndPlay(0, 1)
        self.moveHighlightAndPlay(1, 4)
        self.wait()

        # C -> T1
        self.play(
            *self.moveHighlight(4, 0),
            self.arrow.animate.put_start_and_end_on(
                start = (0, 0, 0),
                end = g1.vertices['T1'].get_left(),
            )
        )
        self.wait()
        self.moveHighlightAndPlay(0, 1)
        self.moveHighlightAndPlay(1, 2)
        self.wait()

        # T1 -> C
        self.play(
            *self.moveHighlight(2, 5),
            self.arrow.animate.put_start_and_end_on(
                start = (1, 2, 0),
                end = g1.vertices['C'].get_left(),
            ),
        )
        self.wait()
        # Print C
        self.moveHighlightAndPlay(5, 6)
        self.wait()

        # C -> D
        self.play(
            *self.moveHighlight(6, 0),
            self.arrow.animate.put_start_and_end_on(
                start = (1, -1, 0),
                end = g1.vertices['D'].get_left(),
            ),
        )
        self.wait()
        self.moveHighlightAndPlay(0, 1)
        self.moveHighlightAndPlay(1, 4)
        self.wait()

        # D -> T2
        self.play(
            *self.moveHighlight(4, 0),
            self.arrow.animate.put_start_and_end_on(
                start = (1, -2, 0),
                end = g1.vertices['T2'].get_left(),
            )
        )
        self.wait()
        self.moveHighlightAndPlay(0, 1)
        self.moveHighlightAndPlay(1, 2)
        self.wait()

        # T2 -> D
        self.play(
            *self.moveHighlight(2, 5),
            self.arrow.animate.put_start_and_end_on(
                start = (1, -1, 0),
                end = g1.vertices['D'].get_left(),
            ),
        )
        self.wait()
        # Print D
        self.moveHighlightAndPlay(5, 6)
        self.wait()

        # D -> T3
        self.play(
            *self.moveHighlight(6, 0),
            self.arrow.animate.put_start_and_end_on(
                start = (1, -2, 0),
                end = g1.vertices['T3'].get_left(),
            ),
        )
        self.wait()
        self.moveHighlightAndPlay(0, 1)
        self.moveHighlightAndPlay(1, 2)
        self.wait()

        # T3 -> D
        self.play(
            *self.moveHighlight(2, 8),
            self.arrow.animate.put_start_and_end_on(
                start = (1, -1, 0),
                end = g1.vertices['D'].get_left(),
            ),
        )
        self.wait()

        # D -> C
        self.play(
            *self.moveHighlight(8, 8),
            self.arrow.animate.put_start_and_end_on(
                start = (1, 2, 0),
                end = g1.vertices['C'].get_left(),
            ),
        )
        self.wait()

        # C -> L
        self.play(
            *self.moveHighlight(8, 5),
            self.arrow.animate.put_start_and_end_on(
                start = (1, 2, 0),
                end = g1.vertices['L'].get_left(),
            ),
        )
        self.wait()
        # Print L
        self.moveHighlightAndPlay(5, 6)
        self.wait()

        # L -> P
        self.play(
            *self.moveHighlight(6, 0),
            self.arrow.animate.put_start_and_end_on(
                start = (3, 2, 0),
                end = g1.vertices['P'].get_left(),
            ),
        )
        self.wait()
        self.moveHighlightAndPlay(0, 1)
        self.moveHighlightAndPlay(1, 4)
        self.wait()

        # P -> T4
        self.play(
            *self.moveHighlight(4, 0),
            self.arrow.animate.put_start_and_end_on(
                start = (3, 0, 0),
                end = g1.vertices['T4'].get_left(),
            ),
        )
        self.wait()
        self.moveHighlightAndPlay(0, 1)
        self.moveHighlightAndPlay(1, 2)
        self.wait()

        # T4 -> P
        self.play(
            *self.moveHighlight(2, 5),
            self.arrow.animate.put_start_and_end_on(
                start = (3, 2, 0),
                end = g1.vertices['P'].get_left(),
            ),
        )
        self.wait()
        # Print P
        self.moveHighlightAndPlay(5, 6)
        self.wait()

        # P -> T5
        self.play(
            *self.moveHighlight(6, 0),
            self.arrow.animate.put_start_and_end_on(
                start = (3, 0, 0),
                end = g1.vertices['T5'].get_left(),
            ),
        )
        self.wait()
        self.moveHighlightAndPlay(0, 1)
        self.moveHighlightAndPlay(1, 2)
        self.wait()

        # T5 -> P
        self.play(
            *self.moveHighlight(2, 8),
            self.arrow.animate.put_start_and_end_on(
                start = (3, 2, 0),
                end = g1.vertices['P'].get_left(),
            ),
        )
        self.wait()

        # P -> L
        self.play(
            *self.moveHighlight(8, 8),
            self.arrow.animate.put_start_and_end_on(
                start = (1, 2, 0),
                end = g1.vertices['L'].get_left(),
            ),
        )
        self.wait()

        self.play(Unwrite(self.arrow))
        self.wait()

    def getGraph(self, vertices: List[Hashable], edges: List[Tuple[Hashable, Hashable]]):
        return Graph(
            vertices,
            edges,
            layout="tree",
            root_vertex="L",
            labels=True,
            vertex_config={
                "radius": 0.5,
            }
        )

    def getPseudocode(self) -> Code:
        code = '''
def printInorder(node):
    if node is None:
        return
        
    printInorder(node.left)
    print(node.value)
    printInorder(node.right)
    
    return
        '''

        return Code(
            code=code,
            language="python",
            insert_line_no=False,
            line_spacing=1,
        )

    def getHighlighters(self, code: Code) -> VGroup:
        highlighters = VGroup()

        code.code = remove_invisible_chars(code.code)

        for line in code.code:
            highlighters.add(
                SurroundingRectangle(line)
                .set_fill(YELLOW)
                .set_opacity(0)
                .stretch_to_fit_width(code.background_mobject.get_width())
                .align_to(code.background_mobject, LEFT)
            )

        return highlighters

    def moveHighlight(self, prevLine: int, line: int) -> List:
        return [
            self.highlights[prevLine].animate.set_opacity(0),
            self.highlights[line].animate.set_opacity(0.3),
        ]

    def moveHighlightAndPlay(self, prevLine: int, line: int) -> None:
        self.play(self.highlights[prevLine].animate.set_opacity(0))
        self.play(self.highlights[line].animate.set_opacity(0.3))
