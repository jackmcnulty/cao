# cao/engine.py 

import os
from .registry import ConverterRegistry

def convert(input_path, output_path, **options):
    input_ext = os.path.splitext(input_path)[1][1:]
    output_ext = os.path.splitext(output_path)[1][1:]

    SourceFactory = ConverterRegistry.get_source(input_ext)
    TargetClass = ConverterRegistry.get_target(output_ext)

    if not SourceFactory:
        raise ValueError(f"No source registered for: {input_ext}")
    if not TargetClass:
        raise ValueError(f"No target registered for: {output_ext}")

    source = SourceFactory()
    data = source.extract(input_path, options=options)

    if not TargetClass.accepts_type(data["type"]):
        raise ValueError(f"{output_ext} target does not support data type: {data['type']}")

    TargetClass.write(data, output_path)
