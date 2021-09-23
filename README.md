# [img2texture](https://github.com/rtmigo/img2texture_py#readme) (DRAFT)

Command line utility for converting images to seamless tiles.

The resulting tiles can be used as textures in games, compositing and 3D modeling applications, etc.

<details>
  <summary>Sample images</summary>




![Source tiled](docs/1_orion_src_2x2.jpg)

Four copies of original image side by side (Orion galaxy by NASA/ESA).

We cannot use this image of Orion as an endless background: the seams are visible.

### Converted image

![Converted tiled](docs/2_orion_seamless.jpg2x2.jpg)

Four copies of the converted image: result of  `img2texture`. 

Each image is slightly reduced in size and the edges are modified with 
alpha-blending.

Seams no longer appear when merging images. This indicates that the converted image can be tiled and panned in any 
direction. It will feel endless and seamless.


</details>

# Install

```
$ pip3 install https://github.com/rtmigo/img2texture_py
```

# Run

```
$ img2texture /path/to/source.jpg /path/to/seamless_result.jpg 
```

