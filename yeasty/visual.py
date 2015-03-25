import pygame
import pygame.gfxdraw as gfx
from pygame.color import Color
from pymunk import Vec2d
import random

# Get some funky colors
COLORS = pygame.color.THECOLORS.items()
random.shuffle(COLORS)

# TODO push / pop for state


class Visualisation(object):
    def __init__(self):
        self.height = 100
        self.offx = 50
        self.offy = 50
        self.zoom = .5
        self.fill_color = Color('white')
        self.outline_color = Color('white')
        self.surface = None

    def set_size(self, w, h):
        self.height = h
        self.offx = -w / 2
        self.offy = -h / 2

    def set_rect(self, rect):
        self.height = rect.height
        c = rect.center
        self.offx = -c[0]
        self.offy = -c[1]

    # inline scaling to the surface
    def to_surface_x(self, x):
        return int((x * self.zoom) - self.offx)

    def to_surface_y(self, y):
        return int(self.height - ((y * self.zoom) - self.offy))

    def to_surface_scale(self, v):
        return int(v * self.zoom)

    # Python versions
    def to_surface(self, x, y):
        newx = (x * self.zoom) - self.offx
        newy = (y * self.zoom) - self.offy
        newy = self.height - newy
        return newx, newy

    def to_world(self, x, y):
        x = float(x)
        y = float(y)
        newx = (x + self.offx) / self.zoom
        # y is flipped
        h = self.height
        newy = (h - y + self.offy) / self.zoom
        return newx, newy

    # Pygame drawing routines. One day these will call the interface directly
    def line(self, p1, p2):
        ix1 = self.to_surface_x(p1.x)
        iy1 = self.to_surface_y(p1.y)
        ix2 = self.to_surface_x(p2.x)
        iy2 = self.to_surface_y(p2.y)
        gfx.line(self.surface, ix1, iy1, ix2, iy2, self.outline_color)

    def circle(self, center, r, fill):
        ix = self.to_surface_x(center.x)
        iy = self.to_surface_y(center.y)
        ir = self.to_surface_scale(r)
        if fill:
            gfx.filled_circle(self.surface, ix, iy, ir, self.fill_color)
        gfx.aacircle(self.surface, ix, iy, ir, self.outline_color)

    # TODO Use the Vertices class here
    def polygon(self, vertices, vcount, fill):
        verts = []
        for i in range(vcount):
            ix = self.to_surface_x(vertices[i].x)
            iy = self.to_surface_y(vertices[i].y)
            verts.append((ix, iy))
        if fill:
            gfx.filled_polygon(self.surface, verts, self.fill_color)
        gfx.aapolygon(self.surface, verts, self.outline_color)

    # def hit_test(self, world, x, y):
        # x, y = self.to_world(x, y)
        # # Make a little square, and see who is there
        # aabb = AABB(x - .00001, y - .00001, x + .00001, y + .00001)
        # hits = world.query_aabb(aabb)
        # if hits:
            # # Just send back the first one, and the world location
            # return hits[0], Vec2(x, y)
        # return None

    def render(self, surface, sim):
        self.surface = surface

        out = Color(255, 255, 255)
        self.outline_color = out
        for c in sim.cells:
            self.fill_color = COLORS[c.color][1]
            self.circle(c.body.position, c.shape.radius, True)
            if c.dead:
                self.fill_color = Color(55, 55, 55)
                self.circle(c.body.position, c.shape.radius * .5, True)
            v = Vec2d(c.shape.radius, 0)
            v.rotate(c.body.angle)
            v += c.body.position
            self.line(c.body.position, v)
        # draw the bonds
        ok = Color(0, 255, 0, 200)
        self.outline_color = ok
        for b in sim.bonds:
            c = b.j1
            pv1 = c.a.position + c.anchr1.rotated(c.a.angle)
            pv2 = c.b.position + c.anchr2.rotated(c.b.angle)
            self.line(pv1, pv2)
            c = b.j2
            pv1 = c.a.position + c.anchr1.rotated(c.a.angle)
            pv2 = c.b.position + c.anchr2.rotated(c.b.angle)
            self.line(pv1, pv2)

            # Display the stressed joints
            # stressed = Color(255, 0, 0, 200)
            # if not b.growing:
                # if (ja - jb).length > .1:
                    # self.viz.fill_color = stressed
                    # p = ja + (jb - ja)/2.0
                    # self.viz.circle(p, .25, True)
                    # self.viz.outline_color = ok
