# -*- coding: utf-8 -*-
#
# Copyright 2015 Simone Campagna
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import inspect

__all__ = (
    'Register',
    'Key',
    'get_function',
    'register',
)


class Key(object):
    def __init__(self, key=None):
        self._key = key

    @property
    def key(self):
        return self._key


def get_function(function_or_class):
    if isinstance(function_or_class, type):
        function = function_or_class.__init__
    else:
        function = function_or_class
    return function


class Register(object):
    def __init__(self):
        self._register = {}

    def _get_key(self, key, value):
        if isinstance(value, Key):
            if value.key is None:
                value = Key(key)
        else:
            value = Key(value)
        return value

    def get(self, function_or_class, default=None):
        function = get_function(function_or_class)
        return self._register.get(function, default)

    def __call__(self, *inject_args, **inject_kwargs):
        function_injected_args = {}
        for arg_value in inject_args:
            key = self._get_key(None, arg_value)
            arg_name = key.key
            if arg_name is None:
                raise KeyError("undefined")
            function_injected_args[arg_name] = key
        for arg_name, arg_value in inject_kwargs.items():
            key = self._get_key(arg_name, arg_value)
            function_injected_args[arg_name] = key

        def register_decorator(function_or_class):
            function = get_function(function_or_class)
            signature = inspect.signature(function)
            self._register[function] = (signature, function_injected_args)
            return function_or_class

        return register_decorator


register = Register()
