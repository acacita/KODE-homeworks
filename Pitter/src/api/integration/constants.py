import os
from typing import List, NamedTuple, Union

CONFIDENT_ENOUGH = 0.7


class SpeechContext:  # todo rethink about full version usage, if any ideas occur implement this type
    pass


RecognitionAudioShort = NamedTuple('NamedTuple', [('content', str)])
RecognitionAudioLong = NamedTuple('NamedTuple', [('uri', str)])
RecognitionAudio = Union[RecognitionAudioShort, RecognitionAudioLong]

RecognitionConfigFull = NamedTuple('RecognitionConfig', [('encoding', str),
                                                         ('sampleRateHertz', int),
                                                         ('audioChannelCount', int),
                                                         ('enableSeparateRecognitionPerChannel', bool),
                                                         ('languageCode', str),
                                                         ('maxAlternatives', int),
                                                         ('profanityFilter', bool),
                                                         ('speechContexts', List[SpeechContext]),
                                                         ('enableWordTimeOffsets', bool),
                                                         ('model', str),
                                                         ('useEnhanced', bool)])

RecognitionConfigShort = NamedTuple('RecognitionConfigShort', [("encoding", str),
                                                               ('languageCode', str),
                                                               ('profanityFilter', bool),
                                                               ]
                                    )

RecognitionConfig = Union[RecognitionConfigFull, RecognitionConfigShort]

RecognizeRequest = NamedTuple('RecognizeRequest', [('config', RecognitionConfig),
                                                   ('audio', RecognitionAudio),
                                                   ])



def get_key():
    cwd = os.getcwd()
    rel_path = os.path.join(cwd, 'api/integration/api-key.txt')
    with open(rel_path, 'r') as f:
        return f.read()

API_KEY = get_key()