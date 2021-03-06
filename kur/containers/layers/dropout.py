"""
Copyright 2017 Deepgram

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from . import Layer, ParsingError

###############################################################################
class Dropout(Layer):	# pylint: disable=too-few-public-methods
	""" A dropout layer.
	"""

	###########################################################################
	def __init__(self, *args, **kwargs):
		""" Creates a new dropout layer.
		"""
		super().__init__(*args, **kwargs)
		self.dropout = None

	###########################################################################
	def _parse(self, engine):
		""" Parse the layer.
		"""

		super()._parse(engine)

		if isinstance(self.args, dict):
			if 'fraction' in self.args:
				self.dropout = engine.evaluate(
					self.args['fraction'], recursive=True)
				if not isinstance(self.dropout, (int, float)):
					raise ParsingError('"dropout" must be a float.')
			else:
				raise ParsingError('Missing required key "fraction" for '
					'Dropout layer.')
		elif isinstance(self.args, (int, float)):
			self.dropout = self.args
		else:
			raise ParsingError('Dropout layer requires a single '
				'floating-point argument argument. Instead we received: {}'
				.format(self.args))

		self.dropout = float(self.dropout)
		if self.dropout < 0 or self.dropout >= 1:
			raise ParsingError('Dropout fraction must be >= 0 and < 1.')

	###########################################################################
	def _build(self, model):
		""" Instantiates the layer with the given backend.
		"""
		backend = model.get_backend()
		if backend.get_name() == 'keras':

			import keras.layers as L			# pylint: disable=import-error
			yield L.Dropout(
				self.dropout,
				name=self.name
			)

		else:
			raise ValueError(
				'Unknown or unsupported backend: {}'.format(backend))

	###########################################################################
	def shape(self, input_shapes):
		""" Returns the output shape of this layer for a given input shape.
		"""
		if len(input_shapes) > 1:
			raise ValueError('Dropout only take a single input.')
		input_shape = input_shapes[0]
		return input_shape

### EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF
