import { useRef, useState } from "react";
import { Editor, OnMount } from "@monaco-editor/react";
import style from "../../util/Styles";
import { RunBtn, ResetBtn, TestBtn } from "../Buttons";
import {
  resetPreviousCode,
  executePythonCode,
  testStudentCode,
} from "../../util/util";
import { useParams } from "react-router-dom";
import { TestResult } from "../../util/types";
import { defaultHintTitle } from "../../pages/Exercise";

interface Props {
  skelCode: string;
  studentCode: string;
  previousCode: string;
  language: string;
  setStudentCode: (code: string) => void;
  setOutput: (output: string) => void;
  setError: (error: string) => void;
  setTestResults: (results: TestResult[]) => void;
  setHintTitle: (title: string) => void;
}
function CodeBox({
  skelCode,
  previousCode,
  language,
  studentCode,
  setStudentCode,
  setOutput,
  setError,
  setTestResults,
  setHintTitle,
}: Props) {
  const MIN_HEIGHT = 150;
  const MAX_HEIGHT = 400;
  const LINE_HEIGHT = 20;

  const editorRef = useRef<any>(null);
  const [editorHeight, setEditorHeight] = useState(MIN_HEIGHT);

  const { studentName, lang, exercise } = useParams();
  const exerciseId = `${lang}_${exercise}`;

  // Define a custom theme
  const defineCustomTheme = (monaco: any) => {
    monaco.editor.defineTheme("customTheme", {
      base: "vs-dark",
      inherit: true,
      rules: [],
      colors: {
        "editor.background": "#212936",
      },
    });
  };

  const handleEditorDidMount: OnMount = (editor, monaco) => {
    editorRef.current = editor;

    // Adjust height of the codebox based on code length
    const updateHeight = () => {
      const lineCount = editor.getModel()?.getLineCount() || 1;
      const newHeight = Math.min(
        Math.max(lineCount * LINE_HEIGHT, MIN_HEIGHT),
        MAX_HEIGHT
      );

      setEditorHeight(newHeight);
    };

    editor.onDidContentSizeChange(updateHeight);

    // Adjust height on mount
    updateHeight();

    defineCustomTheme(monaco);
    monaco.editor.setTheme("customTheme");
  };

  const resetCode = () => {
    const defaultCode = skelCode;
    if (editorRef.current) {
      editorRef.current.setValue(defaultCode);
      setEditorHeight(MIN_HEIGHT);
      resetPreviousCode(studentName!, exerciseId, defaultCode);
    }
    setOutput("");
    setError("");
    setTestResults([]);
    setHintTitle(defaultHintTitle);
  };

  const runCode = async () => {
    const runOutput = await executePythonCode(studentCode);
    if (runOutput.output) {
      setOutput(runOutput.output);
    }
    if (runOutput.error) {
      setError(runOutput.error);
      setHintTitle("Ran into an error? Click for a hint");
    } else {
      setHintTitle(defaultHintTitle);
    }
    setTestResults([]);
  };

  const testCode = async () => {
    setOutput("");
    setError("");
    const data = await testStudentCode(studentName!, exerciseId, studentCode);
    setTestResults(data.testResults);
    setHintTitle(
      "Tried running tests? Click here for a hint on why specific tests may be failing"
    );

    if (data.stderr) {
      setError(data.stderr);
      setHintTitle("Ran into an error? Click for a hint");
    }
  };

  return (
    <div className={style(styles, "ctn")}>
      <div className={style(styles, "btnCtn")}>
        <RunBtn handleBtn={runCode} />
        <TestBtn handleBtn={testCode} />
        <ResetBtn handleBtn={resetCode} />
      </div>
      <div
        className={style(styles, "editorCtn")}
        style={{
          height: `${editorHeight}px`,
        }}
      >
        <Editor
          height="100%"
          language={language}
          theme="vs-dark"
          value={previousCode}
          onMount={handleEditorDidMount}
          onChange={(value) => setStudentCode(value || "")}
          options={{
            fontSize: 14,
            minimap: { enabled: false },
            lineNumbers: "on",
            scrollBeyondLastLine: false,
            wordWrap: "on",
            scrollbar: {
              vertical: editorHeight === MAX_HEIGHT ? "auto" : "hidden",
            },
            padding: { top: 20 },
          }}
        />
      </div>
    </div>
  );
}

const styles = {
  ctn: ["flex", "flex-col", "bg-editor-blue", "p-4", "gap-4", "rounded-lg"],
  btnCtn: ["flex", "items-center", "justify-end", "gap-5"],
  editorCtn: ["flex", "flex-col", "w-full", "rounded-md", "overflow-hidden"],
};

export default CodeBox;
