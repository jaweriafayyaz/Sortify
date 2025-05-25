import pygame
import random
import math
import time

pygame.init()

# Visualization class
class VisualizationSettings:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 100, 255)
    GRAY = (200, 200, 200)
    FONT = pygame.font.SysFont('comicsans', 18)
    SMALL_FONT = pygame.font.SysFont('comicsans', 14)
    LARGE_FONT = pygame.font.SysFont('comicsans', 36)
    SIDE_PADDING = 100
    TOP_PADDING = 150

    def __init__(self, width, height, array):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sortify - Sorting Algorithm Visualizer")
        self.set_array(array)

    def set_array(self, array):
        self.array = array
        self.min_val = min(array)
        self.max_val = max(array)
        self.block_width = round((self.width - self.SIDE_PADDING) / len(array))
        self.block_height = math.floor((self.height - self.TOP_PADDING) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PADDING // 2

# Draw screen and UI
def draw_screen(vis, algo_name, ascending, result_text):
    vis.window.fill(vis.WHITE)
    title = vis.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, vis.GREEN)
    vis.window.blit(title, (vis.width / 2 - title.get_width() / 2, 5))

    controls = vis.FONT.render("R - Reset | SPACE - Start | A/D - Asc/Desc", 1, vis.BLACK)
    vis.window.blit(controls, (vis.width / 2 - controls.get_width() / 2, 45))

    algos = vis.FONT.render("I - Insertion | B - Bubble | S - Selection | M - Merge | Q - Quick", 1, vis.BLACK)
    vis.window.blit(algos, (vis.width / 2 - algos.get_width() / 2, 75))

    if result_text:
        result = vis.FONT.render(result_text, 1, vis.BLUE)
        vis.window.blit(result, (vis.width / 2 - result.get_width() / 2, 105))

    draw_array(vis)
    pygame.display.update()

