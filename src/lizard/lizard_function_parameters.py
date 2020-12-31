"""Create a profile for the interface sizes of a codebase."""
import lizard


def analyze_function_parameters(input_file, output_file):
    """Analyze the function size."""
    results = lizard.analyze_file(input_file)
    print(output_file)
    print(results)
