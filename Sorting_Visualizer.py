import pygame
import random
import math
import time
pygame.init()

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    GREY = 128, 128, 128
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('comicsans', 30)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)

    SIDE_PAD = 100
    TOP_PAD = 150
  

    def __init__(self, width, height, lst) :
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Sorting Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

def draw(draw_info):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

	# title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
	# draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 45))

    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 75))

    draw_list(draw_info)
    pygame.display.update()



def draw_list(draw_info, color_positions = {}):
    lst = draw_info.lst


    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i] 

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))



def generate_starting_list(n, min_val, max_val):
    lst = []
    for i in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst


def bubble_sort(draw_info, ascending = True):
    lst = draw_info.lst
    n = len(lst)

    for i in range(n):
        for j in range(0, n-i-1):
            if ascending:
                if lst[j] > lst[j+1]:
                    lst[j], lst[j+1] = lst[j+1], lst[j]
            else:
                if lst[j] < lst[j+1]:
                    lst[j], lst[j+1] = lst[j+1], lst[j]

            draw_list(draw_info, {j: DrawInformation.RED, j+1: DrawInformation.RED})
            draw(draw_info) # Adjust the delay for visualization

            draw_list(draw_info)
            pygame.display.update()

    return lst


def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        key = lst[i]
        j = i - 1

        while j >= 0 and ((ascending and lst[j] > key) or (not ascending and lst[j] < key)):
            lst[j + 1] = lst[j]
            j -= 1
            draw_list(draw_info, {j + 1: DrawInformation.RED})
            draw(draw_info)  # Adjust the delay for visualization
            draw_list(draw_info)
            pygame.display.update()

        lst[j + 1] = key
        draw_list(draw_info, {i: DrawInformation.GREEN})
        draw(draw_info)  # Adjust the delay for visualization
        draw_list(draw_info)
        pygame.display.update()

    return lst



def merge_sort(draw_info, ascending=True):
    def merge(arr, left, mid, right):
        n1 = mid - left + 1
        n2 = right - mid

        L = [0] * n1
        R = [0] * n2

        for i in range(n1):
            L[i] = arr[left + i]
        for i in range(n2):
            R[i] = arr[mid + 1 + i]

        i = 0
        j = 0
        k = left

        while i < n1 and j < n2:
            if (ascending and L[i] <= R[j]) or (not ascending and L[i] >= R[j]):
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1

        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1

    def merge_sort_recursive(arr, left, right):
        if left < right:
            mid = (left + right) // 2
            merge_sort_recursive(arr, left, mid)
            merge_sort_recursive(arr, mid + 1, right)
            merge(arr, left, mid, right)

            # Delay and update the visualization
            draw_list(draw_info, {i: DrawInformation.RED for i in range(left, right + 1)})
            draw(draw_info)
            # time.sleep(0.1)  # Adjust the delay duration as needed
            draw_list(draw_info)
            pygame.display.update()


    arr = draw_info.lst
    merge_sort_recursive(arr, 0, len(arr) - 1)

    return arr


def main():
    run = True 
    clock = pygame.time.Clock()

    n = 100
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(1200, 600, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(60)
        draw(draw_info)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False

            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)

            elif event.key == pygame.K_a and sorting == False:
                ascending = True

            elif event.key == pygame.K_d and sorting == False:
                ascending = False

            elif event.key == pygame.K_b and sorting == False:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"

            elif event.key == pygame.K_i and sorting == False:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"

            elif event.key == pygame.K_m and sorting == False:
                sorting_algorithm = merge_sort
                sorting_algo_name = "Merge Sort"

    pygame.quit()

if __name__ == "__main__":
    main()
