"""
Copyright (C) 2020

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import inspect
import collections

import numpy as np

from . import transpose, color, debug


def crop(index, ymin, ymax, xmin, xmax):
    def make(image):
        return image[ymin:ymax, xmin:xmax]

    def decorate(mdp):
        class MDP(mdp):
            class Controller(mdp.Controller):
                def get_state(self):
                    state = super().get_state()
                    state['inputs'][index] = make(state['inputs'][index])
                    return state

            def describe_blob(self):
                encoding = super().describe_blob()
                for model in encoding['models']:
                    model['inputs'][index]['shape'] = make(np.zeros(model['inputs'][index]['shape'])).shape
                return encoding
        return MDP
    return decorate


def crop_hwc(index, ymin, ymax, xmin, xmax):
    def make(image):
        return image[ymin:ymax, xmin:xmax, :]

    def decorate(mdp):
        class MDP(mdp):
            class Controller(mdp.Controller):
                def get_state(self):
                    state = super().get_state()
                    state['inputs'][index] = make(state['inputs'][index])
                    return state

            def describe_blob(self):
                encoding = super().describe_blob()
                for model in encoding['models']:
                    model['inputs'][index]['shape'] = make(np.zeros(model['inputs'][index]['shape'])).shape
                return encoding
        return MDP
    return decorate


def downsample(index, height, width):
    def make(image):
        return image[::height, ::width]

    def decorate(mdp):
        class MDP(mdp):
            class Controller(mdp.Controller):
                def get_state(self):
                    state = super().get_state()
                    state['inputs'][index] = make(state['inputs'][index])
                    return state

            def describe_blob(self):
                encoding = super().describe_blob()
                for model in encoding['models']:
                    model['inputs'][index]['shape'] = make(np.zeros(model['inputs'][index]['shape'])).shape
                return encoding
        return MDP
    return decorate


def downsample_hwc(index, height, width):
    def make(image):
        return image[::height, ::width, :]

    def decorate(mdp):
        class MDP(mdp):
            class Controller(mdp.Controller):
                def get_state(self):
                    state = super().get_state()
                    state['inputs'][index] = make(state['inputs'][index])
                    return state

            def describe_blob(self):
                encoding = super().describe_blob()
                for model in encoding['models']:
                    model['inputs'][index]['shape'] = make(np.zeros(model['inputs'][index]['shape'])).shape
                return encoding
        return MDP
    return decorate


def resize(index, height, width, **kwargs):
    import cv2

    def make(image):
        return cv2.resize(image, (width, height), **kwargs)

    def decorate(mdp):
        class MDP(mdp):
            class Controller(mdp.Controller):
                def get_state(self):
                    state = super().get_state()
                    state['inputs'][index] = make(state['inputs'][index])
                    return state

            def describe_blob(self):
                encoding = super().describe_blob()
                for model in encoding['models']:
                    model['inputs'][index]['shape'] = make(np.zeros(model['inputs'][index]['shape'])).shape
                return encoding
        return MDP
    return decorate


def stack_chw(index, size):
    NAME_FUNC = inspect.getframeinfo(inspect.currentframe()).function
    PATH_FUNC = f'{__name__}.{NAME_FUNC}{index}'

    def make(self, image):
        if not hasattr(self, PATH_FUNC):
            setattr(self, PATH_FUNC, collections.deque([image] * size, maxlen=size))
        attr = getattr(self, PATH_FUNC)
        attr.append(image)
        assert len(attr) == size
        return np.concatenate(attr, axis=0)

    def decorate(mdp):
        class MDP(mdp):
            class Controller(mdp.Controller):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    assert not hasattr(self, PATH_FUNC)

                def get_state(self):
                    state = super().get_state()
                    state['inputs'][index] = make(self, state['inputs'][index])
                    return state

            def describe_blob(self):
                encoding = super().describe_blob()
                for model in encoding['models']:
                    shape = model['inputs'][index]['shape']
                    model['inputs'][index]['shape'] = (shape[0] * size,) + shape[1:]
                return encoding
        return MDP
    return decorate
