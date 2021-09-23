# [img2texture](https://github.com/rtmigo/img2texture_py#readme) (DRAFT)

Command line utility for converting images to seamless tiles.

The resulting tiles can be used as textures in games, compositing and 3D modeling applications, etc.

<details>
  <summary>Sample images</summary>

### Source image

This is an image of the Orion galaxy from NASA / ESA.

![Source image](docs/1_orion_src.jpg) 

### Source tiled 

The original image cannot be used as an endless background: the seams are visible.

![Source tiled](docs/1_orion_src_2x2.jpg)

### Converted image

This is the result of `img2texture`. The image is slightly reduced in size and the edges are modified.

![Converted image](docs/2_orion_seamless.jpg)

### Converted tiled

The seams between the tiles are disappeared.

![Converted tiled](docs/2_orion_seamless.jpg2x2.jpg)


</details>

# Install

```
$ pip3 install https://github.com/rtmigo/img2texture_py
```

# Run

```
$ img2texture /path/to/source.jpg /path/to/seamless_result.jpg 
```

