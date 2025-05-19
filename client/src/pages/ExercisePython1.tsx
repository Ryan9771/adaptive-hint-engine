import axios from "axios";

const code = `def is_palindrome():
	print("hi there")

is_palindrome()`;

const executePythonCode = async (code: string) => {
  try {
    const response = await axios.post(
      "https://emkc.org/api/v2/piston/execute",
      {
        language: "python",
        version: "3.10.0",
        files: [
          {
            name: "main.py",
            content: code,
          },
        ],
      }
    );

    const { run } = response.data;
    return {
      output: run.stdout,
      error: run.stderr,
    };
  } catch (error) {
    console.error("Error executing code:", error);
    return {
      output: "",
      error: "An error occurred while executing the code.",
    };
  }
};

console.log(executePythonCode);
