import pygame
import random
import math

# Initialize Pygame modules
pygame.init()


class VisualizationSettings:
    # Color constants (RGB)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BACKGROUND_COLOR = WHITE

    # Gradient colors for array bars
    COLOR_GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    # Fonts for text rendering
    FONT = pygame.font.SysFont('comicsans', 30)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)

    # UI padding constants
    SIDE_PADDING = 100
    TOP_PADDING = 150

    def __init__(self, width, height, array):
        """
        Initialize visualization settings with window size and array.
        Calculate block size based on array length and value range.
        """
        self.width = width
        self.height = height

        # Create Pygame display window
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sortify - Sorting Algorithm Visualization")

        # Setup array and derived properties
        self.set_array(array)

    def set_array(self, array):
        """
        Set the array to visualize and calculate scaling factors.
        """
        self.array = array
        self.min_value = min(array)
        self.max_value = max(array)

        # Calculate width of each block to fit in window with side padding
        self.block_width = round((self.width - self.SIDE_PADDING) / len(array))

        # Calculate height scaling for blocks relative to max and min values
        self.block_height = math.floor((self.height - self.TOP_PADDING) / (self.max_value - self.min_value))

        # Starting x coordinate for drawing the first block
        self.start_x = self.SIDE_PADDING // 2


def draw_screen(vis_settings, algorithm_name, ascending):
    """
    Draw the entire screen including titles, controls, and the array visualization.
    """
    # Fill background
    vis_settings.window.fill(vis_settings.BACKGROUND_COLOR)

    # Render and draw title text
    title = vis_settings.LARGE_FONT.render(
        f"{algorithm_name} - {'Ascending' if ascending else 'Descending'}", 1, vis_settings.GREEN)
    vis_settings.window.blit(title, (vis_settings.width / 2 - title.get_width() / 2, 5))

    # Render and draw controls text
    controls = vis_settings.FONT.render(
        "R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, vis_settings.BLACK)
    vis_settings.window.blit(controls, (vis_settings.width / 2 - controls.get_width() / 2, 45))

    # Render and draw algorithm selection info
    algo_info = vis_settings.FONT.render(
        "I - Insertion | B - Bubble | S - Selection | Q - Quick | M - Merge", 1, vis_settings.BLACK)
    vis_settings.window.blit(algo_info, (vis_settings.width / 2 - algo_info.get_width() / 2, 75))

    # Draw the array blocks
    draw_array(vis_settings)

    # Update the display
    pygame.display.update()


def draw_array(vis_settings, color_positions={}, clear_bg=False):
    """
    Draw the array as vertical bars.
    Optionally highlights certain bars with specified colors.
    """
    array = vis_settings.array

    # Clear only the area where array is drawn for smooth animation
    if clear_bg:
        clear_rect = (vis_settings.SIDE_PADDING // 2, vis_settings.TOP_PADDING,
                      vis_settings.width - vis_settings.SIDE_PADDING, vis_settings.height - vis_settings.TOP_PADDING)
        pygame.draw.rect(vis_settings.window, vis_settings.BACKGROUND_COLOR, clear_rect)

    # Draw each block representing an element in the array
    for i, val in enumerate(array):
        x = vis_settings.start_x + i * vis_settings.block_width
        y = vis_settings.height - (val - vis_settings.min_value) * vis_settings.block_height

        # Default color cycling through gradients for visual appeal
        color = vis_settings.COLOR_GRADIENTS[i % 3]

        # Override color if specified (e.g., for elements being compared or swapped)
        if i in color_positions:
            color = color_positions[i]

        # Draw the rectangle (bar) for the array element
        pygame.draw.rect(vis_settings.window, color, (x, y, vis_settings.block_width, vis_settings.height))

    if clear_bg:
        pygame.display.update()


def generate_random_array(size, min_value, max_value):
    """
    Generate a random array of specified size and value range.
    """
    return [random.randint(min_value, max_value) for _ in range(size)]


def bubble_sort(vis_settings, ascending=True):
    """
    Generator function to perform bubble sort and visualize each swap.
    Yields control after each significant operation to allow animation.
    """
    array = vis_settings.array
    n = len(array)

    for i in range(n - 1):
        for j in range(n - 1 - i):
            if (array[j] > array[j + 1] and ascending) or (array[j] < array[j + 1] and not ascending):
                array[j], array[j + 1] = array[j + 1], array[j]
                # Highlight swapped elements
                draw_array(vis_settings, {j: vis_settings.GREEN, j + 1: vis_settings.RED}, True)
                yield True  # Yield after each swap for animation
    yield False  # Sorting finished


def insertion_sort(vis_settings, ascending=True):
    """
    Generator function to perform insertion sort with visualization.
    """
    array = vis_settings.array
    n = len(array)

    for i in range(1, n):
        current = array[i]
        j = i
        while j > 0 and ((array[j - 1] > current and ascending) or (array[j - 1] < current and not ascending)):
            array[j] = array[j - 1]
            j -= 1
            array[j] = current
            # Highlight compared/swapped elements
            draw_array(vis_settings, {j: vis_settings.GREEN, j + 1: vis_settings.RED}, True)
            yield True
    yield False


def selection_sort(vis_settings, ascending=True):
    """
    Generator function to perform selection sort with visualization.
    """
    array = vis_settings.array
    n = len(array)

    for i in range(n):
        selected_index = i
        for j in range(i + 1, n):
            if (array[j] < array[selected_index] and ascending) or (array[j] > array[selected_index] and not ascending):
                selected_index = j
            draw_array(vis_settings, {selected_index: vis_settings.RED, j: vis_settings.GREEN}, True)
            yield True
        # Swap the found minimum/maximum with current position
        array[i], array[selected_index] = array[selected_index], array[i]
        draw_array(vis_settings, {i: vis_settings.GREEN, selected_index: vis_settings.RED}, True)
        yield True
    yield False


def quick_sort(vis_settings, ascending=True):
    """
    Generator function to perform quick sort with visualization.
    Uses recursive helper functions implemented as generators.
    """

    array = vis_settings.array

    def partition(start, end):
        """
        Partition the array segment and visualize swaps.
        """
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
        """
        Recursive quick sort implementation using generators.
        """
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
    """
    Generator function to perform merge sort with visualization.
    Uses recursive helper functions implemented as generators.
    """

    array = vis_settings.array

    def merge(start, mid, end):
        """
        Merge two sorted halves of the array segment and visualize.
        """
        merged = []
        left_idx = start
        right_idx = mid + 1

        # Merge elements while visualizing comparisons
        while left_idx <= mid and right_idx <= end:
            if (array[left_idx] <= array[right_idx] and ascending) or (array[left_idx] >= array[right_idx] and not ascending):
                merged.append(array[left_idx])
                left_idx += 1
            else:
                merged.append(array[right_idx])
                right_idx += 1
            draw_array(vis_settings, {left_idx-1: vis_settings.GREEN, right_idx-1: vis_settings.RED}, True)
            yield True

        # Append remaining elements from left half
        while left_idx <= mid:
            merged.append(array[left_idx])
            left_idx += 1
            draw_array(vis_settings, {left_idx-1: vis_settings.GREEN}, True)
            yield True

        # Append remaining elements from right half
        while right_idx <= end:
            merged.append(array[right_idx])
            right_idx += 1
            draw_array(vis_settings, {right_idx-1: vis_settings.RED}, True)
            yield True

        # Write back merged array to the original array and visualize
        for i, val in enumerate(merged):
            array[start + i] = val
            draw_array(vis_settings, {start + i: vis_settings.GREEN}, True)
            yield True

    def merge_sort_recursive(start, end):
        """
        Recursive merge sort implementation using generators.
        """
        if start < end:
            mid = (start + end) // 2
            yield from merge_sort_recursive(start, mid)
            yield from merge_sort_recursive(mid + 1, end)
            yield from merge(start, mid, end)

    yield from merge_sort_recursive(0, len(array) - 1)
    yield False


def main():
    """
    Main function to run the sorting visualization application.
    Handles user input, sorting control, and rendering.
    """
    running = True

    # Initial configuration
    width = 900
    height = 600
    array_size = 50
    min_val = 1
    max_val = 100

    # Generate initial random array and setup visualization
    array = generate_random_array(array_size, min_val, max_val)
    vis_settings = VisualizationSettings(width, height, array)

    sorting = False
    ascending = True
    sorting_algorithm = bubble_sort
    algorithm_name = "Bubble Sort"
    sorting_generator = None

    clock = pygame.time.Clock()

    while running:
        clock.tick(60)  # Limit to 60 FPS

        if sorting:
            try:
                # Perform next step of sorting
                next(sorting_generator)
            except StopIteration:
                # Sorting finished
                sorting = False
        else:
            # Draw screen normally if not sorting
            draw_screen(vis_settings, algorithm_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Keyboard controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reset array and visualization
                    array = generate_random_array(array_size, min_val, max_val)
                    vis_settings.set_array(array)
                    sorting = False

                elif event.key == pygame.K_SPACE and not sorting:
                    # Start sorting
                    sorting = True
                    sorting_generator = sorting_algorithm(vis_settings, ascending)

                elif event.key == pygame.K_a and not sorting:
                    # Set ascending order
                    ascending = True

                elif event.key == pygame.K_d and not sorting:
                    # Set descending order
                    ascending = False

                # Select sorting algorithm by key
                elif not sorting:
                    if event.key == pygame.K_b:
                        sorting_algorithm = bubble_sort
                        algorithm_name = "Bubble Sort"
                    elif event.key == pygame.K_i:
                        sorting_algorithm = insertion_sort
                        algorithm_name = "Insertion Sort"
                    elif event.key == pygame.K_s:
                        sorting_algorithm = selection_sort
                        algorithm_name = "Selection Sort"
                    elif event.key == pygame.K_q:
                        sorting_algorithm = quick_sort
                        algorithm_name = "Quick Sort"
                    elif event.key == pygame.K_m:
                        sorting_algorithm = merge_sort
                        algorithm_name = "Merge Sort"

                    # Redraw screen to update algorithm name
                    draw_screen(vis_settings, algorithm_name, ascending)

    pygame.quit()


if __name__ == "__main__":
    main()
