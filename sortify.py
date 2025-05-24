import pygame
import random
import math

pygame.init()

class VisualizationSettings:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BACKGROUND_COLOR = WHITE

    COLOR_GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('comicsans', 30)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)

    SIDE_PADDING = 100
    TOP_PADDING = 150

    def __init__(self, width, height, array):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sortify - Sorting Algorithm Visualization")
        self.set_array(array)

    def set_array(self, array):
        self.array = array
        self.min_value = min(array)
        self.max_value = max(array)

        self.block_width = round((self.width - self.SIDE_PADDING) / len(array))
        self.block_height = math.floor((self.height - self.TOP_PADDING) / (self.max_value - self.min_value))
        self.start_x = self.SIDE_PADDING // 2


def draw_screen(vis_settings, algorithm_name, ascending):
    vis_settings.window.fill(vis_settings.BACKGROUND_COLOR)

    title = vis_settings.LARGE_FONT.render(
        f"{algorithm_name} - {'Ascending' if ascending else 'Descending'}", 1, vis_settings.GREEN)
    vis_settings.window.blit(title, (vis_settings.width / 2 - title.get_width() / 2, 5))

    controls = vis_settings.FONT.render(
        "R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, vis_settings.BLACK)
    vis_settings.window.blit(controls, (vis_settings.width / 2 - controls.get_width() / 2, 45))

    algo_info = vis_settings.FONT.render(
        "I - Insertion | B - Bubble | S - Selection | Q - Quick | M - Merge", 1, vis_settings.BLACK)
    vis_settings.window.blit(algo_info, (vis_settings.width / 2 - algo_info.get_width() / 2, 75))

    draw_array(vis_settings)
    pygame.display.update()


def draw_array(vis_settings, color_positions={}, clear_bg=False):
    array = vis_settings.array

    if clear_bg:
        clear_rect = (vis_settings.SIDE_PADDING // 2, vis_settings.TOP_PADDING,
                      vis_settings.width - vis_settings.SIDE_PADDING, vis_settings.height - vis_settings.TOP_PADDING)
        pygame.draw.rect(vis_settings.window, vis_settings.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(array):
        x = vis_settings.start_x + i * vis_settings.block_width
        y = vis_settings.height - (val - vis_settings.min_value) * vis_settings.block_height

        color = vis_settings.COLOR_GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(vis_settings.window, color, (x, y, vis_settings.block_width, vis_settings.height))

    if clear_bg:
        pygame.display.update()


def generate_random_array(size, min_value, max_value):
    return [random.randint(min_value, max_value) for _ in range(size)]


def bubble_sort(vis_settings, ascending=True):
    array = vis_settings.array
    n = len(array)

    for i in range(n - 1):
        for j in range(n - 1 - i):
            if (array[j] > array[j + 1] and ascending) or (array[j] < array[j + 1] and not ascending):
                array[j], array[j + 1] = array[j + 1], array[j]
                draw_array(vis_settings, {j: vis_settings.GREEN, j + 1: vis_settings.RED}, True)
                yield True
    yield False


def insertion_sort(vis_settings, ascending=True):
    array = vis_settings.array
    n = len(array)

    for i in range(1, n):
        current = array[i]
        j = i
        while j > 0 and ((array[j - 1] > current and ascending) or (array[j - 1] < current and not ascending)):
            array[j] = array[j - 1]
            j -= 1
            array[j] = current
            draw_array(vis_settings, {j: vis_settings.GREEN, j + 1: vis_settings.RED}, True)
            yield True
    yield False


def selection_sort(vis_settings, ascending=True):
    array = vis_settings.array
    n = len(array)

    for i in range(n):
        selected_index = i
        for j in range(i + 1, n):
            if (array[j] < array[selected_index] and ascending) or (array[j] > array[selected_index] and not ascending):
                selected_index = j
            draw_array(vis_settings, {selected_index: vis_settings.RED, j: vis_settings.GREEN}, True)
            yield True
        array[i], array[selected_index] = array[selected_index], array[i]
        draw_array(vis_settings, {i: vis_settings.GREEN, selected_index: vis_settings.RED}, True)
        yield True
    yield False


def quick_sort(vis_settings, ascending=True):
    array = vis_settings.array

    def partition(start, end):
        pivot = array[end]
        i = start - 1
        for j in range(start, end):
            if (array[j] <= pivot and ascending) or (array[j] >= pivot and not ascending):
                i += 1
                array[i], array[j] = array[j], array[i]
                draw_array(vis_settings, {i: vis_settings.GREEN, j: vis_settings.RED}, True)
                yield True
        array[i + 1], array[end] = array[end], array[i + 1]
        draw_array(vis_settings, {i + 1: vis_settings.GREEN, end: vis_settings.RED}, True)
        yield True
        return i + 1

    def quick_sort_recursive(start, end):
        if start < end:
            partition_gen = partition(start, end)
            while True:
                try:
                    yield next(partition_gen)
                except StopIteration as e:
                    pivot_index = e.value
                    break
            yield from quick_sort_recursive(start, pivot_index - 1)
            yield from quick_sort_recursive(pivot_index + 1, end)

    yield from quick_sort_recursive(0, len(array) - 1)
    yield False


def merge_sort(vis_settings, ascending=True):
    array = vis_settings.array

    def merge(start, mid, end):
        merged = []
        left_idx = start
        right_idx = mid + 1

        while left_idx <= mid and right_idx <= end:
            if (array[left_idx] <= array[right_idx] and ascending) or (array[left_idx] >= array[right_idx] and not ascending):
                merged.append(array[left_idx])
                left_idx += 1
            else:
                merged.append(array[right_idx])
                right_idx += 1
            draw_array(vis_settings, {left_idx-1: vis_settings.GREEN, right_idx-1: vis_settings.RED}, True)
            yield True

        while left_idx <= mid:
            merged.append(array[left_idx])
            left_idx += 1
            draw_array(vis_settings, {left_idx-1: vis_settings.GREEN}, True)
            yield True

        while right_idx <= end:
            merged.append(array[right_idx])
            right_idx += 1
            draw_array(vis_settings, {right_idx-1: vis_settings.RED}, True)
            yield True

        for i, val in enumerate(merged):
            array[start + i] = val
            draw_array(vis_settings, {start + i: vis_settings.GREEN}, True)
            yield True

    def merge_sort_recursive(start, end):
        if start >= end:
            return
        mid = (start + end) // 2
        yield from merge_sort_recursive(start, mid)
        yield from merge_sort_recursive(mid + 1, end)
        yield from merge(start, mid, end)

    yield from merge_sort_recursive(0, len(array) - 1)
    yield False


def main():
    run = True
    clock = pygame.time.Clock()

    array_size = 50
    min_value = 0
    max_value = 100

    array = generate_random_array(array_size, min_value, max_value)
    vis_settings = VisualizationSettings(800, 600, array)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algorithm_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw_screen(vis_settings, sorting_algorithm_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                array = generate_random_array(array_size, min_value, max_value)
                vis_settings.set_array(array)
                sorting = False

            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(vis_settings, ascending)

            elif event.key == pygame.K_a and not sorting:
                ascending = True

            elif event.key == pygame.K_d and not sorting:
                ascending = False

            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algorithm_name = "Insertion Sort"

            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algorithm_name = "Bubble Sort"

            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algorithm_name = "Selection Sort"

            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm = quick_sort
                sorting_algorithm_name = "Quick Sort"

            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm = merge_sort
                sorting_algorithm_name = "Merge Sort"

    pygame.quit()


if __name__ == "__main__":
    main()
