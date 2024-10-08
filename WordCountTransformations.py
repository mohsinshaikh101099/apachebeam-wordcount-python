import apache_beam as beam

with beam.Pipeline() as p:
    # Read lines from the input file
    lines = p | 'Read' >> beam.io.ReadFromText('input.txt')

    # Split lines into words
    words = lines | 'SplitIntoWords' >> beam.FlatMap(lambda line: line.split())

    # Filter out short words
    long_words = words | 'FilterShortWords' >> beam.Filter(lambda word: len(word) >= 4)

    # Count occurrences of each word
    word_counts = long_words | 'CountWords' >> beam.combiners.Count.PerElement()

    # Format the results as strings
    formatted = word_counts | 'FormatResults' >> beam.Map(lambda wc: f'{wc[0]}: {wc[1]}')

    # Write the results to an output file
    formatted | 'Write' >> beam.io.WriteToText('wordcountslength4.txt')
