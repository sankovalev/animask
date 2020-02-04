# Animask
Animated (GIF) masks after each epoch.

Only semantic segmentation is supported.

![Example with background](https://github.com/sankovalev/animask/blob/master/example.gif)
---
## Installation
First you need to install gifsicle:
```sh
$ sudo apt-get install gifsicle
```
Then install animask by pip or directly from repo:
```sh
$ pip install animask
```
or
```sh
$ pip install git+https://github.com/sankovalev/animask.git
```
### Usage
```python
from animask import Animask

# init object with the image that the mask will be predicted for
animated = Animask(image)

# === repeat this every epoch: ===
# train your model ...
# predict mask for image
# and then add to object as numpy array
animated.add(predicted_mask)
# === finish training ===

# save your gif
animated.save("path_to_file_here.gif")
```
By default, masks will be saved without a background. To apply masks over the original image, save it with flag:
```python
animated.save("path_to_file_here.gif", with_background=True)
```
Additionally, you can configure mask titles, color or transparency and etc.

### License
MIT

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)
   [L4F]: <https://github.com/sankovalev/animask>