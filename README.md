# MABP - Malware Analysis Bot Platform

MABP is a partially context-aware chatbot powered by GPT-3 that serves for basic static analysis tasks. Currently, it can perform the following functions:

- Analyze a PE executable
- Collect md5, sha1, sha256, and sha512 hashes for the sample
- Parse PE, DOS, and Image Optional headers
- Parse the import address table (IAT) for imports 
- Get sentiment analysis on whether certain imports are used in malicious code or not
- Generate simple yara rules based on criteria collected during analysis
- Learn tips and tricks with the `learn` command
- Interact with GPT-3 directly via natural text in the `Input>` area

This platform aims to streamline the process of performing basic static analysis on malware samples, making it easier and more accessible for security researchers, analysts and hobbyists alike. The context-awareness capabilities of GPT-3 ensures that the chatbot is able to respond to a variety of inputs and provide relevant information to users.

## Setup Instructions

To setup MABP, first you will need to create an `OPENAI_API_KEY` environment variable, and export your OpenAI API key to it.
```bash
export OPENAI_API_KEY='YOUR_OPENAI_API_KEY_HERE'
```

Next, install the required packages from `requirements.txt` with `pip`:
```bash
pip3 install -r requirements.txt
```

Finally, run the main script:
```bash
python3 ./mabp.py
```

## How to Use

To use MABP, simply run the main script and follow the prompt. You will be able to select from a list of available commands by typing "help" for more information on each option. The following commands are currently implemented:

| Command | Description |
| ------- | ----------- |
| `banner` | Display ASCII art |
| `analyze_file` | Analyze a binary |
| `make_yara` | Generate Yara rules |
| `clear` | Clear the terminal |
| `help` | Display the help menu |
| `quit` or `exit` | Exit the script |

The chatbot can be used through a command line interface or integrated into other systems. To get started, simply input your desired analysis task and follow the prompt.

## Contributing

If you're interested in contributing to the project, please reach out to the project maintainers for more information on how to get involved.

## References
- [LIEF - Library to Instrument Executable Formats](https://lief.quarkslab.com)
- [OpenAI's GPT-3](https://openai.com/gpt-3/)

## License

This project is licensed under the MIT License. Please see the LICENSE file for more details.
