from typing import Hashable, Tuple

from manim import *
from manim.mobject.text.text_mobject import remove_invisible_chars


class BinarySearchTreeSearch(Scene):
    highlights = None
    arrow = None
    resultText = []

    def construct(self):
        # TODO: Change these vertices & edges into actual binary tree
        vertices = ["L", "C", "P", "F", "A", "E", "G", "N", "Y"]
        edges = [
            ("L", "P"),
            ("L", "C"),
            ("C", "F"),

            ("C", "A"),
            ("F", "G"), ("F", "E"),
            ("P", "Y"), ("P", "N"),
        ]

        g1 = self.getGraph(vertices, edges)

        title = Text("Binary Search Tree - Search")

        self.play(Write(title))
        self.play(title.animate.to_edge(UP).scale(0.5))
        self.play(Write(g1))
        self.play(g1.animate.shift([0, -0.2, 0]).to_edge(RIGHT))
        self.wait()

        codeGroup = self.getPseudocode().scale(0.8).to_edge(LEFT)
        subtitle = Text("Finding 'E'").scale(0.4).next_to(codeGroup, UP)

        self.play(
            Write(subtitle),
            Write(codeGroup),
        )

        self.highlights = self.getHighlighters(codeGroup)
        self.add(self.highlights)

        self.arrow = Arrow(
            start = (1, 2, 0),
            end = g1.vertices['L'].get_left(),
            color = YELLOW,
        )

        # Traverse from L (first) node
        # Finding E
        self.play(
            *self.moveHighlight(0, 0),
            Write(self.arrow)
        )
        self.wait()
        self.moveHighlightAndPlay(0, 1)
        self.moveHighlightAndPlay(1, 4)
        self.moveHighlightAndPlay(4, 7)
        self.wait()

        # L -> C
        self.play(
            *self.moveHighlight(7, 0),
            self.arrow.animate.put_start_and_end_on(
                start = (1, 2, 0),
                end = g1.vertices['C'].get_left(),
            )
        )
        self.wait()
        self.moveHighlightAndPlay(0, 1)
        self.moveHighlightAndPlay(1, 4)
        self.moveHighlightAndPlay(4, 5)
        self.wait()

        # C -> F
        self.play(
            *self.moveHighlight(5, 0),
            self.arrow.animate.put_start_and_end_on(
                start = (1, -1, 0),
                end = g1.vertices['F'].get_left(),
            ),
        )
        self.wait()
        self.moveHighlightAndPlay(0, 1)
        self.moveHighlightAndPlay(1, 4)
        self.moveHighlightAndPlay(4, 7)
        self.wait()

        # F -> E
        self.play(
            *self.moveHighlight(7, 0),
            self.arrow.animate.put_start_and_end_on(
                start = (1, -2, 0),
                end = g1.vertices['E'].get_left(),
            )
        )
        self.wait()
        self.moveHighlightAndPlay(0, 1)
        self.moveHighlightAndPlay(1, 2)
        self.wait()

        self.printNode("E")

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
def search(node, key):
    if node is None or node.key == key:
        return node
        
    if node.key < key:
        return search(node.right, key)
        
    return search(node.left, key)
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
        self.play(
            self.highlights[prevLine].animate.set_opacity(0)
        )
        self.play(
            self.highlights[line].animate.set_opacity(0.3)
        )

    def printNode(self, value: str) -> None:
        text = Text(value)

        try:
            lastText = self.resultText[-1]
            text = text.next_to(lastText, RIGHT)
        except IndexError as e:
            text = text.to_corner(DL)

        self.resultText.append(text)

        self.play(
            Write(text)
        )