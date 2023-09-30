from dataclasses import dataclass, field
import math
import os
from typing import List, Optional, Tuple

from matplotlib import pyplot as plt
from matplotlib.lines import Line2D


@dataclass
class PlotterSetup:
    bg_file: str = field()
    bg_alpha: float = field()
    x_dim: List[int] = field(default_factory=list)
    y_dim: List[int] = field(default_factory=list)
    x_ticks: Optional[Tuple[List[int], List[str]]] = field(default=None)
    aspect_ratio: Optional[float] = field(default=None)
    enforce_original_aspect_ratio: bool = field(default=False)

    def __post_init__(self):
        self.width = abs(self.x_dim[1] - self.x_dim[0])
        self.height = abs(self.y_dim[1] - self.y_dim[0])
        # self.bg_file = os.path.join("/code","assets",self.bg_file)
        self.bg_file = os.path.join("assets",self.bg_file)


class Plotter:

    def __init__(self, config: PlotterSetup):
        self.aspect_ratio = 1
        self.dimensions = config.x_dim + config.y_dim
        self.bg_file = config.bg_file
        self.bg_alpha = config.bg_alpha
        self.fig, self.ax = plt.subplots()
        img = plt.imread(self.bg_file)
        self.ax.imshow(
            img, 
            extent=self.dimensions, 
            alpha=self.bg_alpha,
        )
        if (config.x_ticks is not None):
            self.ax.set_xticks(config.x_ticks[0], config.x_ticks[1])
        if config.enforce_original_aspect_ratio:
            self.aspect_ratio = abs(config.width/config.height)*len(img)/len(img[0])
            self.ax.set_aspect(self.aspect_ratio)
        elif (config.aspect_ratio is not None):
            self.aspect_ratio = abs(config.width/config.height)*config.aspect_ratio
            self.ax.set_aspect(self.aspect_ratio)
    

    def add_text_label(self, x, y, text, color, rotation=0, verticalalignment='center', horizontalalignment='center', x_transform = lambda x: x):
        if self.aspect_ratio != 1:
            m = math.tan(rotation * 2 * math.pi / 360)
            m *= self.aspect_ratio
            rotation = math.atan(m) / 2.0 / math.pi * 360
        self.ax.text(
            x_transform(x), 
            y, 
            text,
            verticalalignment=verticalalignment, 
            horizontalalignment=horizontalalignment,
            rotation=rotation, 
            rotation_mode='anchor',
            color=color,
        )
    
    def add_line(self, x0, y0, x1, y1, color='k', x_transform = lambda x: x):
        line = Line2D([x_transform(x0), x_transform(x1)], [y0, y1], color=color)
        self.ax.add_line(line)

    def add_arrow(self, x, y, dx, dy, color='k', x_transform = lambda x: x):
        x1 = x + dx
        dxp = x_transform(x1) - x_transform(x)
        self.ax.arrow(x_transform(x), y, dxp, dy, ls=':', fc=color, ec=color)

    def plot(self, model, x0, x1, color, x_transform = lambda x: x):
        dx = (x1 - x0) / 500.0
        x = [x_transform(x0 + n * dx) for n in range(501)]
        y = [model(x0 + n * dx) for n in range(501)]
        self.ax.plot(x, y, color)
    
    def save(self, fname, dpi=200):
        self.fig.savefig(fname, dpi=dpi, bbox_inches='tight')