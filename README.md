# Java Code Slicer

## Overview
Java Code Slicer is a Python tool designed to automate the process of identifying refactoring opportunities in Java code, specifically for the "Extract Method" refactoring. It analyzes Java methods to find chunks of code that can be extracted into separate methods, thereby improving code readability, maintainability, and adherence to the Single Responsibility Principle (SRP). This tool is inspired by the methodology outlined in "Identifying Extract Method Refactoring Opportunities Based on Functional Relevance" by Charalampidou et al., utilizing the concept of functional relevance to suggest refactorings.

## Features
- Analyzes Java code to identify long methods that can benefit from refactoring.
- Uses the concept of functional relevance to suggest code chunks for the "Extract Method" refactoring.
- Ranks refactoring opportunities based on an estimate of their fitness for extraction.
- Empirically validated on industrial and open-source projects for effectiveness.

## Installation

1. Ensure Python 3.x is installed on your system.
2. Clone the repository to your local machine.
3. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To use the Java Code Slicer, follow these steps:

1. Place your Java code files in the `src` directory.
2. Run the tool from the command line:
   ```bash
   python code_slicer.py src/myJavaFile.java
   ```
3. The tool will analyze the specified Java file and output suggested refactoring opportunities.

## Configuration
You can configure the tool's parameters (e.g., method size thresholds for analysis) in the `config.json` file to tailor the analysis to your specific needs.

## How It Works
The tool parses the input Java code to build an abstract syntax tree (AST). It then analyzes the AST to identify methods that violate the Single Responsibility Principle by implementing diverse functionalities. By calculating cohesion among statements within a method, it suggests code chunks that collaborate to provide specific functionality and proposes their extraction into separate methods.

## Validation
The accuracy and effectiveness of Java Code Slicer have been validated in both industrial and open-source settings, demonstrating its capability to identify functionally related statements within long methods with high recall rates.

## Contributing
Contributions to the Java Code Slicer are welcome. Please read `CONTRIBUTING.md` for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the `LICENSE` file for details.

## Acknowledgments
This tool is based on the research and methodologies developed by Sofia Charalampidou, Apostolos Ampatzoglou, Alexander Chatzigeorgiou, Antonios Gkortzis, and Paris Avgeriou in their work on identifying extract method refactoring opportunities based on functional relevance.
