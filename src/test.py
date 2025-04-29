from squares import generate_map
from graphic import create_terrain

for i in range(1):
    u = int(input())
    if u == 1:
        create_terrain(generate_map(1, 2**6+1, 100))
        with open('./static/html/not_3d_terrain.html', 'r+') as file:
            text = file.read()
            file.write(text[:52] + '<a href="http://localhost:8000/" class="button">Go to hell</a>' + text[52:])

        