# Draw array bars
def draw_array(vis, color_positions={}, clear_bg=False):
    array = vis.array
    if clear_bg:
        clear_rect = (vis.SIDE_PADDING // 2, vis.TOP_PADDING, vis.width - vis.SIDE_PADDING, vis.height - vis.TOP_PADDING)
        pygame.draw.rect(vis.window, vis.WHITE, clear_rect)

    for i, val in enumerate(array):
        x = vis.start_x + i * vis.block_width
        y = vis.height - (val - vis.min_val) * vis.block_height
        color = (100, 100, 255)
        if i in color_positions:
            color = color_positions[i]
        pygame.draw.rect(vis.window, color, (x, y, vis.block_width, vis.height))

        # Only draw value if block width is wide enough
        if vis.block_width > 20:
            label = vis.SMALL_FONT.render(str(val), 1, vis.BLACK)
            vis.window.blit(label, (x + vis.block_width//2 - label.get_width()//2, y - 20))

    if clear_bg:
        pygame.display.update()

# Sorting algorithms with yield
def bubble_sort(vis, asc=True):
    arr = vis.array
    for i in range(len(arr) - 1):
        for j in range(len(arr) - 1 - i):
            if (arr[j] > arr[j + 1] and asc) or (arr[j] < arr[j + 1] and not asc):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                draw_array(vis, {j: vis.GREEN, j + 1: vis.RED}, True)
                yield True
    yield False

def insertion_sort(vis, asc=True):
    arr = vis.array
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and ((arr[j] > key and asc) or (arr[j] < key and not asc)):
            arr[j + 1] = arr[j]
            j -= 1
            draw_array(vis, {j: vis.RED, j + 1: vis.GREEN}, True)
            yield True
        arr[j + 1] = key
        yield True
    yield False

def selection_sort(vis, asc=True):
    arr = vis.array
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if (arr[j] < arr[min_idx] and asc) or (arr[j] > arr[min_idx] and not asc):
                min_idx = j
            draw_array(vis, {min_idx: vis.RED, j: vis.GREEN}, True)
            yield True
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        yield True
    yield False

def merge_sort(vis, asc=True):
    arr = vis.array
    yield from _merge_sort(arr, 0, len(arr) - 1, vis, asc)
    yield False

def _merge_sort(arr, l, r, vis, asc):
    if l < r:
        m = (l + r) // 2
        yield from _merge_sort(arr, l, m, vis, asc)
        yield from _merge_sort(arr, m + 1, r, vis, asc)
        yield from merge(arr, l, m, r, vis, asc)

def merge(arr, l, m, r, vis, asc):
    L = arr[l:m + 1]
    R = arr[m + 1:r + 1]
    i = j = 0
    k = l
    while i < len(L) and j < len(R):
        if (L[i] <= R[j] and asc) or (L[i] >= R[j] and not asc):
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        draw_array(vis, {k: vis.GREEN}, True)
        yield True
        k += 1
    while i < len(L):
        arr[k] = L[i]
        i += 1
        draw_array(vis, {k: vis.RED}, True)
        yield True
        k += 1
    while j < len(R):
        arr[k] = R[j]
        j += 1
        draw_array(vis, {k: vis.RED}, True)
        yield True
        k += 1

def quick_sort(vis, asc=True):
    arr = vis.array
    yield from _quick_sort(arr, 0, len(arr) - 1, vis, asc)
    yield False

def _quick_sort(arr, low, high, vis, asc):
    if low < high:
        pi = yield from partition(arr, low, high, vis, asc)
        yield from _quick_sort(arr, low, pi - 1, vis, asc)
        yield from _quick_sort(arr, pi + 1, high, vis, asc)

def partition(arr, low, high, vis, asc):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if (arr[j] <= pivot and asc) or (arr[j] >= pivot and not asc):
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
        draw_array(vis, {j: vis.RED, high: vis.GREEN}, True)
        yield True
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    yield True
    return i + 1

# Main app
def main():
    WIDTH, HEIGHT = 900, 600
    SIZE = 30  # Reduce size to prevent overlap
    array = [random.randint(1, 100) for _ in range(SIZE)]
    vis = VisualizationSettings(WIDTH, HEIGHT, array)

    sorting = False
    ascending = True
    sort_algo = bubble_sort
    algo_name = "Bubble Sort"
    sort_gen = None
    result_text = ""
    start_time = None

    complexities = {
        "Bubble Sort": ("O(n²)", "O(1)"),
        "Insertion Sort": ("O(n²)", "O(1)"),
        "Selection Sort": ("O(n²)", "O(1)"),
        "Merge Sort": ("O(n log n)", "O(n)"),
        "Quick Sort": ("O(n log n)", "O(log n)")
    }

    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        if sorting:
            if start_time is None:
                start_time = time.time()
            try:
                next(sort_gen)
            except StopIteration:
                elapsed = round(time.time() - start_time, 3)
                t_c, s_c = complexities[algo_name]
                result_text = f"⏱ Time: {elapsed}s | ⌛ Time: {t_c} | 📦 Space: {s_c}"
                sorting = False
                start_time = None

        else:
            draw_screen(vis, algo_name, ascending, result_text)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    array = [random.randint(1, 100) for _ in range(SIZE)]
                    vis.set_array(array)
                    result_text = ""
                    sorting = False

                elif event.key == pygame.K_SPACE and not sorting:
                    sorting = True
                    sort_gen = sort_algo(vis, ascending)

                elif event.key == pygame.K_a and not sorting:
                    ascending = True
                elif event.key == pygame.K_d and not sorting:
                    ascending = False

                elif not sorting:
                    if event.key == pygame.K_b:
                        sort_algo = bubble_sort
                        algo_name = "Bubble Sort"
                    elif event.key == pygame.K_i:
                        sort_algo = insertion_sort
                        algo_name = "Insertion Sort"
                    elif event.key == pygame.K_s:
                        sort_algo = selection_sort
                        algo_name = "Selection Sort"
                    elif event.key == pygame.K_m:
                        sort_algo = merge_sort
                        algo_name = "Merge Sort"
                    elif event.key == pygame.K_q:
                        sort_algo = quick_sort
                        algo_name = "Quick Sort"

    pygame.quit()

if __name__ == "__main__":
    main()
