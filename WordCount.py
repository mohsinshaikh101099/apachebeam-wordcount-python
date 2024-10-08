import apache_beam as beam

with beam.Pipeline() as p:

    # Read lines from input file

    lines = p | 'Read' >> beam.io.ReadFromText('input.txt') # if the code throws error give full path to your input file eg. C:/users/user-name/input.txt

    # Split each line into words and create a key-value pair (word, 1)

    words = lines | 'ExtractWords' >> beam.FlatMap(lambda line: line.split())

    # Count occurrences of each word

    word_counts = words | 'CountWords' >> beam.combiners.Count.PerElement()

    # Format the results into strings for output

    formatted = word_counts | 'FormatResults' >> beam.Map(lambda word_count: f'{word_count[0]}: {word_count[1]}')

    # Write the results to an output file

    formatted | 'Write' >> beam.io.WriteToText('wordcounts.txt')