from manim import *


class PSOPosPlot(Scene):
    def __init__(self, pso, max_iterations, BOUNDS):
        super().__init__()

        self.pso = pso
        self.max_iterations = max_iterations
        self.bounds = BOUNDS

    def construct(self):
        plane = NumberPlane(
            x_range=(0, self.max_iterations),
            y_range=self.bounds,
            x_length=10,
            y_length=5,
            axis_config={"include_numbers": True},
            y_axis_config={
                "label_direction": LEFT
            }
        )
        plane.center()

        x_label = plane.get_x_axis_label(
            Tex("iteration"), edge=DOWN, direction=DOWN, buff=0.5
        )
        y_label = plane.get_y_axis_label(
            Tex("x"), edge=LEFT, direction=LEFT, buff=0.5
        )

        self.add(plane, x_label, y_label)

        for particle in self.pso.swarm.particles:
            line_graph = plane.plot_line_graph(
                x_values=range(self.max_iterations + 1),
                y_values=particle.pos_history,
                line_color=GOLD_E,
                add_vertex_dots=False,
                stroke_width=4,
            )
            self.add(line_graph)

class PSOFitnessPlot(Scene):
    def __init__(self, pso, max_iterations):
        super().__init__()

        self.pso = pso
        self.max_iterations = max_iterations

    def construct(self):
        plane = NumberPlane(
            x_range=(0, self.max_iterations),
            y_range=(0, 50, 5),
            x_length=10,
            y_length=5,
            axis_config={"include_numbers": True},
            y_axis_config={
                "label_direction": LEFT
            }
        )
        plane.center()

        x_label = plane.get_x_axis_label(
            Tex("iteration"), edge=DOWN, direction=DOWN, buff=0.5
        )
        y_label = plane.get_y_axis_label(
            Tex("f(x)"), edge=LEFT, direction=LEFT, buff=0.5
        )

        self.add(plane, x_label, y_label)

        for particle in self.pso.swarm.particles:
            line_graph = plane.plot_line_graph(
                x_values=range(self.max_iterations + 1),
                y_values=list(map(lambda v: 50 if v >= 50 else v, particle.fitness_value_history)),
                line_color=random_color(),
                add_vertex_dots=False,
                stroke_width=4,
            )

            self.add(line_graph)
