import os
import pygame
import neat

from Bird import Bird
from Pipe import Pipe
from Base import Base

# Initializing fonts in pygame
pygame.font.init()

# Width and Height of the window
WIN_WIDTH = 500
WIN_HEIGHT = 800

# Generation number
GEN = 0

# background image
BG_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "bg.png")))

# Loading font family
STAT_FONT = pygame.font.SysFont("ubuntu", 30)


def draw_window(win, birds, pipes, base, score, gen):
    """Draw principal elements in the window."""

    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (10, 10))

    text = STAT_FONT.render("Generation: " + str(gen), 1, (255, 255, 255))
    win.blit(text, (10, 50))

    base.draw(win)

    for bird in birds:
        bird.draw(win)

    pygame.display.update()


def main(genomes, config):
    """Run the main process to execute the game."""

    global GEN
    GEN += 1
    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(730)
    pipes = [Pipe(600)]

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    clock = pygame.time.Clock()

    run = True

    score = 0

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output = nets[x].activate(
                (bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()

        add_pipe = False
        rem = []

        for pipe in pipes:
            for x, bird in enumerate(birds):

                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))

        for r in rem:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        base.move()

        draw_window(win, birds, pipes, base, score, GEN)


def run(config_path):
    """Prepare neat config to run neural networks."""

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(main, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
